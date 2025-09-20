<script>
	import { Button, TextInput, Tile, Grid, Row, Column } from 'carbon-components-svelte';
	// @ts-ignore
	import { goto } from '$app/navigation';
	import CustomButton from '../../lib/components/CustomButton.svelte';
	// @ts-ignore
	import { login } from '$lib/stores/auth';

	let username = '';
	let password = '';
	let loading = false;
	let errorMessage = '';

	async function handleLogin() {
		if (!username || !password) {
			errorMessage = 'Please enter username and password';
			return;
		}

		const result = await login(username, password);
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
								<CustomButton type="submit" size="field" variant="default">{loading ? 'Signing In...' : 'Sign In'}</CustomButton>
							</div>

							<CustomButton type="submit" variant="secondary" size="field">Register</CustomButton>
						</form>
					</Tile>
				</div>
			</Column>
		</Row>
	</Grid>
</div>

<style>
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
