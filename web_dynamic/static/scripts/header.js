document.addEventListener('DOMContentLoaded', function () {
    // Simulate user logged-in state
    const isLoggedIn = false; // Change this to true to simulate a logged-in user

    const signInButton = document.getElementById('sign-in-button');
    const registerButton = document.getElementById('register-button');
    const signOutButton = document.getElementById('sign-out-button');
    const menuToggle = document.getElementById('menu-toggle');
    const dropdownMenu = document.getElementById('dropdown-menu');

    if (isLoggedIn) {
        signInButton.style.display = 'none';
        registerButton.style.display = 'none';
        signOutButton.style.display = 'block';
    } else {
        signInButton.style.display = 'block';
        registerButton.style.display = 'block';
        signOutButton.style.display = 'none';
    }

    // Toggle dropdown menu on smaller screens
    menuToggle.addEventListener('click', function () {
        const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
        menuToggle.setAttribute('aria-expanded', !isExpanded);
        dropdownMenu.classList.toggle('active');
    });
});