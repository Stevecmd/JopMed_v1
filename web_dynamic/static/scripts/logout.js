document.getElementById('logout-link').addEventListener('click', function(e) {
    e.preventDefault();
    fetch('http://localhost:5000/api/logout', {
        method: 'POST',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            window.location.href = '/login';  // Redirect to login page after logout
        } else {
            alert(data.error || 'Logout failed. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
});