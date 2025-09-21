<!-- lib/components/charts/ChartWrapper.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { createRoot } from 'react-dom/client';
	import { createElement } from 'react';

	let { component, data, ...props } = $props();
	let containerElement: HTMLDivElement;
	let root: any;

	onMount(() => {
		// Create React root and render the component
		root = createRoot(containerElement);
		renderChart();

		return () => {
			if (root) {
				root.unmount();
			}
		};
	});

	$effect(() => {
		// Re-render when data changes
		if (root && containerElement) {
			renderChart();
		}
	});

	function renderChart() {
		if (root && component) {
			const reactElement = createElement(component, { data, ...props });
			root.render(reactElement);
		}
	}
</script>

<div bind:this={containerElement}></div>