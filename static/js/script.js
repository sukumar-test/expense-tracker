/**
 * Custom JavaScript for Expense Tracker Application
 * 
 * This script provides client-side enhancements including:
 * - Bootstrap tooltip initialization
 * - Auto-filling date inputs with today's date
 * - Confirmation dialogs for delete actions
 * 
 * Dependencies: Bootstrap 5.3.0
 */

// Wait for DOM to be fully loaded before executing scripts
document.addEventListener('DOMContentLoaded', function() {
    
    // ===== Bootstrap Tooltips Initialization =====
    // Find all elements with tooltip attribute and initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ===== Auto-fill Date Inputs =====
    // Set today's date as default for empty date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Only set default if the input is currently empty
        if (!input.value) {
            const today = new Date();
            const year = today.getFullYear();
            let month = today.getMonth() + 1;  // JavaScript months are 0-indexed
            let day = today.getDate();
            
            // Add leading zeros to month and day if needed (e.g., 5 becomes 05)
            month = month < 10 ? '0' + month : month;
            day = day < 10 ? '0' + day : day;
            
            // Set the input value in YYYY-MM-DD format
            input.value = `${year}-${month}-${day}`;
        }
    });
    
    // ===== Delete Confirmation Dialogs =====
    // Add confirmation prompt before deleting expenses
    const deleteLinks = document.querySelectorAll('a[href*="/delete/"]');
    deleteLinks.forEach(link => {
        // Only add onclick if it doesn't already exist (avoid duplicates)
        if (!link.getAttribute('onclick')) {
            link.setAttribute('onclick', "return confirm('Are you sure you want to delete this expense?');");
        }
    });
});
