document.getElementById('register-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        email: formData.get('email'),
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        password: formData.get('password')
    };

    fetch('http://localhost:5000/api/register', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registration successful! Please log in.');
            window.location.href = '/login';
        } else {
            alert(data.error || 'Registration failed. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
});