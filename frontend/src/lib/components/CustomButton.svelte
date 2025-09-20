<script lang="ts">
	import { Button } from 'carbon-components-svelte';
	
	export let type: 'button' | 'submit' | 'reset' = 'button';
	export let kind: 'primary' | 'secondary' | 'tertiary' | 'ghost' | 'danger' = 'primary';
	export let size: 'small' | 'field' | 'lg' | 'xl' = 'field';
	export let fullWidth: boolean = false;
	export let variant: 'default' | 'secondary' 
	export let disabled: boolean = false;

	
	const baseStyles = 'display: flex; align-items: center; justify-content: center; text-align: unset; border-radius: 0.2rem; width: 100%; max-width: unset; padding: 0px 2rem;';
	
	const variants = {
        default: '',
		secondary: 'background: #ffffff;color: #2563eb; border: 1px solid #2563eb;',
	};
	
	$: buttonStyles = `${baseStyles} ${variants[variant] || variants.default} ${fullWidth ? 'width: 100%;' : ''}`;


</script>

<Button 
	{type} 
	{kind} 
	{size}
	{disabled}
	style={buttonStyles}
	on:click
    {...$$restProps}
>
	<slot />
</Button>