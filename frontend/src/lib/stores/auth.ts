import { writable } from 'svelte/store';
import { loginUser, logoutUser, checkAuthStatus, registerUser } from '../api/auth';

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

export async function login(
	username: string,
	password: string
): Promise<{ success: boolean; error?: string }> {
	try {
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
		await logoutUser();
		user.set(null);
		isAuthenticated.set(false);
	} catch (error) {
		console.error('Logout error:', error);
		user.set(null);
		isAuthenticated.set(false);
	}
}

export async function register(
	username: string,
	email: string,
	password: string,
	firstName: string,
	lastName: string,
	role: string
): Promise<{ success: boolean; error?: string }> {
	try {
		const response = await registerUser(username, email, password, firstName, lastName, role);
		user.set(response.user);
		isAuthenticated.set(true);

		return { success: true };
	} catch (error) {
		return { success: false, error: (error as Error).message };
	}
}
