import { env } from '$env/dynamic/public';

interface LoginResponse {
	message: string;
	user: {
		id: number;
		username: string;
		email: string;
		first_name: string;
		last_name: string;
		role: string;
	};
}



interface RegisterResponse {
	message: string;
	user: {
		id: number;
		username: string;
		email: string;
		first_name: string;
		last_name: string;
		role: string;
	};
}


export async function loginUser(username: string, password: string): Promise<LoginResponse> {
	const response = await fetch(`${env.PUBLIC_API_BASE_URL}/auth/login/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			username: username,
			password: password
		}),
		credentials: 'include' 
	});

	if (!response.ok) {
		throw new Error('Login failed');
	}

	return response.json();
}

export async function checkAuthStatus() {
	const response = await fetch(`${env.PUBLIC_API_BASE_URL}/auth/profile/`, {
		method: 'GET',
		credentials: 'include'
	});

	if (!response.ok) {
		throw new Error('Not authenticated');
	}

	return response.json();
}


export async function logoutUser(): Promise<void> {
	const response = await fetch(`${env.PUBLIC_API_BASE_URL}/auth/logout/`, {
		method: 'POST',
		credentials: 'include' // 🔒 Sends cookies for authentication
	});

	if (!response.ok) {
		throw new Error('Logout failed');
	}
}


export async function registerUser(
	username: string, 
	email: string, 
	password: string, 
	firstName: string, 
	lastName: string, 
	role: string
): Promise<RegisterResponse> {
	const response = await fetch(`${env.PUBLIC_API_BASE_URL}/auth/register/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			username,
			email,
			password,
			first_name: firstName,
			last_name: lastName,
			role
		}),
		credentials: 'include'
	});

	if (!response.ok) {
		const errorData = await response.json();
		throw new Error(errorData.error || 'Registration failed');
	}

	return response.json();
}