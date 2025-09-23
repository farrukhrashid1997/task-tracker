# Ticket Management System

A full-stack ticket management application built with Svelte frontend and Django backend, featuring real-time notifications via Celery, Redis caching, and RabbitMQ message queuing.

## Architecture

- **Frontend**: Svelte 5 with TypeScript
- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Background Tasks**: Celery
- **Charts**: React components with Chart.js

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- Node.js 22+ (for frontend development)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ticket-management-system
   ```

2. **Kubernetes Setup**
   ```bash
      # Start minikube cluster
      minikube start
      
      # Configure Docker to use minikube's registry
      eval $(minikube docker-env)
      
      # Build the Django application image
      docker build -t django-ticket-app ./backend
      
      # Deploy all services (PostgreSQL, Redis, RabbitMQ, Django, Celery)
      kubectl apply -f kubernetes/ -R
      
      # Wait for Django pod to be ready
      kubectl wait --for=condition=ready pod -l app=django --timeout=300s
      
      # Run database migrations
      kubectl exec deployment/django-deployment -- python manage.py migrate
      
      # Forward Django service to localhost (keep this terminal open)
      # We'd use Ingress in production though.
      kubectl port-forward service/django-service 8000:8000
   ```

3. **Start Frontend Development Server**
   ```bash
   cd frontend
   nvm use 22
   npm install
   npm run dev
   ```


### Core Functionality
- User authentication with JWT cookies
- Ticket CRUD operations with comments
- Dashboard with statistics and React charts
- User profile management
- Email notifications via Celery background tasks
- Responsive design (mobile & desktop)

### Technical Features
- Redis caching for dashboard performance
- RabbitMQ message queuing for email tasks
- Real-time background task processing
- Type-safe APIs with TypeScript
- Docker containerization


## Project Structure
```
ticket-management-system/
├── backend/                # Django API
│   ├── tickets/           # Ticket management app
│   ├── accounts/          # User management app  
│   ├── dashboard/         # Dashboard statistics app
│   └── ticket_system/     # Main Django project
├── frontend/              # Svelte application
│   ├── src/lib/api/      # API client functions
│   ├── src/lib/components/ # Reusable components
│   └── src/routes/       # Page components
├── docker-compose.yml     # Service definitions
└── README.md             # This file
```


## Default Credentials
- **Admin User**: Created during setup step 3
- **RabbitMQ**: ticket_user / ticket_pass
- **Database**: ticket_user / ticket_pass / ticket_system




