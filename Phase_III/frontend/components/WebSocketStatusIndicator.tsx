'use client';

import React, { useEffect, useState } from 'react';
import { websocketService } from '@/lib/websocket';

const WebSocketStatusIndicator = () => {
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'reconnecting'>('disconnected');

  useEffect(() => {
    const unsubscribe = websocketService.subscribeToStatusChanges(setStatus);
    return unsubscribe;
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case 'connected':
        return 'bg-green-500';
      case 'reconnecting':
        return 'bg-yellow-500';
      case 'disconnected':
      default:
        return 'bg-red-500';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected':
        return 'Connected';
      case 'reconnecting':
        return 'Reconnecting...';
      case 'disconnected':
      default:
        return 'Disconnected';
    }
  };

  return (
    <div className="flex items-center space-x-2 text-sm">
      <div className={`w-3 h-3 rounded-full ${getStatusColor()} animate-pulse`}></div>
      <span className="text-gray-600">{getStatusText()}</span>
    </div>
  );
};

export default WebSocketStatusIndicator;