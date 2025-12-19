import React, { useState, useEffect } from 'react';
import { Category } from '@/types';
import { api } from '@/lib/api';
import { websocketService } from '@/lib/websocket';

interface CategoryManagerProps {
  userId: string;
  selectedCategoryId?: number | null;
  onSelectCategory?: (categoryId: number | null) => void;
  showSelector?: boolean;
  showManager?: boolean;
}

const CategoryManager: React.FC<CategoryManagerProps> = ({
  userId,
  selectedCategoryId,
  onSelectCategory,
  showSelector = true,
  showManager = true
}) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [newCategoryName, setNewCategoryName] = useState('');
  const [newCategoryColor, setNewCategoryColor] = useState('#000000');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCategories();

    // Subscribe to category updates
    const unsubscribe = websocketService.subscribeToCategoryUpdates((category, type) => {
      if (type === 'category_create' || type === 'collaboration_category_create') {
        setCategories(prev => [...prev, category]);
      } else if (type === 'category_update' || type === 'collaboration_category_update') {
        setCategories(prev =>
          prev.map(cat => cat.id === category.id ? category : cat)
        );
      } else if (type === 'category_delete' || type === 'collaboration_category_delete') {
        setCategories(prev => prev.filter(cat => cat.id !== category.id));
        if (selectedCategoryId === category.id && onSelectCategory) {
          onSelectCategory(null);
        }
      }
    });

    return () => {
      unsubscribe();
    };
  }, [userId, selectedCategoryId, onSelectCategory]);

  const loadCategories = async () => {
    try {
      setLoading(true);
      const categoriesData = await api.getCategories(userId);
      setCategories(categoriesData);
      setError(null);
    } catch (err) {
      console.error('Error loading categories:', err);
      setError('Failed to load categories');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCategory = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCategoryName.trim()) return;

    try {
      const newCategory = await api.createCategory(userId, {
        name: newCategoryName.trim(),
        color: newCategoryColor
      });

      // Send collaboration event
      websocketService.sendCollaborationEvent('category_create', newCategory);

      setNewCategoryName('');
      setNewCategoryColor('#000000');
    } catch (err) {
      console.error('Error creating category:', err);
      setError('Failed to create category');
    }
  };

  const handleDeleteCategory = async (categoryId: number) => {
    if (!window.confirm('Are you sure you want to delete this category?')) {
      return;
    }

    try {
      await api.deleteCategory(userId, categoryId);
      // Directly update the state since WebSocket is not supported in Phase II
      setCategories(prev => prev.filter(cat => cat.id !== categoryId));
      if (selectedCategoryId === categoryId && onSelectCategory) {
        onSelectCategory(null);
      }
      // Send collaboration event for compatibility (though it won't do anything in Phase II)
      websocketService.sendCollaborationEvent('category_delete', { id: categoryId });
    } catch (err) {
      console.error('Error deleting category:', err);
      setError('Failed to delete category');
    }
  };

  const handleCategorySelect = (categoryId: number | null) => {
    if (onSelectCategory) {
      onSelectCategory(categoryId);
    }
  };

  if (loading && showSelector) {
    return <div>Loading categories...</div>;
  }

  return (
    <div className="space-y-4">
      {showSelector && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              className={`px-3 py-1 rounded-full text-sm ${
                selectedCategoryId === null
                  ? 'bg-gray-200 text-gray-800'
                  : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
              onClick={() => handleCategorySelect(null)}
            >
              No Category
            </button>
            {categories.map((category) => (
              <div key={category.id} className="flex items-center group">
                <button
                  type="button"
                  className={`px-3 py-1 rounded-full text-sm flex items-center ${
                    selectedCategoryId === category.id
                      ? 'text-white'
                      : 'bg-white border text-gray-700 hover:bg-gray-50'
                  }`}
                  style={{
                    backgroundColor: selectedCategoryId === category.id ? category.color : undefined,
                    borderColor: category.color
                  }}
                  onClick={() => handleCategorySelect(category.id)}
                >
                  {category.name}
                </button>
                <button
                  type="button"
                  className="ml-1 text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => handleDeleteCategory(category.id)}
                  title="Delete category"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {showManager && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Manage Categories</h3>

          {error && (
            <div className="mb-3 p-2 bg-red-100 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleCreateCategory} className="flex flex-col sm:flex-row gap-2 mb-3">
            <input
              type="text"
              value={newCategoryName}
              onChange={(e) => setNewCategoryName(e.target.value)}
              placeholder="New category name"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              maxLength={50}
            />
            <input
              type="color"
              value={newCategoryColor}
              onChange={(e) => setNewCategoryColor(e.target.value)}
              className="w-12 h-10 border border-gray-300 rounded cursor-pointer"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Add Category
            </button>
          </form>

          <div className="space-y-2">
            {categories.map((category) => (
              <div key={category.id} className="flex items-center justify-between p-2 bg-white rounded border">
                <div className="flex items-center">
                  <div
                    className="w-4 h-4 rounded-full mr-2 border border-gray-300"
                    style={{ backgroundColor: category.color }}
                  ></div>
                  <span>{category.name}</span>
                </div>
                <button
                  type="button"
                  className="text-red-500 hover:text-red-700"
                  onClick={() => handleDeleteCategory(category.id)}
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CategoryManager;