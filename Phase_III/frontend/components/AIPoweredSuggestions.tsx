import React, { useState, useEffect } from 'react';
import { AISuggestion, TaskCreateData } from '@/types';
import { api } from '@/lib/api';
import { websocketService } from '@/lib/websocket';

interface AIPoweredSuggestionsProps {
  userId: string;
  onSuggestionAccept: (suggestion: TaskCreateData) => void;
  limit?: number;
}

const AIPoweredSuggestions: React.FC<AIPoweredSuggestionsProps> = ({
  userId,
  onSuggestionAccept,
  limit = 3
}) => {
  const [suggestions, setSuggestions] = useState<AISuggestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSuggestions();
  }, [userId]);

  const loadSuggestions = async () => {
    try {
      setLoading(true);
      setError(null);
      const suggestionsData = await api.getTaskSuggestions(userId, limit);
      setSuggestions(suggestionsData);
    } catch (err) {
      console.error('Error loading AI suggestions:', err);
      setError('Failed to load suggestions');
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptSuggestion = (suggestion: AISuggestion) => {
    const taskData: TaskCreateData = {
      title: suggestion.title,
      description: suggestion.description || undefined,
      category_id: suggestion.category_id || undefined,
      due_date: suggestion.due_date || undefined,
      priority: suggestion.priority,
    };
    onSuggestionAccept(taskData);
  };

  if (loading) {
    return (
      <div className="p-4 bg-gray-50 rounded-lg">
        <h3 className="text-md font-medium text-gray-900 mb-2">AI Suggestions</h3>
        <p className="text-sm text-gray-500">Loading smart suggestions...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 rounded-lg border border-red-200">
        <h3 className="text-md font-medium text-red-900 mb-2">AI Suggestions</h3>
        <p className="text-sm text-red-700">{error}</p>
        <button
          onClick={loadSuggestions}
          className="mt-2 text-sm text-red-600 hover:text-red-800"
        >
          Try again
        </button>
      </div>
    );
  }

  if (suggestions.length === 0) {
    return (
      <div className="p-4 bg-gray-50 rounded-lg">
        <h3 className="text-md font-medium text-gray-900 mb-2">AI Suggestions</h3>
        <p className="text-sm text-gray-500">No suggestions available. Complete more tasks to improve AI recommendations.</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
      <h3 className="text-md font-medium text-blue-900 mb-3">AI-Powered Suggestions</h3>
      <div className="space-y-3">
        {suggestions.map((suggestion) => (
          <div key={suggestion.id} className="flex items-start justify-between p-3 bg-white rounded border border-blue-100">
            <div className="flex-1 min-w-0">
              <h4 className="font-medium text-gray-900 truncate">{suggestion.title}</h4>
              {suggestion.description && (
                <p className="text-sm text-gray-500 mt-1 line-clamp-2">{suggestion.description}</p>
              )}
              <div className="flex flex-wrap gap-1 mt-2">
                {suggestion.category && (
                  <span
                    className="px-2 py-1 text-xs rounded-full"
                    style={{
                      backgroundColor: `${suggestion.category.color}20`,
                      color: suggestion.category.color,
                      border: `1px solid ${suggestion.category.color}`
                    }}
                  >
                    {suggestion.category.name}
                  </span>
                )}
                {suggestion.tags.map(tag => (
                  <span key={tag.id} className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full">
                    #{tag.name}
                  </span>
                ))}
                {suggestion.due_date && (
                  <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded-full">
                    📅 {new Date(suggestion.due_date).toLocaleDateString()}
                  </span>
                )}
              </div>
            </div>
            <button
              type="button"
              className="ml-3 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
              onClick={() => handleAcceptSuggestion(suggestion)}
            >
              Use
            </button>
          </div>
        ))}
      </div>
      <button
        onClick={loadSuggestions}
        className="mt-3 text-sm text-blue-600 hover:text-blue-800"
      >
        Refresh Suggestions
      </button>
    </div>
  );
};

export default AIPoweredSuggestions;