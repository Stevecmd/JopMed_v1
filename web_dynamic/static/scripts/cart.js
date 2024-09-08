function fetchCart() {
    const isLoggedIn = document.body.classList.contains('logged-in');
    
    if (isLoggedIn) {
        fetch('http://localhost:5000/api/cart', {
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(displayCart)
        .catch(error => {
            console.error('Error fetching cart:', error);
            displayCart([]);
        });
    } else {
        const localCart = JSON.parse(localStorage.getItem('cart') || '[]');
        displayCart(localCart);
    }
}

function displayCart(cartItems) {
    const cartContainer = document.getElementById('cart-items');
    const totalAmountElement = document.getElementById('total-amount');
    
    if (!cartContainer || !totalAmountElement) {
        console.error('Cart elements not found');
        return;
    }

    cartContainer.innerHTML = '';
    let totalAmount = 0;
    let itemCount = 0;

    cartItems.forEach(item => {
        // Create and append cart item elements
        // ... (your existing code for creating cart item elements)
        
        itemCount += item.quantity;
        totalAmount += item.price * item.quantity;
    });

    totalAmountElement.textContent = totalAmount.toFixed(2);
    
    // Update cart count
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = itemCount;
    }

    // Show/hide checkout button based on login status
    const checkoutButton = document.getElementById('checkout-button');
    if (checkoutButton) {
        checkoutButton.style.display = isLoggedIn ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', fetchCart);
document.addEventListener('cartUpdated', fetchCart);