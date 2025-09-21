// lib/api/dashboard.ts
import { env } from '$env/dynamic/public';

export interface DashboardSummary {
	total_tickets: number;
	open_tickets: number;
	in_progress_tickets: number;
	closed_tickets: number;
	high_priority_tickets: number;
	unassigned_tickets: number;
}

export interface StatusStats {
	status_distribution: {
		[key: string]: number;
	};
	total_tickets: number;
}

export interface PriorityStats {
	priority_distribution: {
		[key: string]: number;
	};
	total_tickets: number;
}

const API_BASE = `${env.PUBLIC_API_BASE_URL}/dashboard`;

export async function getDashboardSummary(): Promise<DashboardSummary> {
	const response = await fetch(`${API_BASE}/summary/`, {
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	if (!response.ok) {
		throw new Error(`Failed to fetch dashboard summary: ${response.statusText}`);
	}

	return response.json();
}

export async function getTicketStatusStats(): Promise<StatusStats> {
	const response = await fetch(`${API_BASE}/status-stats/`, {
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	if (!response.ok) {
		throw new Error(`Failed to fetch status stats: ${response.statusText}`);
	}

	return response.json();
}

export async function getTicketPriorityStats(): Promise<PriorityStats> {
	const response = await fetch(`${API_BASE}/priority-stats/`, {
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	if (!response.ok) {
		throw new Error(`Failed to fetch priority stats: ${response.statusText}`);
	}

	return response.json();
}
