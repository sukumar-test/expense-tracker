# Expense Tracker

A simple web application for tracking personal expenses built with Python and Flask.

![CI/CD Status](https://github.com/your-username/expense-tracker/actions/workflows/cicd.yml/badge.svg)

## Features

- Add, edit, and delete expenses
- Categorize expenses
- Visualize expense distribution by category
- Track expense totals
- Responsive design for mobile and desktop
- Comprehensive test coverage with pytest
- Automated CI/CD pipeline with GitHub Actions
- Automatic deployment to Azure
- RESTful JSON API for programmatic access

## Documentation

This project includes comprehensive documentation:

- **[API Documentation](docs/API.md)** - Detailed API endpoint documentation and usage examples
- **[Architecture Guide](docs/ARCHITECTURE.md)** - Technical architecture and design decisions
- **[Testing Guide](docs/TESTING.md)** - How to run and write tests
- **[Contributing Guide](CONTRIBUTING.md)** - Developer setup and contribution guidelines

## Screenshots

(Screenshots will be available after running the application)

## Technologies Used

- Python
- Flask
- SQLAlchemy (SQLite database)
- Bootstrap 5
- Chart.js for visualizations
- HTML/CSS/JavaScript

## Installation and Setup

1. Clone this repository or download the files
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
expense-tracker/
├── app.py                 # Main application file
├── expenses.db            # SQLite database (created on first run)
├── requirements.txt       # Project dependencies
├── static/                # Static files
│   ├── css/
│   │   └── styles.css     # Custom CSS
│   └── js/
│       └── script.js      # Custom JavaScript
└── templates/             # HTML templates
    ├── add.html           # Add expense page
    ├── base.html          # Base template (layout)
    ├── categories.html    # Category visualization page
    ├── edit.html          # Edit expense page
    └── index.html         # Home page
```

## Usage

1. Add an expense by clicking "Add New Expense"
2. View all expenses on the home page
3. Edit or delete expenses using the action buttons
4. View category breakdown and charts in the "Categories" section

## Testing

The application has a comprehensive test suite built with pytest that achieves over 98% code coverage.

### Running Tests

1. Ensure you have installed test dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the tests:
   ```
   python -m pytest
   ```

3. Run the tests with coverage:
   ```
   python -m pytest --cov=app
   ```

4. Generate a coverage report:
   ```
   python -m pytest --cov=app --cov-report=html
   ```
   This will generate a coverage report in the `htmlcov` directory.

## CI/CD Pipeline

The application uses GitHub Actions for continuous integration and deployment to Azure. The pipeline performs the following steps:

1. Builds the application
2. Runs all tests with coverage reporting
3. Packages the application for deployment
4. Deploys to Azure Web App (when pushing to main/master branch)

### GitHub Secrets Required for Deployment

To enable automatic deployment to Azure, set up the following secrets in your GitHub repository:

- `AZURE_CREDENTIALS`: JSON credential object for Azure authentication
- `AZURE_WEBAPP_NAME`: The name of your Azure Web App
- `AZURE_RESOURCE_GROUP`: The name of your Azure resource group

## Future Enhancements

- User authentication and multi-user support
- Export expenses to CSV/Excel
- Monthly/yearly expense reports
- Budget setting and tracking
- Recurring expenses
- Mobile app integration

## License

MIT License
