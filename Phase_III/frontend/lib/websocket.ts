import { Task, Category, Tag, Reminder, RecurringTask } from '@/types';

interface WebSocketMessage {
  type: string;
  data: any;
  userId?: number;
  timestamp: string;
}

class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectInterval = 5000; // 5 seconds
  private userId: number | null = null;
  private messageHandlers: Array<(message: WebSocketMessage) => void> = [];
  private statusChangeHandlers: Array<(status: 'connected' | 'disconnected' | 'reconnecting') => void> = [];

  connect(userId: number) {
    if (this.ws) {
      this.disconnect();
    }

    this.userId = userId;
    const token = localStorage.getItem('authToken');

    // For Phase II, we'll skip WebSocket connection since backend doesn't support it
    // The backend for Phase II doesn't have WebSocket endpoints
    console.warn('WebSocket connection skipped - backend does not support real-time updates in Phase II');
    return;
  }

  disconnect() {
    // WebSocket not supported in Phase II
    console.warn('WebSocket disconnect called but not supported in Phase II');
  }

  isConnected(): boolean {
    // WebSocket not supported in Phase II
    return false;
  }

  subscribeToMessages(handler: (message: WebSocketMessage) => void) {
    // WebSocket not supported in Phase II - add to handlers anyway for compatibility
    this.messageHandlers.push(handler);
    return () => {
      const index = this.messageHandlers.indexOf(handler);
      if (index > -1) {
        this.messageHandlers.splice(index, 1);
      }
    };
  }

  subscribeToStatusChanges(handler: (status: 'connected' | 'disconnected' | 'reconnecting') => void) {
    // WebSocket not supported in Phase II - add to handlers anyway for compatibility
    this.statusChangeHandlers.push(handler);
    return () => {
      const index = this.statusChangeHandlers.indexOf(handler);
      if (index > -1) {
        this.statusChangeHandlers.splice(index, 1);
      }
    };
  }

  sendMessage(message: any) {
    // WebSocket not supported in Phase II
    console.warn('WebSocket sendMessage called but not supported in Phase II');
  }

  // Handle real-time task updates
  subscribeToTaskUpdates(handler: (task: Task, type: string) => void) {
    // WebSocket not supported in Phase II - return a no-op unsubscribe function
    console.warn('Task updates not supported in Phase II backend');
    return () => {
      // No-op for Phase II compatibility
    };
  }

  // Handle real-time category updates
  subscribeToCategoryUpdates(handler: (category: Category, type: string) => void) {
    // WebSocket not supported in Phase II - return a no-op unsubscribe function
    console.warn('Category updates not supported in Phase II backend');
    return () => {
      // No-op for Phase II compatibility
    };
  }

  // Handle real-time tag updates
  subscribeToTagUpdates(handler: (tag: Tag, type: string) => void) {
    // WebSocket not supported in Phase II - return a no-op unsubscribe function
    console.warn('Tag updates not supported in Phase II backend');
    return () => {
      // No-op for Phase II compatibility
    };
  }

  // Handle real-time reminder updates
  subscribeToReminderUpdates(handler: (reminder: Reminder, type: string) => void) {
    // WebSocket not supported in Phase II - return a no-op unsubscribe function
    console.warn('Reminder updates not supported in Phase II backend');
    return () => {
      // No-op for Phase II compatibility
    };
  }

  // Handle real-time recurring task updates
  subscribeToRecurringTaskUpdates(handler: (recurringTask: RecurringTask, type: string) => void) {
    // WebSocket not supported in Phase II - return a no-op unsubscribe function
    console.warn('Recurring task updates not supported in Phase II backend');
    return () => {
      // No-op for Phase II compatibility
    };
  }

  // Send collaboration event
  sendCollaborationEvent(eventType: string, data: any) {
    // WebSocket not supported in Phase II
    console.warn('WebSocket sendCollaborationEvent called but not supported in Phase II');
  }
}

export const websocketService = new WebSocketService();