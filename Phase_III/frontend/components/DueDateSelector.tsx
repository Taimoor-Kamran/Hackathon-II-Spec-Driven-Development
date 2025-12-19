import React, { useState } from 'react';

interface DueDateSelectorProps {
  selectedDate: string | null;
  onSelectDate: (date: string | null) => void;
  showTime?: boolean;
}

const DueDateSelector: React.FC<DueDateSelectorProps> = ({
  selectedDate,
  onSelectDate,
  showTime = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [customDate, setCustomDate] = useState(selectedDate || '');

  const quickOptions = [
    { label: 'No due date', value: null },
    { label: 'Today', value: new Date().toISOString().split('T')[0] },
    { label: 'Tomorrow', value: new Date(Date.now() + 86400000).toISOString().split('T')[0] },
    { label: 'Next week', value: new Date(Date.now() + 7 * 86400000).toISOString().split('T')[0] },
    { label: 'Next month', value: new Date(new Date().setMonth(new Date().getMonth() + 1)).toISOString().split('T')[0] },
  ];

  const handleQuickSelect = (value: string | null) => {
    onSelectDate(value);
    setIsOpen(false);
  };

  const handleCustomDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCustomDate(e.target.value);
  };

  const handleSaveCustomDate = () => {
    onSelectDate(customDate);
    setIsOpen(false);
  };

  const formatDateDisplay = (dateString: string | null) => {
    if (!dateString) return 'No due date';

    const date = new Date(dateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return 'Tomorrow';
    } else {
      return date.toLocaleDateString();
    }
  };

  return (
    <div className="relative">
      <button
        type="button"
        className={`w-full px-3 py-2 text-left rounded-md border ${
          selectedDate
            ? 'border-green-500 bg-green-50 text-green-700'
            : 'border-gray-300 hover:bg-gray-50 text-gray-700'
        }`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center justify-between">
          <span>{formatDateDisplay(selectedDate)}</span>
          <svg
            className={`w-5 h-5 ml-2 transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {isOpen && (
        <div className="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md border border-gray-200 py-2">
          <div className="px-4 py-2 border-b border-gray-100">
            <h3 className="text-sm font-medium text-gray-900">Due Date</h3>
          </div>

          <div className="py-1">
            {quickOptions.map((option) => (
              <button
                key={option.label}
                type="button"
                className={`w-full text-left px-4 py-2 text-sm ${
                  selectedDate === option.value
                    ? 'bg-blue-100 text-blue-900'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
                onClick={() => handleQuickSelect(option.value)}
              >
                {option.label}
              </button>
            ))}
          </div>

          <div className="px-4 py-3 border-t border-gray-100">
            <div className="flex items-center mb-2">
              <input
                type={showTime ? "datetime-local" : "date"}
                value={customDate}
                onChange={handleCustomDateChange}
                className="flex-1 px-3 py-1 border border-gray-300 rounded text-sm"
              />
            </div>
            <button
              type="button"
              className="w-full px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
              onClick={handleSaveCustomDate}
            >
              Set Date
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DueDateSelector;