<script lang="ts">
	import { onMount } from 'svelte';
	
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { isAuthenticated, authLoading, checkAuth } from '$lib/stores/auth';
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
</svelte:head>

{#if $authLoading}
	<div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
		Loading...
	</div>
{:else}
	{@render children?.()}
{/if}