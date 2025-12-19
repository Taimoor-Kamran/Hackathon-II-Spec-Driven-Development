import React, { useState } from 'react';
import { SearchFilters } from '@/types';

interface SearchFilterProps {
  onSearch: (filters: SearchFilters) => void;
  userId: string;
}

const SearchFilter: React.FC<SearchFilterProps> = ({ onSearch }) => {
  const [filters, setFilters] = useState<SearchFilters>({
    query: '',
    status: undefined,
    category_id: undefined,
    tag_ids: [],
    due_date_start: '',
    due_date_end: '',
    priority: undefined,
    sort_by: undefined,
    sort_order: 'asc',
  });

  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleInputChange = (field: keyof SearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSearch = () => {
    onSearch(filters);
  };

  const clearFilters = () => {
    const clearedFilters: SearchFilters = {
      query: '',
      status: undefined,
      category_id: undefined,
      tag_ids: [],
      due_date_start: '',
      due_date_end: '',
      priority: undefined,
      sort_by: undefined,
      sort_order: 'asc',
    };
    setFilters(clearedFilters);
    onSearch(clearedFilters);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search Query */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <input
            type="text"
            value={filters.query || ''}
            onChange={(e) => handleInputChange('query', e.target.value)}
            placeholder="Title or description..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            value={filters.status || ''}
            onChange={(e) => handleInputChange('status', e.target.value || undefined)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">All</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        {/* Priority Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
          <select
            value={filters.priority || ''}
            onChange={(e) => handleInputChange('priority', e.target.value || undefined)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">All</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        {/* Sort Options */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
          <select
            value={filters.sort_by || ''}
            onChange={(e) => handleInputChange('sort_by', e.target.value || undefined)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">Default</option>
            <option value="title">Title</option>
            <option value="due_date">Due Date</option>
            <option value="priority">Priority</option>
            <option value="created_at">Created Date</option>
          </select>
        </div>
      </div>

      {/* Advanced Filters Toggle */}
      <div className="mt-4">
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-sm text-indigo-600 hover:text-indigo-900"
        >
          {showAdvanced ? 'Hide' : 'Show'} Advanced Filters
        </button>
      </div>

      {/* Advanced Filters */}
      {showAdvanced && (
        <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Category Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <input
              type="number"
              value={filters.category_id || ''}
              onChange={(e) => handleInputChange('category_id', e.target.value ? parseInt(e.target.value) : undefined)}
              placeholder="Category ID"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          {/* Tag IDs Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tag IDs (comma-separated)</label>
            <input
              type="text"
              value={filters.tag_ids?.join(',') || ''}
              onChange={(e) => {
                const value = e.target.value;
                if (value === '') {
                  handleInputChange('tag_ids', []);
                } else {
                  const tagIds = value.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));
                  handleInputChange('tag_ids', tagIds);
                }
              }}
              placeholder="1,2,3"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          {/* Due Date Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Due Date Start</label>
            <input
              type="date"
              value={filters.due_date_start || ''}
              onChange={(e) => handleInputChange('due_date_start', e.target.value || undefined)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Due Date End</label>
            <input
              type="date"
              value={filters.due_date_end || ''}
              onChange={(e) => handleInputChange('due_date_end', e.target.value || undefined)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          {/* Sort Order */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Sort Order</label>
            <select
              value={filters.sort_order}
              onChange={(e) => handleInputChange('sort_order', e.target.value as 'asc' | 'desc')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="mt-4 flex space-x-3">
        <button
          type="button"
          onClick={handleSearch}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Search
        </button>
        <button
          type="button"
          onClick={clearFilters}
          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
};

export default SearchFilter;