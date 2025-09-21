<!-- src/routes/(app)/profile/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { user } from '$lib/stores/auth';
	import { getTickets } from '$lib/api/tickets';
	import type { User, Ticket } from '$lib/api/tickets';
	
	let assignedTickets = $state<Ticket[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);

	async function loadUserTickets() {
		try {
			loading = true;
			error = null;
			
			const ticketsResponse = await getTickets();
			// Filter tickets assigned to current user
			assignedTickets = ticketsResponse.results.filter(
				ticket => ticket.assigned_to?.id === $user?.id
			);
			
		} catch (err) {
			console.error('Failed to load user tickets:', err);
			error = 'Failed to load tickets';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		loadUserTickets();
	});
</script>

<div class="profile-page">
	<div class="profile-header">
		<h1>User Profile</h1>
	</div>

	{#if $user}
		<!-- User Information Card -->
		<div class="profile-card">
			<div class="user-avatar">
				<div class="avatar-circle">
					{$user.first_name[0]}{$user.last_name[0]}
				</div>
			</div>
			
			<div class="user-details">
				<h2>{$user.first_name} {$user.last_name}</h2>
				<p class="username">@{$user.username}</p>
				<p class="email">{$user.email}</p>
				{#if $user.role}
					<p class="role">Role: {$user.role}</p>
				{/if}
			</div>
		</div>

		<!-- Assigned Tickets Section -->
		<div class="tickets-section">
			<h3>My Assigned Tickets ({assignedTickets.length})</h3>
			
			{#if loading}
				<div class="loading">
					<div class="loading-spinner"></div>
					<p>Loading tickets...</p>
				</div>
			{:else if error}
				<div class="error">
					<p>{error}</p>
				</div>
			{:else if assignedTickets.length === 0}
				<div class="empty-state">
					<p>No tickets assigned to you</p>
				</div>
			{:else}
				<div class="tickets-grid">
					{#each assignedTickets as ticket}
						<div class="ticket-card">
							<div class="ticket-header">
								<h4>{ticket.title}</h4>
								<span class="priority-badge priority-{ticket.priority}">
									{ticket.priority}
								</span>
							</div>
							<p class="ticket-description">{ticket.description}</p>
							<div class="ticket-footer">
								<span class="status-badge status-{ticket.status}">
									{ticket.status.replace('_', ' ')}
								</span>
								<span class="ticket-date">
									{new Date(ticket.created_at).toLocaleDateString()}
								</span>
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	{:else}
		<div class="error">
			<p>Please log in to view your profile</p>
		</div>
	{/if}
</div>

<style>
	.profile-page {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
	}

	.profile-header h1 {
		font-size: 2rem;
		font-weight: 600;
		color: #1e293b;
		margin-bottom: 2rem;
	}

	.profile-card {
		background: white;
		border-radius: 12px;
		padding: 2rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		border: 1px solid #e2e8f0;
		display: flex;
		align-items: center;
		gap: 2rem;
		margin-bottom: 3rem;
	}

	.user-avatar {
		flex-shrink: 0;
	}

	.avatar-circle {
		width: 80px;
		height: 80px;
		border-radius: 50%;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		font-size: 1.5rem;
		font-weight: 600;
	}

	.user-details h2 {
		font-size: 1.5rem;
		font-weight: 600;
		color: #1e293b;
		margin: 0 0 0.5rem 0;
	}

	.username {
		color: #64748b;
		margin: 0 0 0.25rem 0;
		font-weight: 500;
	}

	.email {
		color: #64748b;
		margin: 0;
	}

	.role {
		color: #667eea;
		margin: 0.25rem 0 0 0;
		font-weight: 500;
		font-size: 0.875rem;
	}

	.tickets-section h3 {
		font-size: 1.25rem;
		font-weight: 600;
		color: #1e293b;
		margin-bottom: 1.5rem;
	}

	.loading, .error, .empty-state {
		text-align: center;
		padding: 2rem;
		color: #64748b;
	}

	.loading-spinner {
		width: 30px;
		height: 30px;
		border: 3px solid #e2e8f0;
		border-top: 3px solid #667eea;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto 1rem;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.tickets-grid {
		display: grid;
		gap: 1rem;
	}

	.ticket-card {
		background: white;
		border-radius: 8px;
		padding: 1.5rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		border: 1px solid #e2e8f0;
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}

	.ticket-card:hover {
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.ticket-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 0.75rem;
	}

	.ticket-header h4 {
		font-size: 1rem;
		font-weight: 600;
		color: #1e293b;
		margin: 0;
		flex: 1;
	}

	.ticket-description {
		color: #64748b;
		margin-bottom: 1rem;
		font-size: 0.875rem;
		line-height: 1.5;
	}

	.ticket-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.priority-badge, .status-badge {
		padding: 0.25rem 0.5rem;
		border-radius: 6px;
		font-size: 0.75rem;
		font-weight: 500;
		text-transform: capitalize;
	}

	.priority-badge.priority-high { background: #fef2f2; color: #dc2626; }
	.priority-badge.priority-medium { background: #fef3c7; color: #d97706; }
	.priority-badge.priority-low { background: #f0fdf4; color: #16a34a; }

	.status-badge.status-open { background: #fef2f2; color: #dc2626; }
	.status-badge.status-in_progress { background: #fef3c7; color: #d97706; }
	.status-badge.status-closed { background: #f0fdf4; color: #16a34a; }

	.ticket-date {
		font-size: 0.75rem;
		color: #94a3b8;
	}

	/* Mobile responsiveness */
	@media (max-width: 768px) {
		.profile-page {
			padding: 1rem;
		}

		.profile-card {
			flex-direction: column;
			text-align: center;
			gap: 1.5rem;
		}

		.ticket-header {
			flex-direction: column;
			align-items: flex-start;
			gap: 0.5rem;
		}

		.ticket-footer {
			flex-direction: column;
			align-items: flex-start;
			gap: 0.5rem;
		}
	}
</style>