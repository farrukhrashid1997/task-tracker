<script>
	import { Button, TextInput, Tile, Grid, Row, Column } from 'carbon-components-svelte';
	// @ts-ignore
	import { goto } from '$app/navigation';
	import CustomButton from '../../lib/components/CustomButton.svelte';

	let email = '';
	let password = '';

	function handleLogin() {
		// Simple true/false auth for now
		if (email && password) {
			// For now, just redirect to dashboard
			goto('/');
		} else {
			alert('Please enter email and password');
		}
	}
</script>

<!-- Mobile-first container -->
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
						<form on:submit|preventDefault={handleLogin}>
							<TextInput
								bind:value={email}
								labelText="Email"
								placeholder="Enter your email"
								type="email"
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
								<CustomButton type="submit" size="field" variant="default">Sign In</CustomButton>
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
