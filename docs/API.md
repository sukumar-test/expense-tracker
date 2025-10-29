# API Documentation

## Overview

The Expense Tracker application provides both a web interface and a RESTful JSON API for accessing expense data. This document describes all available endpoints.

## Base URL

When running locally: `http://localhost:5000`

## Web Routes

### Home Page

**Endpoint:** `GET /`

**Description:** Displays the main page with a list of all expenses sorted by date (newest first).

**Response:** HTML page

**Features:**
- List of all expenses
- Total amount calculation
- Quick action buttons (Edit/Delete)

**Example:** Navigate to `http://localhost:5000/` in your browser

---

### Add Expense

**Endpoint:** `GET /add` | `POST /add`

**Description:** Add a new expense to the tracker.

#### GET Request
- Displays the form to add a new expense
- Pre-fills the date field with today's date

#### POST Request
- Creates a new expense record in the database

**Form Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes | Short name of the expense (max 100 chars) |
| amount | float | Yes | Cost of the expense |
| category | string | Yes | Expense category (max 50 chars) |
| date | string | No | Date in YYYY-MM-DD format (defaults to today) |
| description | string | No | Detailed description of the expense |

**Success Response:**
- Redirects to `/` (home page)
- Flash message: "Expense added successfully!"

**Example Form Submission:**
```html
POST /add
Content-Type: application/x-www-form-urlencoded

title=Grocery+Shopping&amount=150.75&category=Food&date=2025-05-01&description=Weekly+groceries
```

---

### Edit Expense

**Endpoint:** `GET /edit/<id>` | `POST /edit/<id>`

**Description:** Edit an existing expense.

#### GET Request
- Displays the edit form with pre-filled expense data
- Returns 404 if expense ID doesn't exist

#### POST Request
- Updates the expense record in the database

**URL Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Unique identifier of the expense |

**Form Parameters:** (Same as Add Expense)

**Success Response:**
- Redirects to `/` (home page)
- Flash message: "Expense updated successfully!"

**Error Response:**
- 404 Not Found if expense doesn't exist

**Example:**
```
GET /edit/5
POST /edit/5 with form data
```

---

### Delete Expense

**Endpoint:** `GET /delete/<id>`

**Description:** Delete an expense from the database.

**URL Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Unique identifier of the expense to delete |

**Success Response:**
- Redirects to `/` (home page)
- Flash message: "Expense deleted successfully!"

**Error Response:**
- 404 Not Found if expense doesn't exist

**Example:**
```
GET /delete/5
```

**Note:** The application includes client-side JavaScript confirmation before deletion.

---

### Categories Summary

**Endpoint:** `GET /categories`

**Description:** Displays expense breakdown by category with totals.

**Response:** HTML page

**Features:**
- Aggregated spending by category
- Visual chart representation
- Total amount per category

**Example:** Navigate to `http://localhost:5000/categories`

---

## REST API Endpoints

### Get All Expenses (JSON)

**Endpoint:** `GET /api/expenses`

**Description:** Retrieve all expenses as a JSON array. Expenses are sorted by date (newest first).

**Response Format:** JSON array

**Success Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "title": "Grocery Shopping",
    "amount": 150.75,
    "category": "Food",
    "date": "2025-05-01",
    "description": "Weekly groceries"
  },
  {
    "id": 2,
    "title": "Electric Bill",
    "amount": 87.30,
    "category": "Utilities",
    "date": "2025-05-05",
    "description": "Monthly electricity bill"
  }
]
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| title | string | Expense title |
| amount | float | Expense amount |
| category | string | Expense category |
| date | string | Date in YYYY-MM-DD format |
| description | string | Expense description (can be null) |

**Example Using cURL:**
```bash
curl http://localhost:5000/api/expenses
```

**Example Using JavaScript:**
```javascript
fetch('http://localhost:5000/api/expenses')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Example Using Python:**
```python
import requests

response = requests.get('http://localhost:5000/api/expenses')
expenses = response.json()
print(expenses)
```

---

## Error Handling

The application returns standard HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 302 | Redirect (after successful form submission) |
| 404 | Resource not found (invalid expense ID) |
| 500 | Internal server error |

## Data Validation

### Required Fields
- `title`: Cannot be empty
- `amount`: Must be a valid number
- `category`: Cannot be empty

### Data Types
- `amount`: Converted to float, must be numeric
- `date`: Must be in YYYY-MM-DD format if provided

### Error Handling
- Invalid data types will raise a `ValueError`
- Missing required fields may result in database constraint errors
- Invalid expense IDs return 404 errors

## Common Categories

While categories are free-form text, here are some commonly used categories:
- Food
- Transportation
- Utilities
- Entertainment
- Healthcare
- Shopping
- Housing
- Education
- Travel
- Other

## Notes

- All amounts are stored as floating-point numbers
- Dates are stored as date objects in the database but returned as strings in the API
- The application uses UTC for date/time operations
- Flash messages use Bootstrap alert classes (success, danger, etc.)
