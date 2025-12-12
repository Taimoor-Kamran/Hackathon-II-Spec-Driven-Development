'use client';

import { useState, useEffect } from 'react';
import { Task } from '@/types';
import TaskList from '@/components/TaskList';
import AddTaskForm from '@/components/AddTaskForm';
import { api } from '@/lib/api';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);

  // Get user ID from authentication
  useEffect(() => {
    const fetchUserAndTasks = async () => {
      try {
        const token = localStorage.getItem('authToken');
        if (!token) {
          // Redirect to login if no token
          window.location.href = '/login';
          return;
        }

        // Fetch user info to get the actual user ID
        const response = await fetch('http://localhost:8000/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          // If token is invalid, redirect to login
          localStorage.removeItem('authToken');
          window.location.href = '/login';
          return;
        }

        const userData = await response.json();
        const userId = userData.user_id;
        setUserId(userId.toString()); // Convert to string for API calls

        // Fetch tasks for this user
        if (userId) {
          fetchTasks(userId.toString());
        }
      } catch (error) {
        console.error('Error fetching user or tasks:', error);
        setError('Failed to load user data');
      }
    };

    fetchUserAndTasks();
  }, []);

  const fetchTasks = async (userId: string) => {
    try {
      setLoading(true);
      // Call the actual API to fetch tasks
      const tasks = await api.getTasks(userId);
      setTasks(tasks);
      setError(null);
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (title: string, description: string) => {
    if (!userId) {
      throw new Error('User not authenticated');
    }

    try {
      // Call the actual API to create a new task
      const newTask = await api.createTask(userId, { title, description });
      setTasks([...tasks, newTask]);
      return newTask; // Return the created task to indicate success
    } catch (err) {
      setError('Failed to add task');
      console.error('Error adding task:', err);
      throw err; // Re-throw the error so the form knows it failed
    }
  };

  const handleUpdateTask = async (id: number, updates: Partial<Task>) => {
    if (!userId) return;

    try {
      // Call the actual API to update the task
      const updatedTask = await api.updateTask(userId, id, updates);
      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (id: number) => {
    if (!userId) return;

    try {
      // Call the actual API to delete the task
      await api.deleteTask(userId, id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  const handleToggleComplete = async (id: number) => {
    if (!userId) return;

    try {
      // Call the actual API to toggle task completion
      const updatedTask = await api.toggleTaskCompletion(userId, id);
      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
            <button
              className="text-sm text-indigo-600 hover:text-indigo-900"
              onClick={() => {
                // In a real app, this would log out the user
                localStorage.removeItem('authToken');
                window.location.href = '/';
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
              {userId ? (
                <AddTaskForm onAddTask={handleAddTask} />
              ) : (
                <div className="mb-6 text-center text-gray-500">
                  Loading form...
                </div>
              )}

              {error && (
                <div className="rounded-md bg-red-50 p-4 mb-4">
                  <div className="text-sm text-red-700">{error}</div>
                </div>
              )}

              <TaskList
                tasks={tasks}
                onUpdateTask={handleUpdateTask}
                onDeleteTask={handleDeleteTask}
                onToggleComplete={handleToggleComplete}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}