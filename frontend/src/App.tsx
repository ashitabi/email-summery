import { useState, useEffect } from 'react';
import './App.css';
import ThreadList from './components/ThreadList';
import ThreadDetail from './components/ThreadDetail';
import { Thread, ThreadWithSummary, ThreadSummary } from './types/thread';

function App() {
  const [threads, setThreads] = useState<ThreadWithSummary[]>([]);
  const [selectedThread, setSelectedThread] = useState<ThreadWithSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load threads data from backend API
    fetch('http://localhost:8000/api/threads')
      .then(response => {
        if (!response.ok) {
          throw new Error(`API error: ${response.statusText}`);
        }
        return response.json();
      })
      .then(data => {
        setThreads(data.threads);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading threads:', error);
        alert('Failed to load threads. Please make sure the backend is running on port 8000.');
        setLoading(false);
      });
  }, []);

  const handleThreadSelect = (thread: Thread) => {
    setSelectedThread(thread);
  };

  const handleSummaryUpdate = (threadId: string, summary: ThreadSummary) => {
    setThreads(prevThreads =>
      prevThreads.map(thread =>
        thread.thread_id === threadId
          ? { ...thread, summary: { ...summary, isEdited: true } }
          : thread
      )
    );

    if (selectedThread?.thread_id === threadId) {
      setSelectedThread({ ...selectedThread, summary: { ...summary, isEdited: true } });
    }
  };

  const handleSummaryApprove = (threadId: string) => {
    setThreads(prevThreads =>
      prevThreads.map(thread =>
        thread.thread_id === threadId && thread.summary
          ? { ...thread, summary: { ...thread.summary, isApproved: true } }
          : thread
      )
    );

    if (selectedThread?.thread_id === threadId && selectedThread.summary) {
      setSelectedThread({
        ...selectedThread,
        summary: { ...selectedThread.summary, isApproved: true }
      });
    }
  };

  const handleGenerateSummary = async (threadId: string) => {
    const thread = threads.find(t => t.thread_id === threadId);
    if (!thread) return;

    try {
      // Call backend API to generate real AI summary
      const response = await fetch('http://localhost:8000/api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ thread }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      const apiSummary = data.summary;

      // Add UI-specific flags
      const summary: ThreadSummary = {
        ...apiSummary,
        isApproved: false,
        isEdited: false
      };

      setThreads(prevThreads =>
        prevThreads.map(t =>
          t.thread_id === threadId ? { ...t, summary } : t
        )
      );

      if (selectedThread?.thread_id === threadId) {
        setSelectedThread({ ...selectedThread, summary });
      }
    } catch (error) {
      console.error('Error generating summary:', error);
      alert('Failed to generate summary. Please make sure the backend is running on port 8000.');
    }
  };

  if (loading) {
    return <div className="loading">Loading threads...</div>;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>CE Email Summarization Tool</h1>
        <p>AI-powered customer email thread analysis and summarization</p>
      </header>

      <div className="app-content">
        <aside className="sidebar">
          <ThreadList
            threads={threads}
            selectedThreadId={selectedThread?.thread_id}
            onThreadSelect={handleThreadSelect}
          />
        </aside>

        <main className="main-content">
          {selectedThread ? (
            <ThreadDetail
              thread={selectedThread}
              onSummaryUpdate={handleSummaryUpdate}
              onSummaryApprove={handleSummaryApprove}
              onGenerateSummary={handleGenerateSummary}
            />
          ) : (
            <div className="empty-state">
              <h2>Select a thread to view details</h2>
              <p>Choose an email thread from the left panel to start reviewing</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
