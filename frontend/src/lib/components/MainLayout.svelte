<script lang="ts">
  import { page } from '$app/stores';
  import Sidebar from './Sidebar.svelte';

  // Svelte 5 runes
  let sidebarOpen = $state(false);

  // Derived: show sidebar except on login/register
  let showSidebar = $derived(!['/login', '/register'].includes($page.url.pathname));

  function toggleSidebar() {
    sidebarOpen = !sidebarOpen;
  }

  // Close sidebar on route change
  $effect(() => {
    // will re-run whenever $page.url.pathname changes
    if ($page.url.pathname) {
      sidebarOpen = false;
    }
  });
</script>

{#if showSidebar}
  <div class="layout-container">
    <!-- Mobile menu button -->
    <button
      class="mobile-menu-btn"
      on:click={toggleSidebar}
      aria-label="Toggle menu"
    >
      <span class="hamburger"></span>
    </button>

    <!-- Sidebar -->
    <div class="sidebar-wrapper" class:mobile-open={sidebarOpen}>
      <Sidebar />
    </div>

    <!-- Mobile overlay -->
    {#if sidebarOpen}
      <div class="mobile-overlay" on:click={toggleSidebar}></div>
    {/if}

    <!-- Main content -->
    <main class="main-content">
      <div class="content-wrapper">
        <slot />
      </div>
    </main>
  </div>
{:else}
  <!-- Login/Register pages without sidebar -->
  <main class="auth-main">
    <slot />
  </main>
{/if}

<style>
  .layout-container {
    display: flex;
    min-height: 100vh;
    background: #f8fafc;
  }

  .sidebar-wrapper {
    position: relative;
    width: 250px;
  }

  .main-content {
    flex: 1;
    background: #f8fafc;
    transition: margin-left 0.3s ease;
  }

  .content-wrapper {
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  .mobile-menu-btn {
    display: none;
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 1001;
    background: #667eea;
    border: none;
    border-radius: 8px;
    padding: 0.75rem;
    color: white;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
  }

  .mobile-menu-btn:hover {
    background: #5a6fd8;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  .hamburger {
    display: block;
    width: 20px;
    height: 2px;
    background: white;
    position: relative;
  }

  .hamburger::before,
  .hamburger::after {
    content: '';
    position: absolute;
    width: 20px;
    height: 2px;
    background: white;
    transition: all 0.3s ease;
  }

  .hamburger::before {
    top: -6px;
  }

  .hamburger::after {
    bottom: -6px;
  }

  .mobile-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
  }

  .auth-main {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .main-content {
      margin-left: 0;
    }

    .mobile-menu-btn {
      display: block;
    }

    .sidebar-wrapper {
      position: fixed;
      top: 0;
      left: 0;
      width: 250px;
      height: 100%;
      background: #fff;
      z-index: 1000;
      transform: translateX(-100%);
      transition: transform 0.3s ease;
    }

    .sidebar-wrapper.mobile-open {
      transform: translateX(0);
    }

    .content-wrapper {
      padding: 1rem;
      padding-top: 4rem; /* space for mobile menu button */
    }
  }

  @media (max-width: 480px) {
    .content-wrapper {
      padding: 0.75rem;
      padding-top: 4rem;
    }
  }
</style>
