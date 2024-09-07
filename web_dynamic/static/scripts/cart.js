document.addEventListener('DOMContentLoaded', function() {
    const cartContainer = document.getElementById('cart-items');
    const totalAmountElement = document.getElementById('total-amount');

    function fetchCart() {
        fetch('http://localhost:5000/api/cart', {
            credentials: 'include',  // Ensure cookies are included
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.status === 401) {
                // Handle unauthorized access
                // alert('Please log in to view your cart.');
                return Promise.reject('User not logged in');
            }
            return response.json();
        })
        .then(cartItems => {
            cartContainer.innerHTML = '';
            let totalAmount = 0;

            cartItems.forEach(item => {
                const cartItem = document.createElement('div');
                cartItem.className = 'cart-item';
                cartItem.innerHTML = `
                    <img src="${item.product ? item.product.image_url : item.service.image_url}" alt="${item.product ? item.product.name : item.service.name}" class="cart-item-image">
                    <div class="cart-item-details">
                        <h3>${item.product ? item.product.name : item.service.name}</h3>
                        <p>Quantity: ${item.quantity}</p>
                        <p>Price: $${(item.product ? item.product.price : item.service.price).toFixed(2)}</p>
                    </div>
                `;
                cartContainer.appendChild(cartItem);
                totalAmount += (item.product ? item.product.price : item.service.price) * item.quantity;
            });

            totalAmountElement.textContent = totalAmount.toFixed(2);
        })
        .catch(error => {
            if (error !== 'User not logged in') {
                console.error('Error fetching cart:', error);
            }
        });
    }

    fetchCart();
});