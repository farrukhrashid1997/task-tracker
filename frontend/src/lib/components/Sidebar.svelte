<!-- lib/components/Sidebar.svelte -->
<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { logout } from '$lib/stores/auth';

	$: currentPath = $page.url.pathname;

	const navItems = [
		{
			path: '/',
			label: 'Dashboard'
		},
		{
			path: '/tickets',
			label: 'Tickets'
		},
		{
			path: '/profile',
			label: 'Profile'
		}
	];

	function handleLogout() {
		logout();
		goto('/login');
	}
</script>

<aside class="sidebar">
	<div class="sidebar-header">
		<h2>TicketFlow</h2>
	</div>

	<nav class="sidebar-nav">
		<ul>
			{#each navItems as item}
				<li>
					<a href={item.path} class="nav-link" class:active={currentPath === item.path}>
						<span class="nav-label">{item.label}</span>
					</a>
				</li>
			{/each}
		</ul>
	</nav>

	<div class="sidebar-footer">
		<button class="logout-btn" on:click={handleLogout}>
			<span class="nav-icon">🚪</span>
			<span>Logout</span>
		</button>
	</div>
</aside>

<style>
	.sidebar {
		width: 250px;
		height: 100vh;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		display: flex;
		flex-direction: column;
		z-index: 1000;
	}

	.sidebar-header {
		padding: 2rem 1.5rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.2);
	}

	.sidebar-header h2 {
		margin: 0;
		font-size: 1.5rem;
		font-weight: 600;
		background: linear-gradient(45deg, #fff, #e0e7ff);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.sidebar-nav {
		flex: 1;
		padding: 1rem 0;
	}


	.sidebar-nav li {
		margin: 0.5rem 0;
	}

	.nav-link {
		display: flex;
		align-items: center;
		padding: 0.75rem 1.5rem;
		color: rgba(255, 255, 255, 0.8);
		text-decoration: none;
		transition: all 0.3s ease;
		border-radius: 0 25px 25px 0;
		margin-right: 1rem;
	}

	.nav-link:hover {
		background: rgba(255, 255, 255, 0.1);
		color: white;
		transform: translateX(5px);
	}

	.nav-link.active {
		background: rgba(255, 255, 255, 0.2);
		color: white;
		box-shadow: inset 3px 0 0 #fff;
	}

	.nav-icon {
		font-size: 1.2rem;
		margin-right: 0.75rem;
		width: 24px;
		text-align: center;
	}

	.nav-label {
		font-weight: 500;
	}

	.sidebar-footer {
		padding: 1.5rem;
		border-top: 1px solid rgba(255, 255, 255, 0.2);
	}

	.logout-btn {
		display: flex;
		align-items: center;
		width: 100%;
		padding: 0.75rem;
		background: rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.8);
		border: none;
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.3s ease;
		font-size: 0.95rem;
	}

	.logout-btn:hover {
		background: rgba(255, 255, 255, 0.2);
		color: white;
		transform: translateY(-2px);
	}

	.logout-btn .nav-icon {
		margin-right: 0.75rem;
	}

	/* Mobile responsiveness */
	@media (max-width: 768px) {

	}
</style>
