document.addEventListener('DOMContentLoaded', function () {
    // Simulate user logged-in state
    const isLoggedIn = false; // Change this to true to simulate a logged-in user

    const loginButton = document.getElementById('login-button');
    const registerButton = document.getElementById('register-button');
    const signOutButton = document.getElementById('logout-button');
    const menuToggle = document.getElementById('menu-toggle');
    const dropdownMenu = document.getElementById('dropdown-menu');

    if (loginButton && registerButton && signOutButton) {
        if (isLoggedIn) {
            loginButton.style.display = 'none';
            registerButton.style.display = 'none';
            signOutButton.style.display = 'block';
        } else {
            loginButton.style.display = 'block';
            registerButton.style.display = 'block';
            signOutButton.style.display = 'none';
        }
    }

    // Toggle dropdown menu on smaller screens
    if (menuToggle && dropdownMenu) {
        menuToggle.addEventListener('click', function () {
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', !isExpanded);
            dropdownMenu.classList.toggle('active');
        });
    }
});