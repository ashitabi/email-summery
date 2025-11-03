export interface Message {
  id: string;
  sender: 'customer' | 'company';
  timestamp: string;
  body: string;
}

export interface Thread {
  thread_id: string;
  topic: string;
  subject: string;
  initiated_by: 'customer' | 'company';
  order_id: string;
  product: string;
  messages: Message[];
}

export interface ThreadsData {
  version: string;
  generated_at: string;
  description: string;
  threads: Thread[];
}

export interface ThreadSummary {
  thread_id: string;
  order_id: string;
  product: string;
  issue_category: string;
  summary: string;
  sentiment: 'positive' | 'neutral' | 'negative' | 'frustrated';
  status: 'pending' | 'in_progress' | 'resolved' | 'unresolved';
  action_items: string[];
  priority: 'low' | 'medium' | 'high';
  isApproved?: boolean;
  isEdited?: boolean;
}

export interface ThreadWithSummary extends Thread {
  summary?: ThreadSummary;
}
