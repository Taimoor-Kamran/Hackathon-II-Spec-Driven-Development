'use client';

import React from 'react';
import WebSocketStatusIndicator from '../components/WebSocketStatusIndicator';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/navigation';

// Create a separate component for the authenticated layout to access the Auth context
export default function ClientLayoutWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}