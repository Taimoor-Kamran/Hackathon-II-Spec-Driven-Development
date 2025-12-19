import { NextRequest, NextResponse } from 'next/server';
import { ChatRequest } from '../../../../../chat_endpoint'; // Adjust path as needed

export async function POST(request: NextRequest) {
  try {
    const { user_id, session_id, message } = await request.json();

    // Validate input
    if (!user_id || !session_id || !message) {
      return NextResponse.json(
        { error: 'Missing required fields: user_id, session_id, or message' },
        { status: 400 }
      );
    }

    // Prepare headers with authentication if available
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Check for Authorization header in the incoming request and forward it
    const authHeader = request.headers.get('authorization');
    if (authHeader) {
      headers['Authorization'] = authHeader;
    }

    // Call the backend chat endpoint
    const backendResponse = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        user_id,
        session_id,
        message
      }),
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      throw new Error(`Backend error: ${backendResponse.status} - ${errorText}`);
    }

    const data = await backendResponse.json();

    return NextResponse.json(data);
  } catch (error) {
    console.error('Error processing chat request:', error);

    return NextResponse.json(
      { error: 'Failed to process chat message', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    );
  }
}