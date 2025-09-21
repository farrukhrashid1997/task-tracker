<!-- src/app.html or your main layout file -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { isAuthenticated, authLoading, checkAuth } from '$lib/stores/auth';
	import MainLayout from '$lib/components/MainLayout.svelte';
	import favicon from '$lib/assets/favicon.svg';
	import '../app.css';

	let { children } = $props();

	const publicRoutes = ['/login', '/register'];

	onMount(() => {
		checkAuth();
	});

	$effect(() => {
		if (!$authLoading) {
			const currentPath = $page.url.pathname;
			const isPublicRoute = publicRoutes.includes(currentPath);
			
			if (!$isAuthenticated && !isPublicRoute) {
				goto('/login');
			}
			
			if ($isAuthenticated && currentPath === '/login') {
				goto('/');
			}
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>TicketFlow - Ticket Management System</title>
	<meta name="description" content="Modern ticket management system" />
</svelte:head>

{#if $authLoading}
	<div class="loading-container">
		<div class="loading-spinner"></div>
		<p>Loading...</p>
	</div>
{:else}
	<MainLayout>
		{@render children?.()}
	</MainLayout>
{/if}

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		background: #f8fafc;
		color: #1e293b;
		line-height: 1.6;
	}

	:global(*) {
		box-sizing: border-box;
	}

	.loading-container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100vh;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid rgba(255, 255, 255, 0.3);
		border-top: 4px solid white;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
	}

	.loading-container p {
		font-size: 1.1rem;
		margin: 0;
		opacity: 0.9;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	/* Global styles for consistency */
	:global(.btn) {
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.2s ease;
		text-decoration: none;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-size: 0.875rem;
	}

	:global(.btn-primary) {
		background: #667eea;
		color: white;
	}

	:global(.btn-primary:hover) {
		background: #5a6fd8;
		transform: translateY(-1px);
	}

	:global(.btn-secondary) {
		background: #e2e8f0;
		color: #475569;
	}

	:global(.btn-secondary:hover) {
		background: #cbd5e1;
	}

	:global(.card) {
		background: white;
		border-radius: 12px;
		padding: 1.5rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		border: 1px solid #e2e8f0;
	}

	:global(.form-group) {
		margin-bottom: 1rem;
	}

	:global(.form-label) {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 500;
		color: #374151;
	}

	:global(.form-input) {
		width: 100%;
		padding: 0.75rem;
		border: 1px solid #d1d5db;
		border-radius: 6px;
		font-size: 0.875rem;
		transition: border-color 0.2s ease;
	}

	:global(.form-input:focus) {
		outline: none;
		border-color: #667eea;
		box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
	}

	:global(.text-sm) {
		font-size: 0.875rem;
	}

	:global(.text-xs) {
		font-size: 0.75rem;
	}

	:global(.text-muted) {
		color: #6b7280;
	}

	:global(.mb-4) {
		margin-bottom: 1rem;
	}

	:global(.mb-6) {
		margin-bottom: 1.5rem;
	}
</style>