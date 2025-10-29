/**
 * @fileoverview Custom JavaScript for the Expense Tracker application.
 * 
 * This script provides client-side functionality for the expense tracker including:
 * - Initializing Bootstrap tooltips
 * - Setting default date values for date inputs
 * - Adding confirmation dialogs for delete actions
 * 
 * @author Expense Tracker Team
 * @version 1.0.0
 */

/**
 * Initializes the application when the DOM content is fully loaded.
 * Sets up tooltips, date inputs, and delete confirmations.
 * 
 * @listens DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    /**
     * Sets today's date as default for empty date input fields.
     * Formats the date as YYYY-MM-DD to match the HTML5 date input format.
     */
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            const today = new Date();
            const year = today.getFullYear();
            let month = today.getMonth() + 1;
            let day = today.getDate();
            
            // Add leading zeros if needed
            month = month < 10 ? '0' + month : month;
            day = day < 10 ? '0' + day : day;
            
            input.value = `${year}-${month}-${day}`;
        }
    });
    
    /**
     * Adds confirmation dialog for delete actions.
     * Prevents accidental deletion by requiring user confirmation.
     * Only adds the confirmation if one hasn't been set already.
     */
    const deleteLinks = document.querySelectorAll('a[href*="/delete/"]');
    deleteLinks.forEach(link => {
        if (!link.getAttribute('onclick')) {
            link.setAttribute('onclick', "return confirm('Are you sure you want to delete this expense?');");
        }
    });
});
