import React, { useState } from 'react';
import { Task, Tag, Category } from '@/types';

interface TaskCardProps {
  task: Task;
  onUpdate: (id: number, updates: Partial<Task>) => void;
  onDelete: (id: number) => void;
  onToggleComplete: (id: number) => void;
  onAddTags?: (taskId: number, tagIds: number[]) => void;
  onRemoveTags?: (taskId: number, tagIds: number[]) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onUpdate,
  onDelete,
  onToggleComplete,
  onAddTags,
  onRemoveTags
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [category, setCategory] = useState<number | null>(task.category_id);
  const [dueDate, setDueDate] = useState<string | null>(task.due_date);
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>(task.priority);
  const [selectedTags, setSelectedTags] = useState<number[]>(task.tags.map(t => t.id));

  const handleSave = () => {
    // Check if tags have changed and update them separately
    const tagsChanged = JSON.stringify(selectedTags) !== JSON.stringify(task.tags.map(t => t.id));

    onUpdate(task.id, {
      title,
      description: description || undefined,
      category_id: category,
      due_date: dueDate,
      priority
    });

    // If tags changed, handle tag updates
    if (tagsChanged && onAddTags && onRemoveTags) {
      const currentTagIds = task.tags.map(t => t.id);
      const addedTagIds = selectedTags.filter(id => !currentTagIds.includes(id));
      const removedTagIds = currentTagIds.filter(id => !selectedTags.includes(id));

      if (addedTagIds.length > 0) {
        onAddTags(task.id, addedTagIds);
      }
      if (removedTagIds.length > 0) {
        onRemoveTags(task.id, removedTagIds);
      }
    }

    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setCategory(task.category_id);
    setDueDate(task.due_date);
    setPriority(task.priority);
    setSelectedTags(task.tags.map(t => t.id));
    setIsEditing(false);
  };

  const handleToggleComplete = () => {
    onToggleComplete(task.id);
  };

  const handleTagToggle = (tagId: number) => {
    if (selectedTags.includes(tagId)) {
      setSelectedTags(selectedTags.filter(id => id !== tagId));
    } else {
      setSelectedTags([...selectedTags, tagId]);
    }
  };

  const getPriorityColor = (priority: 'low' | 'medium' | 'high') => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return 'Tomorrow';
    } else {
      return date.toLocaleDateString();
    }
  };

  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !task.completed;

  return (
    <div className={`bg-white shadow rounded-lg p-4 ${task.completed ? 'opacity-75' : ''} ${isOverdue ? 'border-l-4 border-red-500' : ''}`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Task title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Task description (optional)"
            rows={2}
          />

          {/* Category Selector */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Category</label>
            <select
              value={category || ''}
              onChange={(e) => setCategory(e.target.value ? parseInt(e.target.value) : null)}
              className="w-full px-3 py-1 border border-gray-300 rounded text-sm"
            >
              <option value="">No Category</option>
              <option value="1">Work</option>
              <option value="2">Personal</option>
              <option value="3">Shopping</option>
            </select>
          </div>

          {/* Due Date */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Due Date</label>
            <input
              type="date"
              value={dueDate || ''}
              onChange={(e) => setDueDate(e.target.value || null)}
              className="w-full px-3 py-1 border border-gray-300 rounded text-sm"
            />
          </div>

          {/* Priority */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Priority</label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
              className="w-full px-3 py-1 border border-gray-300 rounded text-sm"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Tags</label>
            <div className="flex flex-wrap gap-1">
              {task.tags.map((tag) => (
                <button
                  key={tag.id}
                  type="button"
                  className={`px-2 py-1 rounded-full text-xs ${
                    selectedTags.includes(tag.id)
                      ? 'bg-blue-100 text-blue-800 border border-blue-300'
                      : 'bg-gray-100 text-gray-800 border border-gray-300'
                  }`}
                  onClick={() => handleTagToggle(tag.id)}
                >
                  #{tag.name}
                </button>
              ))}
            </div>
          </div>

          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleComplete}
              className="h-4 w-4 text-indigo-600 border-gray-300 rounded mt-1"
            />
            <div className="ml-3 flex-1">
              <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-500'}`}>
                  {task.description}
                </p>
              )}

              <div className="mt-2 flex flex-wrap gap-2">
                {/* Category */}
                {task.category && (
                  <span
                    className="px-2 py-1 text-xs rounded-full"
                    style={{
                      backgroundColor: `${task.category.color}20`,
                      color: task.category.color,
                      border: `1px solid ${task.category.color}`
                    }}
                  >
                    {task.category.name}
                  </span>
                )}

                {/* Tags */}
                {task.tags.map((tag) => (
                  <span key={tag.id} className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full">
                    #{tag.name}
                  </span>
                ))}

                {/* Priority */}
                <span className={`px-2 py-1 text-xs rounded-full ${getPriorityColor(task.priority)}`}>
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </span>

                {/* Due Date */}
                {task.due_date && (
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    isOverdue ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    📅 {formatDate(task.due_date)}
                  </span>
                )}
              </div>

              <div className="mt-2 text-xs text-gray-500">
                Created: {new Date(task.created_at).toLocaleString()}
                {task.updated_at !== task.created_at && (
                  <span>, Updated: {new Date(task.updated_at).toLocaleString()}</span>
                )}
              </div>
            </div>
          </div>
          <div className="mt-3 flex justify-end space-x-2">
            <button
              onClick={() => setIsEditing(true)}
              className="inline-flex items-center px-2.5 py-0.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskCard;