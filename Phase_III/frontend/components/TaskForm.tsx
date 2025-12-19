import React, { useState, useEffect } from 'react';
import { TaskCreateData, Category, Tag } from '@/types';
import { api } from '@/lib/api';
import DueDateSelector from '@/components/DueDateSelector';
import RecurringTaskForm from '@/components/RecurringTaskForm';

interface TaskFormProps {
  userId: string;
  onSuccess: () => void;
  onCancel: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ userId, onSuccess, onCancel }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState<number | null>(null);
  const [dueDate, setDueDate] = useState<string | null>(null);
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [selectedTags, setSelectedTags] = useState<number[]>([]);
  const [showRecurringForm, setShowRecurringForm] = useState(false);
  const [recurringData, setRecurringData] = useState<any>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCategoriesAndTags();
  }, [userId]);

  const loadCategoriesAndTags = async () => {
    try {
      const [categoriesData, tagsData] = await Promise.all([
        api.getCategories(userId),
        api.getTags(userId)
      ]);
      setCategories(categoriesData);
      setTags(tagsData);
    } catch (err) {
      console.error('Error loading categories and tags:', err);
      setError('Failed to load categories and tags');
    }
  };

  const handleTagToggle = (tagId: number) => {
    if (selectedTags.includes(tagId)) {
      setSelectedTags(selectedTags.filter(id => id !== tagId));
    } else {
      setSelectedTags([...selectedTags, tagId]);
    }
  };

  const handleSetRecurring = (data: any) => {
    setRecurringData(data);
    setShowRecurringForm(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const taskData: TaskCreateData = {
        title: title.trim(),
        description: description.trim() || undefined,
        category_id: categoryId || undefined,
        due_date: dueDate || undefined,
        priority,
        tag_ids: selectedTags.length > 0 ? selectedTags : undefined
      };

      const newTask = await api.createTask(userId, taskData);

      // If recurring data was set, create the recurring task
      if (recurringData) {
        await api.createRecurringTask(newTask.id, recurringData);
      }

      setTitle('');
      setDescription('');
      setCategoryId(null);
      setDueDate(null);
      setPriority('medium');
      setSelectedTags([]);
      setRecurringData(null);

      onSuccess();
    } catch (err) {
      console.error('Error creating task:', err);
      setError('Failed to create task');
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="Task title"
          required
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="Task description (optional)"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <select
            value={categoryId || ''}
            onChange={(e) => setCategoryId(e.target.value ? parseInt(e.target.value) : null)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">No Category</option>
            {categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Due Date
        </label>
        <DueDateSelector
          selectedDate={dueDate}
          onSelectDate={setDueDate}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Tags
        </label>
        <div className="flex flex-wrap gap-2">
          {tags.map(tag => (
            <button
              key={tag.id}
              type="button"
              className={`px-3 py-1 rounded-full text-sm ${
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

      <div>
        <button
          type="button"
          onClick={() => setShowRecurringForm(!showRecurringForm)}
          className="text-sm text-indigo-600 hover:text-indigo-800"
        >
          {recurringData ? 'Edit Recurring Pattern' : 'Set Recurring Pattern'}
        </button>
      </div>

      {showRecurringForm && (
        <RecurringTaskForm
          taskTitle={title}
          onSetRecurring={handleSetRecurring}
          onCancel={() => setShowRecurringForm(false)}
        />
      )}

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {loading ? 'Creating...' : 'Create Task'}
        </button>
      </div>
    </form>
  );
};

export default TaskForm;