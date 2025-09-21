<!-- frontend/src/routes/tickets/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	import {
		getTickets,
		deleteTicket,
		getUsers,
		updateTicket,
		type Ticket,
		type User
	} from '$lib/api/tickets';
	import TicketCard from '$lib/components/TicketCard.svelte';
	import CreateTicketModal from '$lib/components/CreateTicketModal.svelte';
	import CustomButton from '$lib/components/CustomButton.svelte';

	let tickets: Ticket[] = [];
	let users: User[] = [];
	let showCreateModal = false;

	onMount(async (): Promise<void> => {
		const resp = await getTickets();
		tickets = resp.results;
		const respUsers = await getUsers();
		users = respUsers.results;
	});

	function handleViewTicket(ticket: Ticket): void {
		goto(`/tickets/${ticket.id}`);
	}

	function handleEditTicket(ticket: Ticket): void {
		console.log('print ticket');
	}

	async function handleDeleteTicket(ticket: Ticket): Promise<void> {
		await deleteTicket(ticket.id);
		const resp = await getTickets();
		tickets = resp.results;
	}

	async function handleAssignTicket(ticket: Ticket, userId: number | null): Promise<void> {
		await updateTicket(ticket.id, {
			title: ticket.title,
			description: ticket.description,
			priority: ticket.priority,
			status: ticket.status,
			assigned_to_id: userId as number
		});
		const resp = await getTickets();
		tickets = resp.results;
	}
</script>

<div class="tickets-page">
	<div class="header">
		<h1>Tickets</h1>
		<div>
			<CustomButton
				type="button"
				variant="default"
				on:click={() => {
					showCreateModal = true;
				}}>Create Ticket</CustomButton
			>
		</div>
	</div>

	<div class="tickets-list">
		{#if tickets.length > 0 && users.length > 0}
			{#each tickets as ticket}
				<TicketCard
					{ticket}
					{users}
					onView={() => handleViewTicket(ticket)}
					onEdit={() => handleEditTicket(ticket)}
					onDelete={() => handleDeleteTicket(ticket)}
					onAssign={(userId) => handleAssignTicket(ticket, userId)}
				/>
			{/each}
		{:else}
			<div class="loading">Loading tickets and users...</div>
		{/if}
	</div>
</div>

<CreateTicketModal
	bind:open={showCreateModal}
	{users}
	onTicketCreated={async () => {
		showCreateModal = false;
		const resp = await getTickets();
		tickets = resp.results;
	}}
/>

<style>
	.tickets-page {
		padding: 2rem;
		max-width: 1000px;
		margin: 0 auto;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
	}

	.header h1 {
		margin: 0;
		font-size: 2rem;
		font-weight: 600;
	}

	.tickets-list {
		display: flex;
		flex-direction: column;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: #6f6f6f;
		font-size: 1rem;
	}

	@media (max-width: 768px) {
		.tickets-page {
			padding: 1rem;
		}

		.header {
			flex-direction: column;
			gap: 1rem;
			align-items: stretch;
		}
	}
</style>
