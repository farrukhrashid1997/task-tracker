// lib/components/charts/ChartComponents.tsx
import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

interface ChartData {
	[key: string]: number;
}

interface StatusPieChartProps {
	data: ChartData;
}

interface PriorityBarChartProps {
	data: ChartData;
}

// Status Distribution Pie Chart
export function StatusPieChart({ data }: StatusPieChartProps) {
	const chartRef = useRef<HTMLCanvasElement>(null);
	const chartInstance = useRef<Chart | null>(null);

	useEffect(() => {
		if (chartInstance.current) {
			chartInstance.current.destroy();
		}

		if (!chartRef.current) return;
		const ctx = chartRef.current.getContext('2d');
		if (!ctx) return;

		const labels = Object.keys(data || {});
		const values = Object.values(data || {});
		chartInstance.current = new Chart(ctx, {
			type: 'pie',
			data: {
				labels: labels.map(
					(label) => label.charAt(0).toUpperCase() + label.slice(1).replace('_', ' ')
				),
				datasets: [
					{
						data: values,
						backgroundColor: [
							'#ef4444', // Red for open
							'#f59e0b', // Orange for in_progress
							'#10b981' // Green for closed
						],
						borderWidth: 2,
						borderColor: '#fff'
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: {
						position: 'bottom',
						labels: {
							padding: 20,
							usePointStyle: true,
							font: { size: 12 }
						}
					}
				}
			}
		});

		return () => {
			if (chartInstance.current) {
				chartInstance.current.destroy();
			}
		};
	}, [data]);

	return (
		<div style={{ position: 'relative', height: '300px', width: '100%' }}>
			<canvas ref={chartRef}></canvas>
		</div>
	);
}

// Priority Distribution Bar Chart
export function PriorityBarChart({ data }: PriorityBarChartProps) {
	const chartRef = useRef<HTMLCanvasElement>(null);
	const chartInstance = useRef<Chart | null>(null);

	useEffect(() => {
		if (chartInstance.current) {
			chartInstance.current.destroy();
		}

		if (!chartRef.current) return;
		const ctx = chartRef.current.getContext('2d');
		if (!ctx) return;

		const labels = Object.keys(data || {});
		const values = Object.values(data || {});

		chartInstance.current = new Chart(ctx, {
			type: 'bar',
			data: {
				labels: labels.map((label) => label.charAt(0).toUpperCase() + label.slice(1)),
				datasets: [
					{
						label: 'Tickets',
						data: values,
						backgroundColor: [
							'#dc2626', // Red for high
							'#ea580c', // Orange for medium
							'#16a34a' // Green for low
						],
						borderRadius: 6
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: { display: false }
				},
				scales: {
					y: {
						beginAtZero: true,
						ticks: { stepSize: 1 }
					}
				}
			}
		});

		return () => {
			if (chartInstance.current) {
				chartInstance.current.destroy();
			}
		};
	}, [data]);

	return (
		<div style={{ position: 'relative', height: '300px', width: '100%' }}>
			<canvas ref={chartRef}></canvas>
		</div>
	);
}
