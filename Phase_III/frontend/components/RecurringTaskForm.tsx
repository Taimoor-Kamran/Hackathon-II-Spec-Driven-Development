import React, { useState } from 'react';
import { RecurringTask } from '@/types';

interface RecurringTaskFormProps {
  taskTitle: string;
  onSetRecurring: (recurringData: Omit<RecurringTask, 'id' | 'original_task_id' | 'created_at' | 'updated_at'>) => void;
  onCancel: () => void;
}

const RecurringTaskForm: React.FC<RecurringTaskFormProps> = ({
  taskTitle,
  onSetRecurring,
  onCancel
}) => {
  const [pattern, setPattern] = useState<'daily' | 'weekly' | 'monthly' | 'yearly'>('daily');
  const [interval, setInterval] = useState(1);
  const [endDate, setEndDate] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (interval < 1) {
      setError('Interval must be at least 1');
      return;
    }

    const recurringData = {
      recurrence_pattern: pattern,
      interval,
      end_date: endDate || null,
    };

    onSetRecurring(recurringData);
  };

  const patternOptions = [
    { value: 'daily', label: 'Daily' },
    { value: 'weekly', label: 'Weekly' },
    { value: 'monthly', label: 'Monthly' },
    { value: 'yearly', label: 'Yearly' },
  ];

  return (
    <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
      <h3 className="text-lg font-medium text-blue-900 mb-3">
        Set Recurring Pattern for: "{taskTitle}"
      </h3>

      {error && (
        <div className="mb-3 p-2 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Recurrence Pattern
          </label>
          <select
            value={pattern}
            onChange={(e) => setPattern(e.target.value as any)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            {patternOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Every
          </label>
          <div className="flex items-center">
            <input
              type="number"
              min="1"
              value={interval}
              onChange={(e) => setInterval(Math.max(1, parseInt(e.target.value) || 1))}
              className="w-20 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
            <span className="ml-2 text-gray-700">
              {pattern === 'daily' && 'day(s)'}
              {pattern === 'weekly' && 'week(s)'}
              {pattern === 'monthly' && 'month(s)'}
              {pattern === 'yearly' && 'year(s)'}
            </span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            End Date (optional)
          </label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
          <p className="mt-1 text-xs text-gray-500">
            Leave blank for no end date
          </p>
        </div>

        <div className="flex space-x-3 pt-2">
          <button
            type="submit"
            className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Set Recurring
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default RecurringTaskForm;