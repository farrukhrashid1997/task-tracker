<!-- src/routes/(app)/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { getDashboardSummary, getTicketStatusStats, getTicketPriorityStats } from '$lib/api/dashboard';
	import ChartWrapper from '$lib/components/ChartWrapper.svelte';
	import { StatusPieChart, PriorityBarChart } from '$lib/components/ReactChart.tsx';
	import type { DashboardSummary } from '$lib/api/dashboard';
	
	// State management
	let loading = $state(true);
	let error = $state<string | null>(null);
	let dashboardData = $state({
		summary: {
			total_tickets: 0,
			open_tickets: 0,
			in_progress_tickets: 0,
			closed_tickets: 0,
			high_priority_tickets: 0,
			unassigned_tickets: 0
		} as DashboardSummary,
		statusStats: {} as Record<string, number>,
		priorityStats: {} as Record<string, number>
	});

	// Load real data from API
	async function loadDashboardData() {
		try {
			loading = true;
			error = null;
			
			// Call the API functions
			const [summary, statusStats, priorityStats] = await Promise.all([
				getDashboardSummary(),
				getTicketStatusStats(),
				getTicketPriorityStats()
			]);
			
			dashboardData = {
				summary,
				statusStats: statusStats.status_distribution,
				priorityStats: priorityStats.priority_distribution
			};
			
		} catch (err) {
			console.error('Failed to load dashboard:', err);
			error = err instanceof Error ? err.message : 'Failed to load dashboard data';
			
			// Fallback to mock data for development
			
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		loadDashboardData();
	});
</script>

<div class="dashboard">
	<div class="dashboard-header">
		<h1>Dashboard</h1>
		<p>Overview of your ticket management system</p>
	</div>

	{#if loading}
		<div class="loading-state">
			<div class="loading-spinner"></div>
			<p>Loading dashboard...</p>
		</div>
	{:else if error}
		<div class="error-state">
			<h3>Error loading dashboard</h3>
			<p>{error}</p>
			<button class="btn btn-primary" on:click={loadDashboardData}>
				Try Again
			</button>
		</div>
	{:else}
		<!-- Statistics Cards -->
		<div class="stats-grid">
			<div class="stat-card blue">
				<div class="stat-icon">🎫</div>
				<div class="stat-content">
					<h3>{dashboardData.summary.total_tickets}</h3>
					<p>Total Tickets</p>
				</div>
			</div>
			
			<div class="stat-card red">
				<div class="stat-icon">🔓</div>
				<div class="stat-content">
					<h3>{dashboardData.summary.open_tickets}</h3>
					<p>Open Tickets</p>
				</div>
			</div>
			
			<div class="stat-card orange">
				<div class="stat-icon">⏳</div>
				<div class="stat-content">
					<h3>{dashboardData.summary.in_progress_tickets}</h3>
					<p>In Progress</p>
				</div>
			</div>
			
			<div class="stat-card green">
				<div class="stat-icon">✅</div>
				<div class="stat-content">
					<h3>{dashboardData.summary.closed_tickets}</h3>
					<p>Closed</p>
				</div>
			</div>
			
			<div class="stat-card red">
				<div class="stat-icon">🚨</div>
				<div class="stat-content">
					<h3>{dashboardData.summary.high_priority_tickets}</h3>
					<p>High Priority</p>
				</div>
			</div>
			
			<div class="stat-card gray">
				<div class="stat-icon">👤</div>
				<div class="stat-content">
					<h3>{dashboardData.summary.unassigned_tickets}</h3>
					<p>Unassigned</p>
				</div>
			</div>
		</div>

		<!-- Charts Section -->
		<div class="charts-section">
			<h2>Analytics</h2>
			
			<div class="charts-grid">
				<!-- Status Distribution Chart -->
				<div class="chart-card">
					<div class="chart-header">
						<h3>Ticket Status Distribution</h3>
						<p>Current status breakdown of all tickets</p>
					</div>
					<div class="chart-container">
						{console.log(dashboardData)}
						<ChartWrapper component={StatusPieChart} data={dashboardData.statusStats} />
					</div>
				</div>

				<!-- Priority Distribution Chart -->
				<div class="chart-card">
					<div class="chart-header">
						<h3>Priority Distribution</h3>
						<p>Tickets grouped by priority level</p>
					</div>
					<div class="chart-container">
						<ChartWrapper component={PriorityBarChart} data={dashboardData.priorityStats} />
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.dashboard {
		max-width: 1200px;
		margin: 0 auto;
	}

	.dashboard-header {
		margin-bottom: 2rem;
	}

	.dashboard-header h1 {
		font-size: 2.5rem;
		font-weight: 700;
		color: #1e293b;
		margin: 0 0 0.5rem 0;
	}

	.dashboard-header p {
		color: #64748b;
		font-size: 1.1rem;
		margin: 0;
	}

	.loading-state,
	.error-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 4rem 2rem;
		text-align: center;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid #e2e8f0;
		border-top: 4px solid #667eea;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	.error-state h3 {
		color: #ef4444;
		margin-bottom: 0.5rem;
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1.5rem;
		margin-bottom: 3rem;
	}

	.stat-card {
		background: white;
		border-radius: 12px;
		padding: 1.5rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		border: 1px solid #e2e8f0;
		display: flex;
		align-items: center;
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}

	.stat-card:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.stat-icon {
		font-size: 2.5rem;
		margin-right: 1rem;
		flex-shrink: 0;
	}

	.stat-content h3 {
		font-size: 2rem;
		font-weight: 700;
		margin: 0 0 0.25rem 0;
	}

	.stat-content p {
		font-size: 0.875rem;
		color: #64748b;
		margin: 0;
		font-weight: 500;
	}

	.stat-card.blue .stat-content h3 { color: #3b82f6; }
	.stat-card.red .stat-content h3 { color: #ef4444; }
	.stat-card.orange .stat-content h3 { color: #f59e0b; }
	.stat-card.green .stat-content h3 { color: #10b981; }
	.stat-card.gray .stat-content h3 { color: #6b7280; }

	.charts-section {
		margin-top: 3rem;
	}

	.charts-section h2 {
		font-size: 1.875rem;
		font-weight: 600;
		color: #1e293b;
		margin-bottom: 1.5rem;
	}

	.charts-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
		gap: 2rem;
	}

	.chart-card {
		background: white;
		border-radius: 12px;
		padding: 1.5rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		border: 1px solid #e2e8f0;
	}

	.chart-header {
		margin-bottom: 1.5rem;
	}

	.chart-header h3 {
		font-size: 1.25rem;
		font-weight: 600;
		color: #1e293b;
		margin: 0 0 0.5rem 0;
	}

	.chart-header p {
		color: #64748b;
		font-size: 0.875rem;
		margin: 0;
	}

	.chart-container {
		position: relative;
		height: 300px;
	}

	.btn {
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.2s ease;
	}

	.btn-primary {
		background: #667eea;
		color: white;
	}

	.btn-primary:hover {
		background: #5a6fd8;
	}

	/* Mobile responsiveness */
	@media (max-width: 768px) {
		.dashboard-header h1 {
			font-size: 2rem;
		}

		.stats-grid {
			grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
			gap: 1rem;
		}

		.stat-card {
			padding: 1rem;
		}

		.stat-icon {
			font-size: 2rem;
		}

		.stat-content h3 {
			font-size: 1.5rem;
		}

		.charts-grid {
			grid-template-columns: 1fr;
			gap: 1.5rem;
		}

		.chart-card {
			padding: 1rem;
		}
	}

	@media (max-width: 480px) {
		.stat-card {
			flex-direction: column;
			text-align: center;
		}

		.stat-icon {
			margin-right: 0;
			margin-bottom: 0.5rem;
		}
	}
</style>