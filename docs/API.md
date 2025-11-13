# API Documentation

This document describes the REST API endpoints available in the Expense Tracker application.

## Base URL

When running locally: `http://localhost:5000`

## Endpoints

### Get All Expenses

Returns a JSON array of all expenses in the database.

**Endpoint:** `/api/expenses`

**Method:** `GET`

**Authentication:** None (currently)

**Response:**

```json
[
  {
    "id": 1,
    "title": "Grocery Shopping",
    "amount": 85.50,
    "category": "Food",
    "date": "2025-11-10",
    "description": "Weekly groceries from supermarket"
  },
  {
    "id": 2,
    "title": "Gas",
    "amount": 45.00,
    "category": "Transportation",
    "date": "2025-11-11",
    "description": "Gas station fill-up"
  }
]
```

**Status Codes:**
- `200 OK` - Success

**Example Request:**

```bash
curl http://localhost:5000/api/expenses
```

**Example Response:**

```json
[
  {
    "id": 1,
    "title": "Coffee",
    "amount": 5.50,
    "category": "Food",
    "date": "2025-11-13",
    "description": "Morning coffee"
  }
]
```

## Data Models

### Expense

Represents a single expense entry.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Auto | Unique identifier |
| title | String (100) | Yes | Expense title |
| amount | Float | Yes | Expense amount in dollars |
| category | String (50) | Yes | Expense category |
| date | Date | No | Date of expense (defaults to current date) |
| description | Text | No | Additional details about the expense |

## Categories

The application supports the following predefined categories:
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Travel
- Education
- Other

## Error Handling

The API currently returns standard HTTP status codes:

- `200 OK` - Request successful
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Future API Endpoints

The following endpoints are planned for future releases:

- `POST /api/expenses` - Create a new expense
- `GET /api/expenses/{id}` - Get a specific expense
- `PUT /api/expenses/{id}` - Update an expense
- `DELETE /api/expenses/{id}` - Delete an expense
- `GET /api/categories` - Get category summary
- `GET /api/stats` - Get expense statistics

## Authentication

Currently, the API does not require authentication. Future versions will implement:
- User authentication via JWT tokens
- API key authentication for external integrations
- Role-based access control (RBAC)

## Rate Limiting

No rate limiting is currently implemented. This will be added in future versions to prevent abuse.

## CORS

Cross-Origin Resource Sharing (CORS) is not currently configured. If you need to access the API from a different domain, you'll need to configure CORS headers.
