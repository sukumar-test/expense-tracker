# User Guide

Welcome to the Expense Tracker User Guide! This comprehensive guide will help you get the most out of the application.

## Table of Contents

- [Getting Started](#getting-started)
- [Dashboard Overview](#dashboard-overview)
- [Managing Expenses](#managing-expenses)
- [Categories and Analytics](#categories-and-analytics)
- [Tips and Best Practices](#tips-and-best-practices)
- [Frequently Asked Questions](#frequently-asked-questions)

## Getting Started

### Accessing the Application

1. **Local Installation**: If running locally, navigate to `http://localhost:5000` in your web browser
2. **Deployed Version**: Access via your deployment URL (e.g., Azure Web App URL)

### First-Time Setup

When you first open the application:
1. You'll see an empty expense list
2. The database is automatically created
3. You're ready to start adding expenses

No registration or login is required in the current version.

## Dashboard Overview

The main dashboard (`Home` page) displays:

### Header
- **Application Title**: "Expense Tracker"
- **Navigation Menu**: Links to Home, Categories, and Add Expense

### Expense List
- **Table View**: All your expenses in a formatted table
- **Columns**:
  - Date: When the expense occurred
  - Title: Name of the expense
  - Category: Expense category
  - Amount: Cost in dollars
  - Actions: Edit and Delete buttons

### Summary
- **Total Expenses**: Sum of all recorded expenses displayed at the top

### Empty State
- If no expenses exist, you'll see a message prompting you to add your first expense

## Managing Expenses

### Adding a New Expense

1. **Navigate to Add Expense**
   - Click "Add New Expense" button on the home page
   - Or click "Add Expense" in the navigation menu

2. **Fill in the Form**
   - **Title** (Required): Enter a descriptive name for the expense
     - Example: "Grocery Shopping", "Gas", "Coffee"
   - **Amount** (Required): Enter the cost in dollars
     - Example: 45.50, 12.99
   - **Category** (Required): Select from the dropdown
     - Options: Food & Dining, Transportation, Shopping, Entertainment, Bills & Utilities, Healthcare, Travel, Education, Other
   - **Date** (Optional): Select the date of the expense
     - Defaults to today's date if not specified
   - **Description** (Optional): Add any additional details
     - Example: "Weekly groceries from Walmart"

3. **Submit**
   - Click the "Add Expense" button
   - You'll be redirected to the home page
   - A success message will confirm the expense was added

### Editing an Expense

1. **Locate the Expense**
   - Find the expense in the list on the home page

2. **Click Edit**
   - Click the blue "Edit" button next to the expense

3. **Modify Details**
   - Update any field as needed
   - All fields are pre-filled with current values

4. **Save Changes**
   - Click "Update Expense"
   - You'll be redirected to the home page
   - A success message will confirm the update

### Deleting an Expense

1. **Locate the Expense**
   - Find the expense in the list on the home page

2. **Click Delete**
   - Click the red "Delete" button next to the expense

3. **Confirmation**
   - The expense is immediately deleted
   - A confirmation message will appear
   - The total is automatically recalculated

**Note**: Deletion is permanent and cannot be undone. Make sure you want to delete the expense before clicking.

## Categories and Analytics

### Viewing Category Breakdown

1. **Navigate to Categories**
   - Click "Categories" in the navigation menu

2. **View the Analysis**
   - **Category Table**: Shows each category with total amount spent
   - **Visual Chart**: Pie chart showing expense distribution
   - **Summary**: Quick overview of spending by category

### Understanding Categories

The application provides predefined categories to help organize your expenses:

- **Food & Dining**: Restaurants, groceries, coffee, etc.
- **Transportation**: Gas, public transit, parking, car maintenance
- **Shopping**: Clothing, electronics, household items
- **Entertainment**: Movies, concerts, hobbies, games
- **Bills & Utilities**: Rent, electricity, water, internet
- **Healthcare**: Medical bills, prescriptions, insurance
- **Travel**: Hotels, flights, vacation expenses
- **Education**: Books, courses, tuition
- **Other**: Miscellaneous expenses that don't fit other categories

### Using the Chart

The pie chart provides a visual representation of your spending:
- Each slice represents a category
- Hover over slices to see exact amounts
- Larger slices indicate higher spending in that category
- Use this to identify where most of your money goes

## Tips and Best Practices

### Recording Expenses

1. **Be Consistent**
   - Record expenses as soon as they occur
   - Don't wait until the end of the week or month
   - Regular recording ensures accurate tracking

2. **Be Specific**
   - Use clear, descriptive titles
   - Good: "Weekly groceries - Safeway"
   - Avoid: "Shopping", "Stuff"

3. **Use Descriptions**
   - Add context in the description field
   - Note what you purchased or why
   - Helps when reviewing expenses later

4. **Categorize Accurately**
   - Choose the most appropriate category
   - Be consistent with categorization
   - This makes analytics more useful

### Reviewing Expenses

1. **Regular Reviews**
   - Check your expenses weekly or monthly
   - Look for spending patterns
   - Identify areas to reduce spending

2. **Use the Categories Page**
   - Regularly review category breakdown
   - Identify your highest spending categories
   - Set goals to reduce spending in specific areas

3. **Check for Duplicates**
   - Occasionally scan for duplicate entries
   - Delete any accidental duplicates

### Data Management

1. **Edit for Accuracy**
   - Fix any errors immediately
   - Correct amounts, dates, or categories
   - Accurate data leads to better insights

2. **Don't Over-Categorize**
   - Use "Other" for truly miscellaneous items
   - Don't force items into inappropriate categories
   - Keep categorization simple and logical

## Frequently Asked Questions

### General Questions

**Q: Do I need to create an account?**
A: No, the current version doesn't require user accounts. All expenses are stored locally.

**Q: Can multiple people use the same application?**
A: Currently, the application is single-user. All users accessing the same deployment will see the same expenses.

**Q: Where is my data stored?**
A: Data is stored in a SQLite database file (`expenses.db`) on the server.

### Using the Application

**Q: Can I import expenses from a CSV file?**
A: This feature is not currently available but is planned for a future release.

**Q: Can I export my expenses?**
A: Export functionality is not currently available but is planned for future development.

**Q: What date format should I use?**
A: The application uses the standard date picker. Click the date field to select from a calendar.

**Q: Can I add custom categories?**
A: Currently, only predefined categories are available. Custom categories may be added in a future release.

**Q: How many expenses can I add?**
A: There's no hard limit, but performance may vary with very large numbers of expenses (thousands).

### Data and Privacy

**Q: Is my data secure?**
A: The application stores data in a local database. For deployed versions, ensure your hosting platform provides appropriate security measures.

**Q: Can I backup my data?**
A: For local installations, you can backup the `expenses.db` file. For deployed versions, consult your hosting provider's backup options.

**Q: What happens if I delete the database file?**
A: All your expense data will be lost. A new empty database will be created on the next run.

### Troubleshooting

**Q: The page is blank or not loading**
A: 
- Check that the application is running
- Verify you're using the correct URL
- Try refreshing the page
- Clear browser cache if needed

**Q: I get an error when adding an expense**
A:
- Ensure all required fields are filled (Title, Amount, Category)
- Check that the amount is a valid number
- Try using a different browser

**Q: The total amount seems incorrect**
A:
- Refresh the page to recalculate
- Check for duplicate entries
- Verify all expense amounts are correct

**Q: Changes aren't saving**
A:
- Ensure you click the submit/save button
- Check that the application has write access to the database
- Look for any error messages

## Features Coming Soon

Future releases will include:

1. **User Authentication**: Personal accounts and login
2. **Data Export**: Export to CSV, Excel, or PDF
3. **Budget Tracking**: Set and monitor budgets
4. **Recurring Expenses**: Automatically add regular expenses
5. **Reports**: Monthly and yearly spending reports
6. **Search and Filter**: Find specific expenses quickly
7. **Mobile App**: Native apps for iOS and Android
8. **Custom Categories**: Create your own expense categories
9. **Multi-Currency**: Support for different currencies
10. **Receipt Upload**: Attach receipt images to expenses

## Getting Help

If you encounter issues or have questions:

1. **Check this guide**: Many common questions are answered here
2. **Review the README**: The README.md file has additional information
3. **Check GitHub Issues**: See if others have reported similar problems
4. **Open an Issue**: Report bugs or request features on GitHub
5. **Contact Support**: Reach out to the development team

## Conclusion

Thank you for using Expense Tracker! We hope this guide helps you effectively manage your personal finances. 

Happy tracking! 💰📊
