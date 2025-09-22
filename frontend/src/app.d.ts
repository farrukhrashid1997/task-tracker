declare global {
	interface Window {
		google: {
			accounts: {
				id: {
					initialize: (config: any) => void;
					renderButton: (element: HTMLElement, config: any) => void;
				};
			};
		};
	}

	const google: Window['google'];

	interface GoogleCredentialResponse {
		credential: string;
		select_by: string;
	}

	interface GoogleButtonConfig {
		theme: 'outline' | 'filled_blue' | 'filled_black';
		size: 'large' | 'medium' | 'small';
		text: 'signin_with' | 'signup_with' | 'continue_with' | 'signin';
		width: string | number;
	}

	interface GoogleAuthResult {
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
}

export {};
