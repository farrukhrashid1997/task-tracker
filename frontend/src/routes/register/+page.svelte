<script lang="ts">
	import { Button, TextInput, Tile, Grid, Row, Column, Select, SelectItem } from 'carbon-components-svelte';
	import { goto } from '$app/navigation';
	import CustomButton from '../../lib/components/CustomButton.svelte';

	let username = '';
	let email = '';
	let password = '';
	let confirmPassword = '';
	let firstName = '';
	let lastName = '';
	let role = 'customer';
	let loading = false;
	let errorMessage = '';

	async function handleRegister() {
	// Basic validation
	if (!username || !email || !password || !firstName || !lastName) {
		errorMessage = 'All fields are required';
		return;
	}

	if (password !== confirmPassword) {
		errorMessage = 'Passwords do not match';
		return;
	}

	if (password.length < 6) {
		errorMessage = 'Password must be at least 6 characters';
		return;
	}

	loading = true;
	errorMessage = '';

	try {
		const { register } = await import('$lib/stores/auth');
		const result = await register(username, email, password, firstName, lastName, role);
		
		if (result.success) {
			// Registration successful, redirect to dashboard (user is now logged in via cookies)
			goto('/');
		} else {
			errorMessage = result.error || 'Registration failed';
		}
	} catch (error: any) {
		errorMessage = error.message || 'Registration failed';
	} finally {
		loading = false;
	}
}
</script>

<div class="register-container">
	<Grid>
		<Row>
			<Column sm={12} md={12}>
				<div class="register-card">
					<Tile style="padding: 2rem;">
						<div class="register-header">
							<h1>Create Account</h1>
							<p>Join Task Tracker</p>
						</div>

						{#if errorMessage}
							<div class="error-message">
								{errorMessage}
							</div>
						{/if}

						<form on:submit|preventDefault={handleRegister}>
							<div class="form-row">
								<TextInput
									bind:value={firstName}
									labelText="First Name"
									placeholder="Enter your first name"
									style="margin-bottom: 1rem; margin-right: 0.5rem;"
									disabled={loading}
									required
								/>

								<TextInput
									bind:value={lastName}
									labelText="Last Name"
									placeholder="Enter your last name"
									style="margin-bottom: 1rem; margin-left: 0.5rem;"
									disabled={loading}
									required
								/>
							</div>

							<TextInput
								bind:value={username}
								labelText="Username"
								placeholder="Choose a username"
								style="margin-bottom: 1rem;"
								disabled={loading}
								required
							/>

							<TextInput
								bind:value={email}
								labelText="Email"
								placeholder="Enter your email"
								type="email"
								style="margin-bottom: 1rem;"
								disabled={loading}
								required
							/>

							<Select
								bind:selected={role}
								labelText="Role"
								style="margin-bottom: 1rem;"
								disabled={loading}
							>
								<SelectItem value="customer" text="Customer" />
								<SelectItem value="agent" text="Agent" />
								<SelectItem value="admin" text="Admin" />
							</Select>

							<TextInput
								bind:value={password}
								type="password"
								labelText="Password"
								placeholder="Enter your password"
								style="margin-bottom: 1rem;"
								disabled={loading}
								required
							/>

							<TextInput
								bind:value={confirmPassword}
								type="password"
								labelText="Confirm Password"
								placeholder="Confirm your password"
								style="margin-bottom: 2rem;"
								disabled={loading}
								required
							/>

							<div style="margin-bottom: 1rem;">
								<CustomButton 
									type="submit" 
									size="field" 
									variant="default"
									disabled={loading}
								>
									{loading ? 'Creating Account...' : 'Create Account'}
								</CustomButton>
							</div>

							<CustomButton 
								type="button" 
								variant="secondary" 
								size="field"
								disabled={loading}
								on:click={() => goto('/login')}
							>
								Back to Login
							</CustomButton>
						</form>
					</Tile>
				</div>
			</Column>
		</Row>
	</Grid>
</div>

<style>
	.register-container {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 1rem;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	}

	.register-card {
		width: 100%;
		min-width: 500px;
		max-width: 600px;
	}

	.register-header {
		text-align: center;
		margin-bottom: 2rem;
	}

	.register-header h1 {
		margin: 0 0 0.5rem 0;
		font-size: 2rem;
		font-weight: 600;
	}

	.register-header p {
		margin: 0;
		color: #525252;
		font-size: 0.875rem;
	}

	.form-row {
		display: flex;
		gap: 1rem;
	}

	.error-message {
		background: #da1e28;
		color: white;
		padding: 0.75rem;
		border-radius: 4px;
		margin-bottom: 1rem;
		text-align: center;
	}

	@media (max-width: 672px) {
		.register-container {
			padding: 0.5rem;
		}

		.register-card {
			min-width: 300px;
		}

		.form-row {
			flex-direction: column;
			gap: 0;
		}
	}
</style>