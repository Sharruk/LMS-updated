// Main JavaScript for College Materials & PYQs Portal

document.addEventListener('DOMContentLoaded', function() {
    console.log('College Materials & PYQs Portal loaded');
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
});

/**
 * Initialize animations for page elements
 */
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Add slide-in animation to breadcrumbs
    const breadcrumb = document.querySelector('.breadcrumb');
    if (breadcrumb) {
        breadcrumb.classList.add('slide-in');
    }
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize search functionality for file tables
 */
function initializeSearch() {
    const searchInput = document.getElementById('fileSearch');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const tableRows = document.querySelectorAll('tbody tr');
        const cards = document.querySelectorAll('.file-card');
        
        // Search in table view
        tableRows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const isVisible = text.includes(searchTerm);
            row.style.display = isVisible ? '' : 'none';
        });
        
        // Search in card view
        cards.forEach(card => {
            const text = card.textContent.toLowerCase();
            const isVisible = text.includes(searchTerm);
            card.closest('.col-md-6').style.display = isVisible ? '' : 'none';
        });
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show" role="alert">
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Insert at the top of the main container
    const mainContainer = document.querySelector('main .container');
    if (mainContainer) {
        mainContainer.insertAdjacentHTML('afterbegin', alertHtml);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = mainContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }
}

/**
 * Get icon for alert type
 */
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Get file type icon based on extension
 */
function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const iconMap = {
        'pdf': 'fa-file-pdf file-pdf',
        'doc': 'fa-file-word file-doc',
        'docx': 'fa-file-word file-doc',
        'xls': 'fa-file-excel file-xls',
        'xlsx': 'fa-file-excel file-xls',
        'ppt': 'fa-file-powerpoint file-ppt',
        'pptx': 'fa-file-powerpoint file-ppt',
        'jpg': 'fa-file-image file-img',
        'jpeg': 'fa-file-image file-img',
        'png': 'fa-file-image file-img',
        'gif': 'fa-file-image file-img',
        'zip': 'fa-file-archive file-zip',
        'rar': 'fa-file-archive file-zip',
        '7z': 'fa-file-archive file-zip',
        'txt': 'fa-file-alt file-default'
    };
    
    return iconMap[ext] || 'fa-file file-default';
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
}

/**
 * Handle form submissions with loading states
 */
function handleFormSubmission(formId, buttonSelector) {
    const form = document.getElementById(formId);
    const button = document.querySelector(buttonSelector);
    
    if (!form || !button) return;
    
    form.addEventListener('submit', function() {
        button.classList.add('loading');
        button.disabled = true;
    });
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Copied to clipboard!', 'success');
    }).catch(function() {
        showAlert('Failed to copy to clipboard', 'error');
    });
}

/**
 * Validate file upload
 */
function validateFileUpload(fileInput, allowedExtensions) {
    const file = fileInput.files[0];
    if (!file) return false;
    
    const ext = file.name.split('.').pop().toLowerCase();
    if (!allowedExtensions.includes(ext)) {
        showAlert(`File type .${ext} is not allowed`, 'error');
        return false;
    }
    
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showAlert('File size exceeds 16MB limit', 'error');
        return false;
    }
    
    return true;
}

/**
 * Initialize file upload drag and drop
 */
function initializeDragAndDrop(dropZoneId, fileInputId) {
    const dropZone = document.getElementById(dropZoneId);
    const fileInput = document.getElementById(fileInputId);
    
    if (!dropZone || !fileInput) return;
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    dropZone.addEventListener('drop', handleDrop, false);
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight() {
        dropZone.classList.add('drag-over');
    }
    
    function unhighlight() {
        dropZone.classList.remove('drag-over');
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            // Trigger change event
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }
}

/**
 * Load more content (pagination helper)
 */
function loadMoreContent(url, containerId, buttonId) {
    const container = document.getElementById(containerId);
    const button = document.getElementById(buttonId);
    
    if (!container || !button) return;
    
    button.classList.add('loading');
    button.disabled = true;
    
    fetch(url)
        .then(response => response.text())
        .then(html => {
            container.insertAdjacentHTML('beforeend', html);
            button.classList.remove('loading');
            button.disabled = false;
        })
        .catch(error => {
            console.error('Error loading content:', error);
            showAlert('Failed to load more content', 'error');
            button.classList.remove('loading');
            button.disabled = false;
        });
}

/**
 * Handle offline/online status
 */
window.addEventListener('online', function() {
    showAlert('Connection restored!', 'success');
});

window.addEventListener('offline', function() {
    showAlert('You are currently offline. Some features may not work.', 'warning');
});

/**
 * Handle page visibility changes
 */
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden
        console.log('Page hidden');
    } else {
        // Page is visible
        console.log('Page visible');
    }
});

/**
 * Error handling for images
 */
document.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
        e.target.style.display = 'none';
        console.log('Image failed to load:', e.target.src);
    }
}, true);

/**
 * Print functionality
 */
function printPage() {
    window.print();
}

/**
 * Export table data to CSV
 */
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = Array.from(table.querySelectorAll('tr'));
    const csv = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.map(cell => `"${cell.textContent.trim()}"`).join(',');
    }).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}