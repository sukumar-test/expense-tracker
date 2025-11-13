# Architecture Documentation

This document describes the architecture and design of the Expense Tracker application.

## Overview

Expense Tracker is a web-based application built using the Flask framework. It follows the Model-View-Controller (MVC) architectural pattern and uses SQLAlchemy as the ORM for database operations.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
│                     (HTML/CSS/JavaScript)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Flask Application                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routes     │  │   Models     │  │  Templates   │     │
│  │ (app.py)     │──│ (Expense)    │──│  (Jinja2)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       SQLAlchemy ORM                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      SQLite Database                         │
│                      (expenses.db)                           │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Python 3.x**: Programming language
- **Flask 2.0.1**: Lightweight web framework
- **Flask-SQLAlchemy 2.5.1**: ORM extension for Flask
- **SQLAlchemy 1.4.23**: Database toolkit and ORM
- **SQLite**: Embedded database

### Frontend
- **HTML5**: Markup language
- **CSS3**: Styling
- **Bootstrap 5**: CSS framework for responsive design
- **JavaScript**: Client-side scripting
- **Chart.js**: Data visualization library

### Testing
- **pytest 7.4.0**: Testing framework
- **pytest-flask 1.2.0**: Flask testing utilities
- **pytest-cov 4.1.0**: Coverage reporting
- **coverage 7.3.0**: Code coverage measurement

## Application Components

### 1. Application Layer (app.py)

The main application file contains:

#### Configuration
- Flask app initialization
- Secret key for session management
- Database URI configuration
- SQLAlchemy settings

#### Data Model
- **Expense Model**: Represents expense entries with fields:
  - `id`: Primary key (auto-increment)
  - `title`: Expense title (String, max 100 chars)
  - `amount`: Expense amount (Float)
  - `category`: Expense category (String, max 50 chars)
  - `date`: Date of expense (Date, defaults to current date)
  - `description`: Optional description (Text)

#### Routes
- `GET /`: Home page listing all expenses
- `GET/POST /add`: Add new expense
- `GET/POST /edit/<id>`: Edit existing expense
- `GET /delete/<id>`: Delete expense
- `GET /categories`: View expense breakdown by category
- `GET /api/expenses`: REST API endpoint for expenses

### 2. View Layer (templates/)

Jinja2 templates provide the user interface:

- **base.html**: Base template with common layout and navigation
- **index.html**: Home page with expense list
- **add.html**: Form for adding new expenses
- **edit.html**: Form for editing existing expenses
- **categories.html**: Category breakdown with charts

### 3. Static Assets (static/)

- **CSS** (`static/css/styles.css`): Custom styling
- **JavaScript** (`static/js/script.js`): Client-side logic

### 4. Database Layer

- **SQLite database** (`expenses.db`): Persistent storage
- **SQLAlchemy ORM**: Object-relational mapping
- **Automatic table creation**: Database tables are created on first run

## Design Patterns

### MVC Pattern
- **Model**: Expense class (data structure and database operations)
- **View**: Jinja2 templates (presentation layer)
- **Controller**: Flask routes (business logic and request handling)

### Repository Pattern
- SQLAlchemy provides abstraction over database operations
- Models encapsulate data access logic

### Template Inheritance
- Base template (`base.html`) provides common structure
- Child templates extend the base template

## Data Flow

### Adding an Expense
1. User clicks "Add New Expense"
2. Browser requests `/add` (GET)
3. Flask renders `add.html` template
4. User fills form and submits
5. Browser sends POST request to `/add`
6. Flask validates and creates Expense object
7. SQLAlchemy inserts record into database
8. Flask redirects to home page
9. Success message displayed via flash

### Viewing Expenses
1. User navigates to home page
2. Browser requests `/` (GET)
3. Flask queries all expenses from database
4. SQLAlchemy returns Expense objects
5. Flask calculates total amount
6. Template renders expense list
7. Browser displays formatted HTML

### API Access
1. Client sends GET request to `/api/expenses`
2. Flask queries all expenses
3. Converts Expense objects to dictionaries
4. Returns JSON response

## Security Considerations

### Current Implementation
- Flask secret key for session security
- SQL injection prevention via SQLAlchemy ORM
- CSRF protection via Flask forms (recommended to add)

### Future Enhancements
- User authentication and authorization
- Input validation and sanitization
- Password hashing (bcrypt/argon2)
- Rate limiting for API endpoints
- HTTPS enforcement in production

## Scalability

### Current Limitations
- Single-user application
- SQLite database (not suitable for high concurrency)
- No caching mechanism
- Synchronous request handling

### Scaling Strategy
For larger deployments, consider:
1. **Database**: Migrate to PostgreSQL/MySQL
2. **Authentication**: Implement user accounts
3. **Caching**: Add Redis for session/data caching
4. **Async**: Use async routes for I/O operations
5. **Load Balancing**: Deploy multiple instances behind load balancer
6. **CDN**: Serve static assets via CDN

## Deployment Architecture

### Development
- Local Flask development server
- SQLite database
- Debug mode enabled

### Production (Azure)
```
┌─────────────────────────────────────────┐
│         Azure Load Balancer             │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        Azure Web App Service            │
│  ┌────────────────────────────────┐    │
│  │   Flask App (Gunicorn/uWSGI)   │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Persistent Storage / Database       │
└─────────────────────────────────────────┘
```

## Error Handling

- Flask flash messages for user feedback
- HTTP error codes for API responses
- Database transaction rollback on errors
- 404 error handling for missing resources

## Testing Architecture

- **Unit Tests**: Test individual functions and models
- **Integration Tests**: Test route handlers and database operations
- **Test Fixtures**: Reusable test setup (conftest.py)
- **Test Coverage**: >98% code coverage
- **CI/CD**: Automated testing on every commit

## Performance Considerations

### Current Optimizations
- SQLAlchemy lazy loading
- Simple queries without complex joins
- Minimal JavaScript for fast page loads

### Monitoring
- Application logging (can be enhanced)
- Error tracking (recommended: Sentry)
- Performance monitoring (recommended: New Relic)

## Future Architecture Improvements

1. **Microservices**: Separate API and frontend
2. **Message Queue**: Async task processing (Celery + Redis)
3. **Search**: Add Elasticsearch for expense search
4. **Analytics**: Separate analytics service
5. **Mobile**: Native mobile apps or PWA
6. **Multi-tenancy**: Support for multiple users/organizations
