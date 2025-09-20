import { writable } from 'svelte/store';


interface User {
	id: number;
	username: string;
	email: string;
	first_name: string;
	last_name: string;
	role: string;
}

export const isAuthenticated = writable<boolean>(false);
export const user = writable<User | null>(null);
export const authLoading = writable<boolean>(true);




export async function checkAuth(): Promise<void> {
	try {
		const { checkAuthStatus } = await import('../api/auth');
		const response = await checkAuthStatus();
		user.set(response.user);
		isAuthenticated.set(true);
	} catch (error) {
		user.set(null);
		isAuthenticated.set(false);
	} finally {
		authLoading.set(false);
	}
}

export async function login(username: string, password: string): Promise<{ success: boolean; error?: string }> {
	try {
		const { loginUser } = await import('../api/auth');
		
		const response = await loginUser(username, password);
		user.set(response.user);
		isAuthenticated.set(true);
		
		return { success: true };
	} catch (error) {
		return { success: false, error: (error as Error).message };
	}
}

export async function logout(): Promise<void> {
	try {
		const { logoutUser } = await import('../api/auth');
		await logoutUser();
		user.set(null);
		isAuthenticated.set(false);
	} catch (error) {
		console.error('Logout error:', error);
		user.set(null);
		isAuthenticated.set(false);
	}
}

