<!-- frontend/src/routes/tickets/[id]/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { Button, TextArea, Tag } from 'carbon-components-svelte';
	import { ArrowLeft, Edit } from 'carbon-icons-svelte';

	import { getTicket, createComment, type Ticket, type Comment } from '$lib/api/tickets';

	let ticket: Ticket | null = null;
	let newCommentContent = '';
	let ticketId: number;

	const priorityColors: Record<string, string> = {
		Low: 'green',
		Medium: 'yellow',
		High: 'red'
	};

	const statusColors: Record<string, string> = {
		Open: 'blue',
		'In Progress': 'purple',
		Closed: 'gray'
	};

	onMount(async () => {
		ticketId = parseInt($page.params.id);
		ticket = await getTicket(ticketId);
	});

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}

	function goBack(): void {
		goto('/tickets');
	}

	function goToEdit(): void {
		goto(`/tickets/${ticketId}/edit`);
	}

	async function handleCreateComment(): Promise<void> {
		if (!newCommentContent.trim()) return;

		await createComment(ticketId, { content: newCommentContent });
		newCommentContent = '';
		ticket = await getTicket(ticketId);
	}
</script>

<svelte:head>
	<title>Ticket #{ticketId} - Ticket Management</title>
</svelte:head>

<div class="ticket-detail-page">
	<div class="header">
		<Button kind="ghost" icon={ArrowLeft} on:click={goBack}>Back to Tickets</Button>
		{#if ticket}
			<Button kind="primary" icon={Edit} on:click={goToEdit}>Edit Ticket</Button>
		{/if}
	</div>

	{#if ticket}
		<div class="ticket-info">
			<div class="ticket-header">
				<h1>#{ticket.id} - {ticket.title}</h1>
				<div class="tags">
					<Tag type={priorityColors[ticket.priority] as any}>{ticket.priority}</Tag>
					<Tag type={statusColors[ticket.status] as any}>{ticket.status}</Tag>
				</div>
			</div>

			<div class="ticket-meta">
				<div class="meta-item">
					<strong>Created by:</strong>
					{ticket.created_by.first_name}
					{ticket.created_by.last_name} ({ticket.created_by.username})
				</div>
				<div class="meta-item">
					<strong>Assigned to:</strong>
					{#if ticket.assigned_to}
						{ticket.assigned_to.first_name}
						{ticket.assigned_to.last_name} ({ticket.assigned_to.username})
					{:else}
						Unassigned
					{/if}
				</div>
				<div class="meta-item">
					<strong>Created:</strong>
					{formatDate(ticket.created_at)}
				</div>
				<div class="meta-item">
					<strong>Updated:</strong>
					{formatDate(ticket.updated_at)}
				</div>
			</div>

			<div class="ticket-description">
				<h3>Description</h3>
				<p>{ticket.description}</p>
			</div>
		</div>

		<div class="comments-section">
			<h3>Comments ({ticket.comments?.length || 0})</h3>

			<div class="add-comment">
				<TextArea placeholder="Add a comment..." bind:value={newCommentContent} rows={3} />
				<Button kind="primary" on:click={handleCreateComment} disabled={!newCommentContent.trim()}>
					Add Comment
				</Button>
			</div>

			<div class="comments-list">
				{#each ticket.comments || [] as comment}
					<div class="comment">
						<div class="comment-header">
							<strong>{comment.author.first_name} {comment.author.last_name}</strong>
							<span class="comment-date">{formatDate(comment.created_at)}</span>
						</div>
						<p class="comment-content">{comment.content}</p>
					</div>
				{/each}
			</div>
		</div>
	{:else}
		<div class="loading">Loading ticket...</div>
	{/if}
</div>

<style>
	.ticket-detail-page {
		padding: 2rem;
		max-width: 800px;
		margin: 0 auto;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
	}

	.ticket-info {
		background: white;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		padding: 2rem;
		margin-bottom: 2rem;
	}

	.ticket-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 1.5rem;
	}

	.ticket-header h1 {
		margin: 0;
		font-size: 1.75rem;
		font-weight: 600;
		color: #161616;
	}

	.tags {
		display: flex;
		gap: 0.5rem;
	}

	.ticket-meta {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1rem;
		margin-bottom: 1.5rem;
		padding: 1rem;
		background: #f4f4f4;
		border-radius: 4px;
	}

	.meta-item {
		font-size: 0.875rem;
		color: #525252;
	}

	.meta-item strong {
		color: #161616;
	}

	.ticket-description h3 {
		margin: 0 0 1rem 0;
		font-size: 1.25rem;
		color: #161616;
	}

	.ticket-description p {
		margin: 0;
		line-height: 1.6;
		color: #393939;
	}

	.comments-section {
		background: white;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		padding: 2rem;
	}

	.comments-section h3 {
		margin: 0 0 1.5rem 0;
		font-size: 1.25rem;
		color: #161616;
	}

	.add-comment {
		margin-bottom: 2rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.comments-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.comment {
		border: 1px solid #e0e0e0;
		border-radius: 4px;
		padding: 1rem;
		background: #f9f9f9;
	}

	.comment-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.5rem;
	}

	.comment-header strong {
		color: #161616;
		font-size: 0.875rem;
	}

	.comment-date {
		color: #6f6f6f;
		font-size: 0.75rem;
	}

	.comment-content {
		margin: 0;
		color: #393939;
		line-height: 1.5;
	}

	.loading {
		text-align: center;
		padding: 4rem 2rem;
		color: #6f6f6f;
		font-size: 1rem;
	}

	@media (max-width: 768px) {
		.ticket-detail-page {
			padding: 1rem;
		}

		.ticket-header {
			flex-direction: column;
			gap: 1rem;
			align-items: flex-start;
		}

		.ticket-meta {
			grid-template-columns: 1fr;
		}

		.header {
			flex-direction: column;
			gap: 1rem;
			align-items: stretch;
		}
	}
</style>
