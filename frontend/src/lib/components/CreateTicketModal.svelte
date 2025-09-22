<!-- Simplified CreateTicketModal.svelte -->
<script lang="ts">
	import {
		Modal,
		TextInput,
		TextArea,
		Dropdown,
	} from 'carbon-components-svelte';

	import type { User, CreateTicketData, Ticket } from '$lib/api/tickets';

	export let open = false;
	export let users: User[] = [];
	export let modalHeading = 'Create New Ticket';
	export let primaryButtonText = 'Create Ticket';
	export let onSubmit: (data: CreateTicketData) => Promise<void>;
	export let onClose: () => void = () => {};
	
	export let initialData: Partial<Ticket> | null = null;

	let title = '';
	let description = '';
	let priority = 'medium';
	let status = 'open';
	let assignedTo = 'unassigned';
	let submitting = false;
	let error = '';

	const priorityItems = [
		{ id: 'low', text: 'Low Priority' },
		{ id: 'medium', text: 'Medium Priority' },
		{ id: 'high', text: 'High Priority' }
	];

	const statusItems = [
		{ id: 'open', text: 'Open' },
		{ id: 'in_progress', text: 'In Progress' },
		{ id: 'closed', text: 'Closed' }
	];

	$: assigneeItems = [
		{ id: 'unassigned', text: 'Unassigned' },
		...users.map((user) => ({
			id: user.id.toString(),
			text: `${user.first_name} ${user.last_name} (${user.username})`
		}))
	];

	// Pre-fill form when initialData changes
	$: if (initialData && open) {
		title = initialData.title || '';
		description = initialData.description || '';
		priority = initialData.priority || 'medium';
		status = initialData.status || 'open';
		assignedTo = initialData.assigned_to?.id ? initialData.assigned_to.id.toString() : 'unassigned';
	}

	function resetForm(): void {
		title = '';
		description = '';
		priority = 'medium';
		status = 'open';
		assignedTo = 'unassigned';
		submitting = false;
		error = '';
	}

	function handleClose(): void {
		resetForm();
		onClose();
	}

	async function handleSubmit(): Promise<void> {
		if (!title.trim() || !description.trim()) return;

		submitting = true;
		error = '';

		try {
			const ticketData: CreateTicketData = {
				title: title.trim(),
				description: description.trim(),
				priority: priority as 'low' | 'medium' | 'high',
				status: status as 'open' | 'in_progress' | 'closed',
				assigned_to_id: assignedTo !== 'unassigned' ? parseInt(assignedTo) : null
			};

			await onSubmit(ticketData);
			handleClose();
		} catch (err) {
			error = 'Failed to save ticket. Please try again.';
			submitting = false;
		}
	}

	$: isValid = title.trim() && description.trim();
	$: buttonText = submitting ? '' : primaryButtonText;
</script>

<Modal
	bind:open
	{modalHeading}
	primaryButtonText={buttonText}
	primaryButtonDisabled={!isValid || submitting}
	on:click:button--primary={handleSubmit}
	on:close={handleClose}
	size="lg"
	class="ticket-modal"
>
	<div class="form-container">
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
					titleText="Status"
					selectedId={status}
					items={statusItems}
					on:select={(e) => (status = e.detail.selectedId)}
					class="status-dropdown"
				/>
			</div>
		</div>

		<div class="form-section">
			<Dropdown
				titleText="Assign To Team Member"
				selectedId={assignedTo}
				items={assigneeItems}
				on:select={(e) => (assignedTo = e.detail.selectedId)}
				class="assignee-dropdown"
			/>
		</div>

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
</style>