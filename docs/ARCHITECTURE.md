# Architecture Documentation

## Overview

The Expense Tracker is a web-based application built using the Flask framework in Python. It follows a simple MVC (Model-View-Controller) pattern and uses SQLite for data persistence.

## Technology Stack

### Backend
- **Python 3.x**: Core programming language
- **Flask 2.0.1**: Lightweight web framework
- **SQLAlchemy 1.4.23**: ORM (Object-Relational Mapping) for database operations
- **Flask-SQLAlchemy 2.5.1**: Flask integration for SQLAlchemy

### Frontend
- **HTML5**: Markup structure
- **Bootstrap 5.3.0**: CSS framework for responsive design
- **JavaScript (ES6+)**: Client-side interactivity
- **Chart.js**: Data visualization for category charts

### Database
- **SQLite**: Lightweight, file-based relational database

### Testing
- **pytest 7.4.0**: Testing framework
- **pytest-flask 1.2.0**: Flask-specific testing utilities
- **pytest-cov 4.1.0**: Code coverage reporting

### Development Tools
- **Git**: Version control
- **GitHub Actions**: CI/CD pipeline
- **Azure Web Apps**: Hosting platform

## Application Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Browser                       │
│  (HTML/CSS/JavaScript + Bootstrap + Chart.js)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────────┐
│                      Flask Application                       │
│                        (app.py)                              │
│                                                              │
│  ┌────────────┐   ┌────────────┐   ┌──────────────┐        │
│  │   Routes   │───│   Models   │───│  Templates   │        │
│  │ (Views)    │   │  (Expense) │   │   (Jinja2)   │        │
│  └────────────┘   └────────────┘   └──────────────┘        │
│                          │                                   │
│                    SQLAlchemy ORM                            │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    SQLite Database                           │
│                    (expenses.db)                             │
│                                                              │
│  ┌─────────────────────────────────────────────────┐        │
│  │              Expense Table                      │        │
│  │  - id (Primary Key)                             │        │
│  │  - title                                        │        │
│  │  - amount                                       │        │
│  │  - category                                     │        │
│  │  - date                                         │        │
│  │  - description                                  │        │
│  └─────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
expense-tracker/
│
├── app.py                      # Main application file (routes, models, config)
├── requirements.txt            # Python dependencies
├── run.sh                      # Shell script to run the application
├── run_tests.py                # Script to run tests with coverage
├── pytest.ini                  # Pytest configuration
│
├── static/                     # Static assets
│   ├── css/
│   │   └── styles.css          # Custom CSS styles
│   └── js/
│       └── script.js           # Custom JavaScript
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Base template with common layout
│   ├── index.html              # Home page (expense list)
│   ├── add.html                # Add expense form
│   ├── edit.html               # Edit expense form
│   └── categories.html         # Category breakdown page
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Test configuration and fixtures
│   ├── test_app_setup.py       # Application configuration tests
│   ├── test_models.py          # Database model tests
│   ├── test_routes.py          # Route/endpoint tests
│   └── test_edge_cases.py      # Error handling tests
│
├── docs/                       # Documentation
│   ├── API.md                  # API documentation
│   ├── ARCHITECTURE.md         # This file
│   └── TESTING.md              # Testing guide
│
├── .github/                    # GitHub configuration
│   └── workflows/
│       └── cicd.yml            # CI/CD pipeline
│
├── README.md                   # Project overview
├── CONTRIBUTING.md             # Developer guide
└── .gitignore                  # Git ignore rules
```

## Core Components

### 1. Application Entry Point (app.py)

The `app.py` file serves as the main application module and contains:

#### Configuration
- Flask app initialization
- Secret key for session management
- Database URI configuration
- SQLAlchemy settings

#### Data Model
- **Expense Model**: Represents an expense record with fields:
  - `id`: Auto-incrementing primary key
  - `title`: Expense name (string, max 100 chars)
  - `amount`: Cost (float)
  - `category`: Category classification (string, max 50 chars)
  - `date`: Date of expense (date object)
  - `description`: Optional details (text)

#### Routes/Endpoints
- `GET /`: Home page with expense list
- `GET/POST /add`: Add new expense
- `GET/POST /edit/<id>`: Edit existing expense
- `GET /delete/<id>`: Delete expense
- `GET /categories`: Category breakdown
- `GET /api/expenses`: JSON API for expenses

### 2. Database Layer

#### ORM Pattern
The application uses SQLAlchemy ORM to abstract database operations:
- Models are defined as Python classes
- Database queries use Pythonic syntax
- Automatic SQL generation
- Built-in connection pooling

#### Database Schema

```sql
CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    description TEXT
);
```

#### Data Persistence
- SQLite database stored as `expenses.db` file
- Database created automatically on first run
- No migration files needed (simple schema)

### 3. View Layer (Templates)

#### Template Inheritance
- `base.html`: Master template with navigation, footer, and flash messages
- Other templates extend base.html using Jinja2 `{% extends %}`

#### Template Features
- Server-side rendering with Jinja2
- Template variables: `{{ variable }}`
- Control structures: `{% if %}`, `{% for %}`
- Flash message display
- Form rendering with CSRF protection

### 4. Static Assets

#### CSS (static/css/styles.css)
- Custom styles for cards, tables, badges
- Responsive design adjustments
- Hover effects and transitions
- Mobile-first breakpoints

#### JavaScript (static/js/script.js)
- Bootstrap tooltip initialization
- Auto-fill today's date in date inputs
- Confirmation dialogs for delete actions
- Client-side form enhancements

## Data Flow

### Adding an Expense

1. **User Action**: User navigates to `/add` and fills out the form
2. **Client Validation**: Browser validates required fields
3. **Form Submission**: POST request sent to `/add` with form data
4. **Server Processing**: 
   - Flask receives request
   - Extracts form data
   - Creates Expense object
   - Validates data types (amount → float, date → datetime)
5. **Database Operation**: SQLAlchemy adds record to database
6. **Response**: Redirect to home page with success message
7. **Display**: Updated expense list shown to user

### Viewing Expenses

1. **User Action**: User navigates to `/`
2. **Query**: SQLAlchemy queries all expenses, ordered by date
3. **Aggregation**: Total amount calculated in Python
4. **Rendering**: Jinja2 template rendered with expense data
5. **Response**: HTML page sent to browser

### Category Breakdown

1. **User Action**: User navigates to `/categories`
2. **Query**: All expenses retrieved from database
3. **Aggregation**: Python dictionary aggregates amounts by category
4. **Rendering**: Template renders category list
5. **Visualization**: Chart.js creates visual representation

## Security Considerations

### Current Implementation
- **Session Secret**: Used for flash messages and session security
- **SQL Injection Prevention**: SQLAlchemy ORM parameterizes queries
- **CSRF Protection**: Disabled in current version (should be enabled for production)

### Recommended Enhancements for Production
1. Use environment variables for secret key
2. Enable CSRF protection
3. Add input sanitization
4. Implement user authentication
5. Use HTTPS in production
6. Add rate limiting
7. Validate file uploads if added
8. Use prepared statements for all queries

## Scalability Considerations

### Current Limitations
- SQLite suitable for small to medium datasets
- No user authentication (single-user application)
- No caching layer
- Synchronous request handling

### Scaling Options
1. **Database**: Migrate to PostgreSQL or MySQL for concurrent access
2. **Caching**: Add Redis for session storage and caching
3. **Authentication**: Implement user accounts with Flask-Login
4. **API**: Separate frontend/backend with RESTful API
5. **Async**: Use async/await for database operations
6. **Load Balancing**: Deploy multiple instances behind a load balancer

## Deployment Architecture

### Local Development
```
Developer Machine
├── Virtual Environment (venv)
├── SQLite Database (expenses.db)
└── Flask Development Server (port 5000)
```

### Production Deployment (Azure)
```
Azure Web App
├── Linux Container
├── Python Runtime
├── Gunicorn WSGI Server
├── SQLite Database (persistent storage)
└── Application Files (from git repository)
```

### CI/CD Pipeline
1. **Trigger**: Push to main/master branch
2. **Build**: GitHub Actions runs tests
3. **Test**: pytest with coverage reporting
4. **Package**: Create deployment archive
5. **Deploy**: Push to Azure Web App
6. **Validate**: Health check endpoint

## Error Handling

### HTTP Error Codes
- **404**: Resource not found (invalid expense ID)
- **500**: Internal server error (database errors, exceptions)

### Exception Handling
- ValueError: Invalid data types (non-numeric amount, invalid date)
- Database errors: Caught by SQLAlchemy
- Flash messages: User-friendly error notifications

## Performance Characteristics

### Database Queries
- **Index**: Primary key on expense ID (automatic)
- **Sorting**: ORDER BY date DESC for recent expenses first
- **Aggregation**: In-memory Python aggregation for categories

### Response Times (Typical)
- Home page: < 100ms
- Add/Edit/Delete: < 50ms
- Category page: < 150ms
- API endpoint: < 50ms

### Optimization Opportunities
1. Add database indexes on frequently queried fields (category, date)
2. Implement pagination for large expense lists
3. Cache category aggregations
4. Use database-level aggregation instead of Python
5. Lazy loading for related data

## Future Architecture Enhancements

1. **Microservices**: Separate API from web interface
2. **Message Queue**: Async processing for reports and exports
3. **CDN**: Serve static assets from CDN
4. **Docker**: Containerized deployment
5. **Multi-tenancy**: Support multiple users/organizations
6. **Real-time Updates**: WebSocket for live expense updates
7. **Mobile App**: Native or PWA for mobile devices
