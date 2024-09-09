document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');

    searchForm.addEventListener('submit', function(e) {
        if (searchInput.value.trim() === '') {
            e.preventDefault();
            alert('Please enter a search query.');
        } else if (searchInput.value.trim().length < 3) {
            e.preventDefault();
            alert('Search query must be at least 3 characters long.');
        }
    });
});