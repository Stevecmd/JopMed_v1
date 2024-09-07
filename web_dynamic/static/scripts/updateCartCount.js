function updateCartCount() {
    // Check if user is logged in
    const isLoggedIn = document.body.classList.contains('logged-in');
    
    if (isLoggedIn) {
        // Fetch cart from server for logged-in users
        fetch('http://127.0.0.1:5000/api/cart', {
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(cartItems => updateCartCountDisplay(cartItems))
        .catch(error => console.error('Error fetching cart count:', error));
    } else {
        // Use local storage for non-logged-in users
        const localCart = JSON.parse(localStorage.getItem('cart') || '[]');
        updateCartCountDisplay(localCart);
    }
}

function updateCartCountDisplay(cartItems) {
    // Update cart count display
    const cartCount = cartItems.reduce((count, item) => count + item.quantity, 0);
    document.getElementById('cart-count').textContent = cartCount;
}

document.addEventListener('DOMContentLoaded', updateCartCount);
document.addEventListener('cartUpdated', updateCartCount);