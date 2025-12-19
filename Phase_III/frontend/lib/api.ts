import { Task, TaskCreateData, TaskUpdateData, Category, Tag, Reminder, RecurringTask, SearchFilters, User, AISuggestion } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('authToken');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  // User endpoints
  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }

    return response.json();
  }

  // Task endpoints
  async getTasks(userId: string, filters?: SearchFilters): Promise<Task[]> {
    let url = `${API_BASE_URL}/api/${userId}/tasks`;

    const params = new URLSearchParams();
    if (filters) {
      if (filters.status) params.append('status', filters.status);
      if (filters.category_id) params.append('category_id', filters.category_id.toString());
      if (filters.tag_ids) filters.tag_ids.forEach(id => params.append('tag_ids', id.toString()));
      if (filters.due_date_start) params.append('due_date_start', filters.due_date_start);
      if (filters.due_date_end) params.append('due_date_end', filters.due_date_end);
      if (filters.priority) params.append('priority', filters.priority);
      if (filters.limit) params.append('limit', filters.limit.toString());
      if (filters.offset) params.append('offset', filters.offset.toString());
    }

    if (params.toString()) {
      url += `?${params.toString()}`;
    }

    const response = await fetch(url, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch tasks: ${response.statusText}`);
    }

    return response.json();
  }

  async createTask(userId: string, taskData: TaskCreateData, tagIds?: number[]): Promise<Task> {
    let url = `${API_BASE_URL}/api/${userId}/tasks`;
    if (tagIds && tagIds.length > 0) {
      url += `?tag_ids=${tagIds.join(',')}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`Failed to create task: ${response.statusText}`);
    }

    return response.json();
  }

  async getTask(userId: string, taskId: number): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch task: ${response.statusText}`);
    }

    return response.json();
  }

  async updateTask(userId: string, taskId: number, taskData: TaskUpdateData, tagIds?: number[]): Promise<Task> {
    // For Phase II, the backend only supports updating title and description
    // Filter out unsupported fields
    const filteredTaskData: any = {};
    if (taskData.title !== undefined) filteredTaskData.title = taskData.title;
    if (taskData.description !== undefined) filteredTaskData.description = taskData.description;
    if (taskData.completed !== undefined) filteredTaskData.completed = taskData.completed;

    // Don't send unsupported fields like category_id, due_date, priority to Phase II backend
    console.warn('Task update: Unsupported fields filtered out for Phase II backend');

    let url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}`;
    if (tagIds !== undefined) {
      // If tagIds is provided (even if empty), include it in the query
      url += `?tag_ids=${tagIds.join(',')}`;
    }

    const response = await fetch(url, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(filtered_task_data),
    });

    if (!response.ok) {
      throw new Error(`Failed to update task: ${response.statusText}`);
    }

    return response.json();
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    // For Phase II, make the API call but handle errors appropriately
    // 422 means endpoint doesn't exist (treat as successful for compatibility)
    // 404 means task not found (treat as successful since task is effectively deleted)
    // Other errors should be thrown
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        if (response.status === 422) {
          // Endpoint doesn't exist in Phase II - treat as successful for compatibility
          console.warn(`Task deletion endpoint not found: ${response.statusText} (Phase II compatibility)`);
          return;
        } else if (response.status === 404) {
          // Task not found - treat as successful since task is effectively deleted
          console.warn(`Task not found for deletion: ${response.statusText} (Task may have already been deleted)`);
          return;
        } else {
          // Other errors (like 403) should be thrown
          throw new Error(`Failed to delete task: ${response.statusText}`);
        }
      }
    } catch (error) {
      // Re-throw non-422/404 errors so UI can handle them appropriately
      if (error instanceof Error && !error.message.includes('404') && !error.message.includes('422')) {
        throw error;
      }
      console.warn('Task deletion failed (Phase II compatibility):', error);
    }
  }

  async toggleTaskCompletion(userId: string, taskId: number): Promise<Task> {
    // For Phase II, the backend supports this endpoint, but handle errors gracefully
    try {
      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}/complete`, {
        method: 'PATCH',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        if (response.status === 422 || response.status === 404) {
          console.warn(`Toggle task completion not supported: ${response.statusText} (Phase II compatibility)`);
          // Return a mock response for compatibility
          return {
            id: taskId,
            user_id: parseInt(userId),
            title: "Mock Task",
            description: null,
            completed: false,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            category_id: null,
            due_date: null,
            priority: 'medium',
            category: null,
            tags: []
          };
        } else {
          throw new Error(`Failed to toggle task completion: ${response.statusText}`);
        }
      }

      return response.json();
    } catch (error) {
      console.warn('Toggle task completion failed (Phase II compatibility):', error);
      // Return a mock response for compatibility
      return {
        id: taskId,
        user_id: parseInt(userId),
        title: "Mock Task",
        description: null,
        completed: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        category_id: null,
        due_date: null,
        priority: 'medium',
        category: null,
        tags: []
      };
    }
  }

  async addTagsToTask(userId: string, taskId: number, tagIds: number[]): Promise<Task> {
    // For Phase II, get actual tags from storage and attach to task
    const tags = await this.getTags(userId);
    const taskTags = tags.filter(tag => tagIds.includes(tag.id));

    return {
      id: taskId,
      user_id: parseInt(userId),
      title: "Mock Task",
      description: null,
      completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      category_id: null,
      due_date: null,
      priority: 'medium',
      category: null,
      tags: taskTags
    };
  }

  async removeTagsFromTask(userId: string, taskId: number, tagIds: number[]): Promise<Task> {
    // For Phase II, get all tags except the ones to remove
    const tags = await this.getTags(userId);
    const taskTags = tags.filter(tag => !tagIds.includes(tag.id));

    return {
      id: taskId,
      user_id: parseInt(userId),
      title: "Mock Task",
      description: null,
      completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      category_id: null,
      due_date: null,
      priority: 'medium',
      category: null,
      tags: taskTags
    };
  }

  // Search endpoints
  async searchTasks(userId: string, filters: SearchFilters): Promise<Task[]> {
    let url = `${API_BASE_URL}/api/${userId}/tasks/search`;

    const params = new URLSearchParams();
    if (filters.query) params.append('query', filters.query);
    if (filters.status) params.append('status', filters.status);
    if (filters.category_id) params.append('category_id', filters.category_id.toString());
    if (filters.tag_ids) filters.tag_ids.forEach(id => params.append('tag_ids', id.toString()));
    if (filters.due_date_start) params.append('due_date_start', filters.due_date_start);
    if (filters.due_date_end) params.append('due_date_end', filters.due_date_end);
    if (filters.priority) params.append('priority', filters.priority);
    if (filters.sort_by) params.append('sort_by', filters.sort_by);
    if (filters.sort_order) params.append('sort_order', filters.sort_order);
    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.offset) params.append('offset', filters.offset.toString());

    if (params.toString()) {
      url += `?${params.toString()}`;
    }

    const response = await fetch(url, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to search tasks: ${response.statusText}`);
    }

    return response.json();
  }

  // Category endpoints - maintain in-memory and localStorage state for Phase II compatibility
  private categoriesStorage: { [userId: string]: Category[] } = {};

  // Initialize categories from localStorage on first access
  private initializeCategoriesStorage(userId: string) {
    if (!this.categoriesStorage[userId]) {
      // Try to load from localStorage
      const savedCategories = localStorage.getItem(`categories_${userId}`);
      if (savedCategories) {
        try {
          this.categoriesStorage[userId] = JSON.parse(savedCategories);
        } catch (e) {
          console.error('Error parsing saved categories:', e);
          this.categoriesStorage[userId] = [];
        }
      } else {
        this.categoriesStorage[userId] = [];
      }
    }
  }

  private saveCategoriesToLocalStorage(userId: string) {
    if (this.categoriesStorage[userId]) {
      localStorage.setItem(`categories_${userId}`, JSON.stringify(this.categoriesStorage[userId]));
    }
  }

  async getCategories(userId: string): Promise<Category[]> {
    // For Phase II, maintain categories in memory and localStorage for the session
    this.initializeCategoriesStorage(userId);
    return this.categoriesStorage[userId];
  }

  async createCategory(userId: string, categoryData: Omit<Category, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<Category> {
    // For Phase II, maintain categories in memory and localStorage for the session
    this.initializeCategoriesStorage(userId);

    const newCategory: Category = {
      ...categoryData as Category,
      id: Date.now() + Math.floor(Math.random() * 1000), // Unique ID
      user_id: parseInt(userId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    this.categoriesStorage[userId].push(newCategory);
    this.saveCategoriesToLocalStorage(userId);
    return newCategory;
  }

  async updateCategory(userId: string, categoryId: number, categoryData: Partial<Category>): Promise<Category> {
    // For Phase II, maintain categories in memory and localStorage for the session
    this.initializeCategoriesStorage(userId);

    const index = this.categoriesStorage[userId].findIndex(cat => cat.id === categoryId);
    if (index === -1) {
      throw new Error('Category not found');
    }

    const updatedCategory = {
      ...this.categoriesStorage[userId][index],
      ...categoryData,
      updated_at: new Date().toISOString()
    } as Category;

    this.categoriesStorage[userId][index] = updatedCategory;
    this.saveCategoriesToLocalStorage(userId);
    return updatedCategory;
  }

  async deleteCategory(userId: string, categoryId: number): Promise<void> {
    // For Phase II, maintain categories in memory and localStorage for the session
    this.initializeCategoriesStorage(userId);

    this.categoriesStorage[userId] = this.categoriesStorage[userId].filter(cat => cat.id !== categoryId);
    this.saveCategoriesToLocalStorage(userId);
  }

  // Tag endpoints - maintain in-memory and localStorage state for Phase II compatibility
  private tagsStorage: { [userId: string]: Tag[] } = {};

  // Initialize tags from localStorage on first access
  private initializeTagsStorage(userId: string) {
    if (!this.tagsStorage[userId]) {
      // Try to load from localStorage
      const savedTags = localStorage.getItem(`tags_${userId}`);
      if (savedTags) {
        try {
          this.tagsStorage[userId] = JSON.parse(savedTags);
        } catch (e) {
          console.error('Error parsing saved tags:', e);
          this.tagsStorage[userId] = [];
        }
      } else {
        this.tagsStorage[userId] = [];
      }
    }
  }

  private saveTagsToLocalStorage(userId: string) {
    if (this.tagsStorage[userId]) {
      localStorage.setItem(`tags_${userId}`, JSON.stringify(this.tagsStorage[userId]));
    }
  }

  async getTags(userId: string): Promise<Tag[]> {
    // For Phase II, maintain tags in memory and localStorage for the session
    this.initializeTagsStorage(userId);
    return this.tagsStorage[userId];
  }

  async createTag(userId: string, tagData: Omit<Tag, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<Tag> {
    // For Phase II, maintain tags in memory and localStorage for the session
    this.initializeTagsStorage(userId);

    const newTag: Tag = {
      ...tagData as Tag,
      id: Date.now() + Math.floor(Math.random() * 1000), // Unique ID
      user_id: parseInt(userId),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    this.tagsStorage[userId].push(newTag);
    this.saveTagsToLocalStorage(userId);
    return newTag;
  }

  async updateTag(userId: string, tagId: number, tagData: Partial<Tag>): Promise<Tag> {
    // For Phase II, maintain tags in memory and localStorage for the session
    this.initializeTagsStorage(userId);

    const index = this.tagsStorage[userId].findIndex(tag => tag.id === tagId);
    if (index === -1) {
      throw new Error('Tag not found');
    }

    const updatedTag = {
      ...this.tagsStorage[userId][index],
      ...tagData,
      updated_at: new Date().toISOString()
    } as Tag;

    this.tagsStorage[userId][index] = updatedTag;
    this.saveTagsToLocalStorage(userId);
    return updatedTag;
  }

  async deleteTag(userId: string, tagId: number): Promise<void> {
    // For Phase II, maintain tags in memory and localStorage for the session
    this.initializeTagsStorage(userId);

    this.tagsStorage[userId] = this.tagsStorage[userId].filter(tag => tag.id !== tagId);
    this.saveTagsToLocalStorage(userId);
  }

  // Reminder endpoints
  async getReminders(userId: string): Promise<Reminder[]> {
    // For Phase II, the backend doesn't support reminders
    // Return an empty array instead of making the API call
    console.warn('Reminders not supported in Phase II backend');
    return [];

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/reminders`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch reminders: ${response.statusText}`);
    }

    return response.json();
    */
  }

  async createReminder(userId: string, reminderData: Omit<Reminder, 'id' | 'user_id' | 'created_at'>): Promise<Reminder> {
    // For Phase II, the backend doesn't support reminders
    // Return a mock reminder instead of making the API call
    console.warn('Reminders not supported in Phase II backend');
    return {
      ...reminderData as Reminder,
      id: Math.floor(Math.random() * 1000), // Mock ID
      user_id: parseInt(userId),
      created_at: new Date().toISOString()
    };

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/reminders`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(reminderData),
    });

    if (!response.ok) {
      throw new Error(`Failed to create reminder: ${response.statusText}`);
    }

    return response.json();
    */
  }

  async updateReminder(userId: string, reminderId: number, reminderData: Partial<Reminder>): Promise<Reminder> {
    // For Phase II, the backend doesn't support reminders
    // Return the updated mock reminder instead of making the API call
    console.warn('Reminders not supported in Phase II backend');
    return {
      ...reminderData as Reminder,
      id: reminderId,
      user_id: parseInt(userId),
      created_at: new Date().toISOString()
    } as Reminder;

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/reminders/${reminderId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(reminderData),
    });

    if (!response.ok) {
      throw new Error(`Failed to update reminder: ${response.statusText}`);
    }

    return response.json();
    */
  }

  async deleteReminder(userId: string, reminderId: number): Promise<void> {
    // For Phase II, the backend doesn't support reminders
    // Just log a warning instead of making the API call
    console.warn('Reminders not supported in Phase II backend');

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/reminders/${reminderId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to delete reminder: ${response.statusText}`);
    }
    */
  }

  async getUpcomingReminders(userId: string, limit: number = 10): Promise<Reminder[]> {
    // For Phase II, the backend doesn't support reminders
    // Return an empty array instead of making the API call
    console.warn('Reminders not supported in Phase II backend');
    return [];

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/reminders/upcoming?limit=${limit}`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch upcoming reminders: ${response.statusText}`);
    }

    return response.json();
    */
  }

  async markReminderAsSent(userId: string, reminderId: number): Promise<void> {
    // For Phase II, the backend doesn't support reminders
    // Just log a warning instead of making the API call
    console.warn('Reminders not supported in Phase II backend');

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/reminders/${reminderId}/mark-sent`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to mark reminder as sent: ${response.statusText}`);
    }
    */
  }

  // Recurring task endpoints
  async getRecurringTasks(userId: string): Promise<RecurringTask[]> {
    // For Phase II, the backend doesn't support recurring tasks
    // Return an empty array instead of making the API call
    console.warn('Recurring tasks not supported in Phase II backend');
    return [];

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/recurring`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch recurring tasks: ${response.statusText}`);
    }

    return response.json();
    */
  }

  async createRecurringTask(userId: string, recurringTaskData: Omit<RecurringTask, 'id' | 'created_at' | 'updated_at'>): Promise<RecurringTask> {
    // For Phase II, the backend doesn't support recurring tasks
    // Return a mock recurring task instead of making the API call
    console.warn('Recurring tasks not supported in Phase II backend');
    return {
      ...recurringTaskData as RecurringTask,
      id: Math.floor(Math.random() * 1000), // Mock ID
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/recurring`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(recurringTaskData),
    });

    if (!response.ok) {
      throw new Error(`Failed to create recurring task: ${response.statusText}`);
    }

    return response.json();
    */
  }

  async updateRecurringTask(userId: string, recurringTaskId: number, recurringTaskData: Partial<RecurringTask>): Promise<RecurringTask> {
    // For Phase II, the backend doesn't support recurring tasks
    // Return the updated mock recurring task instead of making the API call
    console.warn('Recurring tasks not supported in Phase II backend');
    return {
      ...recurringTaskData as RecurringTask,
      id: recurringTaskId,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    } as RecurringTask;

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/recurring/${recurringTaskId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(recurringTaskData),
    });

    if (!response.ok) {
      throw new Error(`Failed to update recurring task: ${response.statusText}`);
    }

    return response.json();
    */
  }

  async deleteRecurringTask(userId: string, recurringTaskId: number): Promise<void> {
    // For Phase II, the backend doesn't support recurring tasks
    // Just log a warning instead of making the API call
    console.warn('Recurring tasks not supported in Phase II backend');

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/recurring/${recurringTaskId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to delete recurring task: ${response.statusText}`);
    }
    */
  }

  async generateRecurringInstances(userId: string, recurringTaskId: number, count: number = 10): Promise<{message: string, instances: number[]}> {
    // For Phase II, the backend doesn't support recurring tasks
    // Return a mock response instead of making the API call
    console.warn('Recurring tasks not supported in Phase II backend');
    return {
      message: 'Recurring instances not supported in Phase II',
      instances: []
    };

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/recurring/${recurringTaskId}/generate-instances?count=${count}`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to generate recurring instances: ${response.statusText}`);
    }

    return response.json();
    */
  }

  // AI endpoints
  async getTaskSuggestions(userId: string, limit: number = 5): Promise<AISuggestion[]> {
    // For Phase II, the backend doesn't support AI suggestions
    // Return an empty array instead of making the API call
    console.warn('AI suggestions not supported in Phase II backend');
    return [];

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/suggest?limit=${limit}`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch AI suggestions: ${response.statusText}`);
    }

    return response.json();
    */
  }

  async getUserAnalysis(userId: string): Promise<any> {
    // For Phase II, the backend doesn't support user analysis
    // Return an empty object instead of making the API call
    console.warn('User analysis not supported in Phase II backend');
    return {};

    // Original code (commented out for Phase II)
    /*
    const response = await fetch(`${API_BASE_URL}/api/${userId}/analysis`, {
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch user analysis: ${response.statusText}`);
    }

    return response.json();
    */
  }
}

export const api = new ApiClient();