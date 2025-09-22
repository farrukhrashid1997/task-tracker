<script lang="ts">
	import { Button, TextInput, Tile, Grid, Row, Column } from 'carbon-components-svelte';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import CustomButton from '../../lib/components/CustomButton.svelte';
	import { login } from '$lib/stores/auth';
	import { googleAuth } from '$lib/api/auth'; // Add this import
	import { user, isAuthenticated } from '$lib/stores/auth'; // Add these

	let username = '';
	let password = '';
	let loading = false;
	let errorMessage = '';

	interface GoogleCredentialResponse {
		credential: string;
		select_by: string;
	}

	onMount(() => {
		const script = document.createElement('script');
		script.src = 'https://accounts.google.com/gsi/client';
		script.onload = initializeGoogleSignIn;
		document.head.appendChild(script);
	});

	function initializeGoogleSignIn(): void {
		if (!window.google) {
			console.error('Google Sign-In library not loaded');
			return;
		}

		window.google.accounts.id.initialize({
			client_id: '33046009397-91mkm5pdv4febp6pg867p5e90ifichjb.apps.googleusercontent.com', // Replace with your actual client ID
			callback: handleGoogleResponse
		});

		// @ts-ignore
		window.google.accounts.id.renderButton(document.getElementById('google-signin-button'), {
			theme: 'outline',
			size: 'large',
			text: 'signin_with',
			width: '100%'
		});
	}

	async function handleGoogleResponse(response: GoogleCredentialResponse) {
		try {
			loading = true;
			errorMessage = '';

			const result = await googleAuth(response.credential);
			user.set(result.user);
			isAuthenticated.set(true);
			goto('/');
		} catch (err: unknown) {
			console.error('Google sign-in error:', err);
			errorMessage = err instanceof Error ? err.message : 'Google sign-in failed';
		} finally {
			loading = false;
		}
	}

	async function handleLogin() {
		if (!username || !password) {
			errorMessage = 'Please enter username and password';
			return;
		}

		loading = true;
		const result = await login(username, password);
		loading = false;

		if (result.success) {
			goto('/');
		} else {
			errorMessage = result.error || 'Login failed';
		}
	}
</script>

<div class="login-container">
	<Grid>
		<Row>
			<Column sm={12} md={12}>
				<div class="login-card">
					<Tile style="padding: 2rem;">
						<!-- Logo/Title area -->
						<div class="login-header">
							<h1>Task Tracker</h1>
							<p>Sign in to your account</p>
						</div>

						{#if errorMessage}
							<div class="error-message">
								{errorMessage}
							</div>
						{/if}

						<form on:submit|preventDefault={handleLogin}>
							<TextInput
								bind:value={username}
								labelText="Username"
								placeholder="Enter your username"
								type="text"
								style="margin-bottom: 1rem;"
								required
							/>

							<TextInput
								bind:value={password}
								type="password"
								labelText="Password"
								placeholder="Enter your password"
								style="margin-bottom: 2rem;"
								required
							/>
							<div style="margin-bottom: 1rem;">
								<CustomButton type="submit" size="field" variant="default" disabled={loading}>
									{loading ? 'Signing In...' : 'Sign In'}
								</CustomButton>
							</div>

							<CustomButton variant="secondary" on:click={() => goto('/register')} size="field">
								Register
							</CustomButton>
							<div class="or-text">OR</div>
							<div class="google-signin-section">
								<div id="google-signin-button"></div>
							</div>
						</form>
					</Tile>
				</div>
			</Column>
		</Row>
	</Grid>
</div>

<style>
	/* Your existing styles */
	.login-container {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 1rem;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	}

	.login-card {
		width: '100%';
		min-width: 400px;
	}

	.login-header {
		text-align: center;
		margin-bottom: 2rem;
	}

	.error-message {
		background: #da1e28;
		color: white;
		padding: 0.75rem;
		border-radius: 4px;
		margin-bottom: 1rem;
		text-align: center;
	}

	.login-header h1 {
		margin: 0 0 0.5rem 0;
		font-size: 2rem;
		font-weight: 600;
	}

	.login-header p {
		margin: 0;
		color: #525252;
		font-size: 0.875rem;
	}

	.or-text {
		display: flex;
		justify-content: center;
		margin: 1rem 0;
	}

	.google-signin-section {
		margin-bottom: 1.5rem;
		display: flex;
		justify-content: center;
	}

	/* Mobile-first responsive */
	@media (max-width: 672px) {
		.login-container {
			padding: 0.5rem;
		}

		.login-card {
			max-width: 100%;
			min-width: 300px;
		}
	}
</style>
