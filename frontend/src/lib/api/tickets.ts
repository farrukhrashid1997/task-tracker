// frontend/src/lib/api/tickets.ts
import { env } from '$env/dynamic/public';

export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
export type TicketsResponse = PaginatedResponse<Ticket>;


export interface Comment {
  id: number;
  ticket: number;
  user: number;
  content: string;
  created_at: string;
  author?: User;
}

export interface Ticket {
  id: number;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  status: 'open' | 'in_progress' | 'closed';
  assigned_to?: User;
  created_by: User;
  created_at: string;
  updated_at: string;
  comments?: Comment[];
}

export interface CreateTicketData {
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  status: 'open' | 'in_progress' | 'closed';
  assigned_to_id: number | null;
}

export interface UpdateTicketData extends Partial<CreateTicketData> {}

export interface CreateCommentData {
  content: string;
}

const API_BASE = `${env.PUBLIC_API_BASE_URL}/tickets`;

export async function getTickets(): Promise<TicketsResponse> {
  const response = await fetch(`${API_BASE}/`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch tickets: ${response.statusText}`);
  }

  return response.json();
}

export async function getTicket(id: number): Promise<Ticket> {
  const response = await fetch(`${API_BASE}/${id}/`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch ticket: ${response.statusText}`);
  }

  return response.json();
}

export async function createTicket(data: CreateTicketData): Promise<Ticket> {
  const response = await fetch(`${API_BASE}/create/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Failed to create ticket: ${response.statusText}`);
  }

  return response.json();
}

export async function updateTicket(id: number, data: UpdateTicketData): Promise<Ticket> {
  const response = await fetch(`${API_BASE}/${id}/update/`, {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Failed to update ticket: ${response.statusText}`);
  }

  return response.json();
}

export async function deleteTicket(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/${id}/delete/`, {
    method: 'DELETE',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to delete ticket: ${response.statusText}`);
  }
}

export async function createComment(ticketId: number, data: CreateCommentData): Promise<Comment> {
  const response = await fetch(`${API_BASE}/${ticketId}/comments/`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Failed to create comment: ${response.statusText}`);
  }

  return response.json();
}

export async function getUsers(): Promise<PaginatedResponse<User>> {
  const response = await fetch(`${API_BASE}/users/`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch users: ${response.statusText}`);
  }

  return response.json();
}