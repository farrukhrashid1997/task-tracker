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
- Node.js 18+ (for frontend development)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ticket-management-system
   ```

2. **Start Backend Services**
   ```bash
   # Start all backend services (PostgreSQL, Redis, RabbitMQ, Django, Celery)
   docker-compose up --build
   ```

3. **Run Database Setup**
   ```bash
   # Run migrations to create database tables
   docker-compose exec django python manage.py migrate
   ```

4. **Load Sample Data (Optional)**
   ```bash
   # Load test data for development
   docker-compose exec django python manage.py create_sample_data
   ```

5. **Start Frontend Development Server**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Access Points

- **Frontend Application**: http://localhost:5173
- **Django API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **RabbitMQ Management**: http://localhost:15672 (user: `ticket_user`, pass: `ticket_pass`)

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

## Known Issues & Improvements Needed

### Critical Fixes Required
1. **Sidebar hamburger menu** - Mobile menu button not working properly
2. **Missing API endpoints**:
   - Tickets over time data for line chart
   - Dropdown data API (users, priorities, statuses)

### Code Quality Improvements
1. **Add Django serializers** for tickets and accounts modules:
   - Automatic data validation
   - Reduced repetitive code
   - Better API consistency

2. **UI/UX improvements**:
   - Unify button styles across the application
   - Improve mobile responsiveness
   - Better error handling in frontend

### Missing Submission Requirements
1. **Testing**:
   - Unit tests for API endpoints
   - Frontend component tests
   - Celery task tests

2. **CI/CD Pipeline**:
   - Automated testing on commits
   - SAST/DAST security scanning

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

## Next Steps for Completion

1. Fix mobile hamburger menu
2. Implement missing API endpoints
3. Add Django serializers
4. Write comprehensive tests


