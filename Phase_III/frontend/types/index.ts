// Base types
export interface User {
  id: number;
  email: string;
  name: string | null;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  user_id: number;
  name: string;
  color: string;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: number;
  user_id: number;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface Reminder {
  id: number;
  task_id: number;
  user_id: number;
  reminder_time: string; // ISO date string
  sent: boolean;
  created_at: string;
}

export interface RecurringTask {
  id: number;
  original_task_id: number;
  recurrence_pattern: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval: number;
  end_date: string | null; // ISO date string
  created_at: string;
  updated_at: string;
}

// Task types
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  completed: boolean;
  category_id: number | null;
  due_date: string | null; // ISO date string
  priority: 'low' | 'medium' | 'high';
  created_at: string;
  updated_at: string;
  category?: Category | null;
  tags: Tag[];
}

export interface TaskCreateData {
  title: string;
  description?: string;
  completed?: boolean;
  category_id?: number;
  due_date?: string; // ISO date string
  priority?: 'low' | 'medium' | 'high';
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
  category_id?: number;
  due_date?: string; // ISO date string
  priority?: 'low' | 'medium' | 'high';
}

// API response types
export interface TaskResponse extends Task {}
export interface CategoryResponse extends Category {}
export interface TagResponse extends Tag {}
export interface ReminderResponse extends Reminder {}
export interface RecurringTaskResponse extends RecurringTask {}

// Search and filter types
export interface SearchFilters {
  query?: string;
  status?: 'pending' | 'completed';
  category_id?: number;
  tag_ids?: number[];
  due_date_start?: string;
  due_date_end?: string;
  priority?: 'low' | 'medium' | 'high';
  sort_by?: 'title' | 'due_date' | 'priority' | 'created_at';
  sort_order?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}

// WebSocket message types
export interface WebSocketMessage {
  type: string;
  task?: Task;
  task_id?: number;
  timestamp: string;
}

// AI suggestion types
export interface AISuggestion {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  user_id: number;
  category_id: number | null;
  due_date: string | null;
  priority: 'low' | 'medium' | 'high';
  created_at: string;
  updated_at: string;
  category: Category | null;
  tags: Tag[];
}