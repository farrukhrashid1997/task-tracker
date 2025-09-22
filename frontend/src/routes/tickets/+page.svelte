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
		type User,
		type CreateTicketData,
		createTicket
	} from '$lib/api/tickets';
	import TicketCard from '$lib/components/TicketCard.svelte';
	import CreateTicketModal from '$lib/components/CreateTicketModal.svelte';
	import CustomButton from '$lib/components/CustomButton.svelte';

	let tickets: Ticket[] = [];
	let users: User[] = [];
	let showModal = false;
	let editingTicket: Ticket | null = null;
	let showCreateModal = false;
	$: modalConfig = editingTicket
		? {
				heading: 'Edit Ticket',
				buttonText: 'Update Ticket',
				initialData: editingTicket,
				onSubmit: handleUpdateTicket
			}
		: {
				heading: 'Create New Ticket',
				buttonText: 'Create Ticket',
				initialData: null,
				onSubmit: handleCreateTicket
			};

	onMount(async (): Promise<void> => {
		await loadData();
	});

	async function loadData(): Promise<void> {
		const [ticketsResp, usersResp] = await Promise.all([getTickets(), getUsers()]);
		tickets = ticketsResp.results;
		users = usersResp.results;
	}

	function closeModal(): void {
		showModal = false;
		editingTicket = null;
	}

	function handleViewTicket(ticket: Ticket): void {
		goto(`/tickets/${ticket.id}`);
	}

	function handleEditTicket(ticket: Ticket): void {
		editingTicket = ticket;
		showModal = true;
	}

	async function handleDeleteTicket(ticket: Ticket): Promise<void> {
		await deleteTicket(ticket.id);
		const resp = await getTickets();
		tickets = resp.results;
	}

	async function handleCreateTicket(data: CreateTicketData): Promise<void> {
		await createTicket(data);
		await loadData();
	}

	function openCreateModal(): void {
		editingTicket = null;
		showModal = true;
	}

	async function handleUpdateTicket(data: CreateTicketData): Promise<void> {
		if (!editingTicket) return;
		await updateTicket(editingTicket.id, data);
		await loadData();
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
			<CustomButton type="button" variant="default" on:click={openCreateModal}>Create Ticket</CustomButton
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
	bind:open={showModal}
	{users}
	modalHeading={modalConfig.heading}
	primaryButtonText={modalConfig.buttonText}
	initialData={modalConfig.initialData}
	onSubmit={modalConfig.onSubmit}
	onClose={closeModal}
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
