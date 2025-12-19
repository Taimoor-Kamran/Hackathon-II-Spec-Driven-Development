import React, { useState, useEffect, useCallback } from 'react';
import { Task, Category, Tag, SearchFilters } from '@/types';
import { api } from '@/lib/api';
import { websocketService } from '@/lib/websocket';
import TaskCard from './TaskCard';

interface TaskListProps {
  userId: string;
  filters?: SearchFilters;
}

const TaskList: React.FC<TaskListProps> = ({ userId, filters = {} }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);

  // Fetch tasks from API
  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      const tasksData = await api.getTasks(userId, filters);
      setTasks(tasksData);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  }, [userId, filters]);

  // Fetch categories and tags
  const fetchCategoriesAndTags = useCallback(async () => {
    try {
      const categoriesData = await api.getCategories(userId);
      const tagsData = await api.getTags(userId);
      setCategories(categoriesData);
      setTags(tagsData);
    } catch (err) {
      console.error('Error fetching categories and tags:', err);
    }
  }, [userId]);

  // Handle real-time updates from WebSocket
  useEffect(() => {
    // Connect to WebSocket
    websocketService.connect(Number(userId));

    // Subscribe to task updates
    const unsubscribeTaskUpdates = websocketService.subscribeToTaskUpdates((task, type) => {
      if (type === 'task_update' || type === 'collaboration_task_update') {
        setTasks(prevTasks =>
          prevTasks.map(t => (t.id === task.id ? task : t))
        );
      } else if (type === 'task_create') {
        setTasks(prevTasks => [task, ...prevTasks]);
      } else if (type === 'task_delete') {
        setTasks(prevTasks => prevTasks.filter(t => t.id !== task.id));
      } else if (type === 'task_complete') {
        setTasks(prevTasks =>
          prevTasks.map(t =>
            t.id === task.id ? { ...t, completed: task.completed } : t
          )
        );
      }
    });

    // Subscribe to category updates
    const unsubscribeCategoryUpdates = websocketService.subscribeToCategoryUpdates((category, type) => {
      if (type === 'category_update') {
        setTasks(prevTasks =>
          prevTasks.map(task => {
            if (task.category_id === category.id && task.category) {
              return { ...task, category };
            }
            return task;
          })
        );
      }
    });

    // Subscribe to tag updates
    const unsubscribeTagUpdates = websocketService.subscribeToTagUpdates((tag, type) => {
      if (type === 'tag_update') {
        setTasks(prevTasks =>
          prevTasks.map(task => {
            if (task.tags.some(t => t.id === tag.id)) {
              return {
                ...task,
                tags: task.tags.map(t => t.id === tag.id ? tag : t)
              };
            }
            return task;
          })
        );
      }
    });

    // Cleanup on unmount
    return () => {
      unsubscribeTaskUpdates();
      unsubscribeCategoryUpdates();
      unsubscribeTagUpdates();
      websocketService.disconnect();
    };
  }, [userId]);

  // Fetch data on component mount and when filters change
  useEffect(() => {
    fetchTasks();
    fetchCategoriesAndTags();
  }, [fetchTasks, fetchCategoriesAndTags]);

  // Handle task updates
  const handleTaskUpdate = async (id: number, updates: Partial<Task>) => {
    try {
      const updatedTask = await api.updateTask(userId, id, updates);
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === id ? updatedTask : task
        )
      );

      // Send collaboration event for real-time updates
      websocketService.sendCollaborationEvent('task_update', updatedTask);
    } catch (err) {
      console.error('Error updating task:', err);
      setError('Failed to update task');
    }
  };

  // Handle task deletion
  const handleTaskDelete = async (id: number) => {
    try {
      await api.deleteTask(userId, id);
      // Directly update the state since WebSocket is not supported in Phase II
      setTasks(prevTasks => prevTasks.filter(task => task.id !== id));
      // Send WebSocket event for compatibility (though it won't do anything in Phase II)
      websocketService.sendCollaborationEvent('task_delete', { id });
    } catch (err) {
      console.error('Error deleting task:', err);
      setError('Failed to delete task');
    }
  };

  // Handle task completion toggle
  const handleTaskToggleComplete = async (id: number) => {
    try {
      const task = tasks.find(t => t.id === id);
      if (!task) return;

      const updatedTask = await api.toggleTaskCompletion(userId, id);
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === id ? updatedTask : task
        )
      );

      // Send collaboration event for real-time updates
      websocketService.sendCollaborationEvent('task_complete', {
        id: updatedTask.id,
        completed: updatedTask.completed
      });
    } catch (err) {
      console.error('Error toggling task completion:', err);
      setError('Failed to update task');
    }
  };

  // Handle adding tags to a task
  const handleAddTags = async (taskId: number, tagIds: number[]) => {
    try {
      const updatedTask = await api.addTagsToTask(userId, taskId, tagIds);
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? updatedTask : task
        )
      );

      // Send collaboration event for real-time updates
      websocketService.sendCollaborationEvent('task_update', updatedTask);
    } catch (err) {
      console.error('Error adding tags to task:', err);
      setError('Failed to add tags to task');
    }
  };

  // Handle removing tags from a task
  const handleRemoveTags = async (taskId: number, tagIds: number[]) => {
    try {
      const updatedTask = await api.removeTagsFromTask(userId, taskId, tagIds);
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? updatedTask : task
        )
      );

      // Send collaboration event for real-time updates
      websocketService.sendCollaborationEvent('task_update', updatedTask);
    } catch (err) {
      console.error('Error removing tags from task:', err);
      setError('Failed to remove tags from task');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-700">{error}</p>
        <button
          onClick={fetchTasks}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No tasks found</p>
          <p className="text-gray-400 text-sm mt-1">
            {filters.query || filters.status || filters.category_id || (filters.tag_ids && filters.tag_ids.length > 0)
              ? 'Try adjusting your filters'
              : 'Create your first task to get started'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onUpdate={handleTaskUpdate}
              onDelete={handleTaskDelete}
              onToggleComplete={handleTaskToggleComplete}
              onAddTags={handleAddTags}
              onRemoveTags={handleRemoveTags}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;