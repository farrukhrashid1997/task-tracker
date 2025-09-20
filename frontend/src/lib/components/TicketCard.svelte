<!-- frontend/src/lib/components/TicketCard.svelte -->
<script lang="ts">
	import { Edit, TrashCan } from 'carbon-icons-svelte';
	import { Button, Tag, Dropdown } from 'carbon-components-svelte';
	import type { Ticket, User } from '$lib/api/tickets';

	export let users: User[] = [];
	export let ticket: Ticket;
	export let onView: () => void = () => {};
	export let onEdit: () => void = () => {};
	export let onDelete: () => void = () => {};
	export let onAssign: (userId: number | null) => void = () => {};

	const priorityColors: Record<string, string> = {
		low: 'green',
		medium: 'cyan',
		high: 'red'
	};

	const statusColors: Record<string, string> = {
		open: 'blue',
		'in_progress': 'purple',
		closed: 'gray'
	};

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	// Create dropdown items for user assignment
	$: dropdownItems = [
		{ id: 'unassigned', text: 'Unassigned' },
		...users.map((user) => ({
			id: user.id.toString(),
			text: `${user.username}`
		}))
	];

	$: selectedId = ticket?.assigned_to?.id ? ticket.assigned_to.id.toString() : 'unassigned';

	function handleAssignmentChange(event: CustomEvent) {
		const newAssignedId = event.detail.selectedId;
		const userId = newAssignedId === 'unassigned' ? null : parseInt(newAssignedId);
		onAssign(userId);
	}

	console.log(ticket.priority.toLowerCase())

</script>


<div class="ticket-card">
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="ticket-content" on:click={onView}>
		<div class="ticket-header">
			<h3 class="ticket-title">#{ticket.id} - {ticket.title}</h3>
			<div class="assignee">
				<div class="assignment-dropdown" on:click|stopPropagation>
					<Dropdown
						titleText=""
						{selectedId}
						items={dropdownItems}
						on:select={handleAssignmentChange}
						size="sm"
					/>
				</div>
			</div>
		</div>

		<div class="ticket-meta">
			<div class="tags">
				<Tag type={priorityColors[ticket.priority.toLowerCase()] as any}>{ticket.priority}</Tag>
				<Tag type={statusColors[ticket.status.toLowerCase()] as any}>{ticket.status}</Tag>
			</div>
		</div>

		<p class="ticket-description">{ticket.description}</p>

		<div class="ticket-footer">
			<span class="created-date">Created: {formatDate(ticket.created_at)}</span>
		</div>
	</div>

	<div class="ticket-actions">
		<Button kind="ghost" size="small" icon={Edit} on:click={onEdit} />
		<Button kind="danger-ghost" size="small" icon={TrashCan} on:click={onDelete} />
	</div>
</div>

<style>
	.ticket-card {
		background: white;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		margin-bottom: 1rem;
		display: flex;
		transition: box-shadow 0.2s ease;
	}

	.ticket-card:hover {
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.ticket-content {
		flex: 1;
		padding: 1.5rem;
		cursor: pointer;
	}

	.ticket-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}

	.ticket-title {
		margin: 0;
		font-size: 1.1rem;
		font-weight: 600;
		color: #161616;
	}

	.ticket-meta {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}

	.tags {
		display: flex;
		gap: 0.5rem;
	}

	.current-assignee {
		font-weight: 500;
	}

	.assignment-dropdown {
		border: '1px solid ';
	}

	.assignment-dropdown :global(.bx--dropdown) {
		border: 1px solid #e0e0e0;
		border-radius: 4px;
		font-size: 0.75rem;
		min-height: 28px;
	}

	.assignment-dropdown :global(.bx--dropdown__wrapper) {
		background: transparent;
	}

	.assignment-dropdown :global(.bx--list-box__field) {
		background: #f4f4f4;
		border: none;
		min-height: 28px;
	}

	.assignment-dropdown :global(.bx--list-box__field:hover) {
		background: #e8e8e8;
	}

	.ticket-description {
		color: #393939;
		margin: 0 0 1rem 0;
		line-height: 1.5;
	}

	.ticket-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.created-date {
		color: #6f6f6f;
		font-size: 0.75rem;
	}

	.ticket-actions {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		padding: 1rem;
		border-left: 1px solid #e0e0e0;
		justify-content: center;
	}

	@media (max-width: 768px) {
		.ticket-card {
			flex-direction: column;
		}

		.ticket-actions {
			flex-direction: row;
			border-left: none;
			border-top: 1px solid #e0e0e0;
			justify-content: flex-end;
		}
	}
</style>
