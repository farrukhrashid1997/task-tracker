<!-- lib/components/GoogleSignIn.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { googleAuth } from '$lib/api/auth';
	import { user, isAuthenticated } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	let loading = $state(false);
	let error = $state<string | null>(null);

	onMount(() => {
		// Load Google Sign-In script
		const script = document.createElement('script');
		script.src = 'https://accounts.google.com/gsi/client';
		script.onload = initializeGoogleSignIn;
		document.head.appendChild(script);
	});

	function initializeGoogleSignIn() {
		// Initialize Google Sign-In
		google.accounts.id.initialize({
			client_id: 'YOUR_GOOGLE_CLIENT_ID', // Replace with your actual client ID
			callback: handleGoogleResponse
		});

		// Render the sign-in button
		google.accounts.id.renderButton(
			document.getElementById('google-signin-button'),
			{
				theme: 'outline',
				size: 'large',
				text: 'signin_with',
				width: 250
			}
		);
	}

	async function handleGoogleResponse(response: any) {
		try {
			loading = true;
			error = null;

			// Send the credential to your backend
			const result = await googleAuth(response.credential);
			
			user.set(result.user);
			isAuthenticated.set(true);
			
			// Redirect to dashboard
			goto('/');
			
		} catch (err) {
			console.error('Google sign-in error:', err);
			error = err instanceof Error ? err.message : 'Google sign-in failed';
		} finally {
			loading = false;
		}
	}
</script>

<div class="google-signin-container">
	{#if error}
		<div class="error-message">
			{error}
		</div>
	{/if}
	
	{#if loading}
		<div class="loading-overlay">
			<div class="loading-spinner"></div>
		</div>
	{/if}
	
	<div id="google-signin-button"></div>
</div>

<style>
	.google-signin-container {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
	}

	.error-message {
		background: #fef2f2;
		color: #dc2626;
		padding: 0.75rem 1rem;
		border-radius: 6px;
		border: 1px solid #fecaca;
		font-size: 0.875rem;
	}

	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.8);
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 6px;
	}

	.loading-spinner {
		width: 20px;
		height: 20px;
		border: 2px solid #e5e7eb;
		border-top: 2px solid #3b82f6;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
</style>