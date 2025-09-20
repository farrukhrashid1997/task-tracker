<!-- frontend/src/lib/components/CreateTicketModal.svelte -->
<script lang="ts">
	import {
		Modal,
		TextInput,
		TextArea,
		Dropdown,
	} from 'carbon-components-svelte';

	import { createTicket, type User, type CreateTicketData } from '$lib/api/tickets';

	export let open = false;
	export let users: User[] = [];
	export let onTicketCreated: () => void = () => {};

	let title = '';
	let description = '';
	let priority = 'Medium';
	let status = 'Open';
	let assignedTo = 'unassigned';
	let creating = false;
	let error = '';

	const priorityItems = [
		{ id: 'Low', text: 'Low Priority' },
		{ id: 'Medium', text: 'Medium Priority' },
		{ id: 'High', text: 'High Priority' }
	];

	const statusItems = [
		{ id: 'Open', text: 'Open' },
		{ id: 'In Progress', text: 'In Progress' },
		{ id: 'Closed', text: 'Closed' }
	];

	$: assigneeItems = [
		{ id: 'unassigned', text: 'Unassigned' },
		...users.map((user) => ({
			id: user.id.toString(),
			text: `${user.first_name} ${user.last_name} (${user.username})`
		}))
	];

	function resetForm(): void {
		title = '';
		description = '';
		priority = 'Medium';
		status = 'Open';
		assignedTo = 'unassigned';
		creating = false;
		error = '';
	}

	// BUG: Modal doesnt close and refresh once you hit create
	function handleClose(): void {
		open = false;
		resetForm();
	}

	async function handleSubmit(): Promise<void> {
		if (!title.trim() || !description.trim()) return;

		creating = true;
		error = '';

		try {
			const ticketData: CreateTicketData = {
				title: title.trim(),
				description: description.trim(),
				priority: priority as 'low' | 'medium' | 'high',
				status: status as 'open' | 'in_progress' | 'closed',
				assigned_to_id: assignedTo !== 'unassigned' ? parseInt(assignedTo) : null
			};

			await createTicket(ticketData);
			handleClose();
			onTicketCreated();
		} catch (err) {
			error = 'Failed to create ticket. Please try again.';
			creating = false;
		}
	}

	$: isValid = title.trim() && description.trim();
	$: primaryButtonText = creating ? '' : 'Create Ticket';
</script>

<Modal
	bind:open
	modalHeading="Create New Ticket"
	{primaryButtonText}
	primaryButtonDisabled={!isValid || creating}
	on:click:button--primary={handleSubmit}
	on:close={handleClose}
	size="lg"
	class="ticket-modal"
>
	<div class="form-container">
		<!-- Title Section -->
		<div class="form-section">
			<TextInput
				labelText="Title"
				placeholder="Enter a clear, descriptive title..."
				bind:value={title}
				invalid={!title.trim() && title !== ''}
				invalidText="Title is required"
				class="title-input"
			/>
		</div>

		<div class="form-section">
			<TextArea
				labelText="Description"
				placeholder="Provide detailed information about the issue or request..."
				bind:value={description}
				rows={4}
				invalid={!description.trim() && description !== ''}
				invalidText="Description is required"
				class="description-input"
			/>
		</div>

		<!-- Priority and Status Row -->
		<div class="form-row">
			<div class="form-field">
				<Dropdown
					titleText="Priority Level"
					selectedId={priority}
					items={priorityItems}
					on:select={(e) => (priority = e.detail.selectedId)}
					class="priority-dropdown"
				/>
			</div>

			<div class="form-field">
				<Dropdown
					titleText="Initial Status"
					selectedId={status}
					items={statusItems}
					on:select={(e) => (status = e.detail.selectedId)}
					class="status-dropdown"
				/>
			</div>
		</div>

		<!-- Assignment Section -->
		<div class="form-section">
			<Dropdown
				titleText="Assign To Team Member"
				selectedId={assignedTo}
				items={assigneeItems}
				on:select={(e) => (assignedTo = e.detail.selectedId)}
				class="assignee-dropdown"
			/>
		</div>

		<!-- Loading and Error States -->
		{#if error}
			<div class="status-indicator error">
				<div class="error-message">
					<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
						<path
							d="M8 0C3.6 0 0 3.6 0 8s3.6 8 8 8 8-3.6 8-8-3.6-8-8-8zm3.5 10.1L10.1 11.5 8 9.4 5.9 11.5 4.5 10.1 6.6 8 4.5 5.9 5.9 4.5 8 6.6l2.1-2.1 1.4 1.4L9.4 8l2.1 2.1z"
						/>
					</svg>
					<span>{error}</span>
				</div>
			</div>
		{/if}

		<!-- Form Help Text -->
		<div class="help-text">
			<p>All fields marked with * are required. You can assign the ticket later if needed.</p>
		</div>
	</div>
</Modal>

<style>
	/* Form Layout */
	.form-container {
		display: flex;
		flex-direction: column;
		gap: 1.75rem;
		padding: 1.5rem 0;
		max-height: 60vh;
		overflow-y: auto;
	}

	.form-section {
		display: flex;
		flex-direction: column;
	}

	:global(.bx--btn.bx--btn--primary) {
		display: flex;
		flex: 1;
		justify-content: center;
	}

	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.25rem;
	}

	.form-field {
		display: flex;
		flex-direction: column;
	}

	/* Custom Footer */
	.custom-footer {
		display: flex;
		justify-content: center;
		padding: 2rem;
		width: 100%;
		border-top: 1px solid #e0e0e0;
		background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
		margin: 0 -2rem -1.5rem -2rem;
	}

	.button-content {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		z-index: 2;
	}

	.btn-icon {
		transition: transform 0.2s ease;
	}
	.btn-text {
		display: flex;
		align-items: center;
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	/* Shine Effect */
	.btn-shine {
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
		transition: left 0.6s ease;
	}

	:global(.create-btn:hover:not(:disabled)) .btn-shine {
		left: 100%;
	}

	/* Loading Spinner */
	.spinner {
		width: 18px;
		height: 18px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-top: 2px solid #ffffff;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Status Indicators */
	.status-indicator {
		padding: 1rem;
		border-radius: 8px;
		margin: 0.5rem 0;
	}

	.status-indicator.loading {
		background: #f0f7ff;
		border: 1px solid #d0e2ff;
		text-align: center;
	}

	.status-indicator.error {
		background: #fff1f1;
		border: 1px solid #ffd7d9;
	}

	.error-message {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		color: #da1e28;
		font-size: 0.875rem;
	}

	/* Help Text */
	.help-text {
		background: #f4f4f4;
		padding: 1rem;
		border-radius: 8px;
		border-left: 4px solid #0f62fe;
	}

	.help-text p {
		margin: 0;
		font-size: 0.875rem;
		color: #525252;
		line-height: 1.4;
	}

	/* Modal Styling */
	:global(.ticket-modal .bx--modal-container) {
		border-radius: 16px !important;
		box-shadow: 0 16px 32px rgba(0, 0, 0, 0.15) !important;
		max-width: 600px !important;
	}

	:global(.ticket-modal .bx--modal-header) {
		border-bottom: 1px solid #e0e0e0;
		padding: 2rem 2rem 1.5rem 2rem;
		background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
		border-radius: 16px 16px 0 0;
	}

	:global(.ticket-modal .bx--modal-content) {
		padding: 0 2rem;
		background: #ffffff;
	}

	:global(.ticket-modal .bx--modal-close) {
		top: 1.5rem;
		right: 1.5rem;
	}

	/* Input Styling */
	:global(.title-input input) {
		font-size: 1rem;
		font-weight: 500;
	}

	:global(.description-input textarea) {
		font-family: inherit;
		line-height: 1.5;
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.form-row {
			grid-template-columns: 1fr;
		}

		.custom-footer {
			padding: 1.5rem;
		}

		:global(.create-btn) {
			min-width: 160px;
			height: 44px;
			font-size: 0.9rem;
		}

		:global(.ticket-modal .bx--modal-container) {
			max-width: 95vw !important;
			margin: 1rem;
		}

		.form-container {
			max-height: 70vh;
		}
	}

	/* Loading Animation */
	@keyframes pulse {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0.7;
		}
	}

	.status-indicator.loading {
		animation: pulse 2s infinite;
	}

	/* Focus States */
	:global(.create-btn:focus) {
		outline: 2px solid #0f62fe;
		outline-offset: 2px;
	}
</style>
