document.addEventListener('DOMContentLoaded', function() {
    const productsContainer = document.getElementById('products-container');

    // Fetch products data from the server
    fetch('http://localhost:5000/api/products')
        .then(response => response.json())
        .then(products => {
            products.forEach(product => {
                const productCard = document.createElement('div');
                productCard.className = 'product-card';
                productCard.innerHTML = `
                    <img src="${product.image_url || '/static/images/default-product.jpg'}" alt="${product.name}" class="product-image">
                    <h2 class="product-name">${product.name}</h2>
                    <p class="product-description">${product.description}</p>
                    <p class="product-price">$${parseFloat(product.price).toFixed(2)}</p>
                    <p class="product-stock">In stock: ${product.stock}</p>
                    <div class="cart-controls">
                        <button class="decrement-cart" data-product-id="${product.id}">-</button>
                        <span class="cart-quantity" data-product-id="${product.id}">0</span>
                        <button class="increment-cart" data-product-id="${product.id}">+</button>
                    </div>
                `;
                productsContainer.appendChild(productCard);
            });

            document.querySelectorAll('.increment-cart, .decrement-cart').forEach(button => {
                button.addEventListener('click', function() {
                    const productId = this.getAttribute('data-product-id');
                    const change = this.classList.contains('increment-cart') ? 1 : -1;
                    updateCart(productId, change);
                });
            });
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });

    function updateCart(productId, change) {
        fetch('http://localhost:5000/api/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: change
            }),
            credentials: 'include'
        })
        .then(response => {
            if (response.status === 401) {
                // User is not logged in
                alert('Please log in to update your cart.');
                return Promise.reject('User not logged in');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                updateQuantityDisplay(productId, change);
            } else {
                alert(data.error || 'Failed to update cart.');
            }
        })
        .catch(error => {
            if (error !== 'User not logged in') {
                console.error('Error updating cart:', error);
            }
        });
    }

    function updateQuantityDisplay(productId, change) {
        const quantityElement = document.querySelector(`.cart-quantity[data-product-id="${productId}"]`);
        if (quantityElement) {
            let newQuantity = parseInt(quantityElement.textContent) + change;
            newQuantity = Math.max(0, newQuantity);
            quantityElement.textContent = newQuantity;
        }
    }

    function initializeCartQuantities() {
        fetch('http://localhost:5000/api/cart', {
            headers: {
                'User-ID': sessionStorage.getItem('user_id')
            },
            credentials: 'include'
        })
        .then(response => {
            if (response.status === 401) {
                // Handle unauthorized access
                return Promise.reject('User not logged in');
            }
            return response.json();
        })
        .then(cart => {
            for (const item of cart) {
                updateQuantityDisplay(item.product_id, item.quantity);
            }
        })
        .catch(error => {
            if (error !== 'User not logged in') {
                console.error('Error fetching cart:', error);
            }
        });
    }

    initializeCartQuantities();

    function addToCart(productId, name, price) {
        const isLoggedIn = document.body.classList.contains('logged-in');
        const quantity = 1; // Or however you determine the quantity

        if (isLoggedIn) {
            // Send request to server
            fetch('/cart/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_id: productId, quantity: quantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Item added to cart');
                    document.dispatchEvent(new Event('cartUpdated'));
                } else {
                    alert('Failed to add item to cart');
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            // Handle cart locally
            let cart = JSON.parse(localStorage.getItem('cart') || '[]');
            let existingItem = cart.find(item => item.id === productId);
            if (existingItem) {
                existingItem.quantity += quantity;
            } else {
                cart.push({ id: productId, name: name, price: price, quantity: quantity });
            }
            localStorage.setItem('cart', JSON.stringify(cart));
            alert('Item added to cart');
            document.dispatchEvent(new Event('cartUpdated'));
        }
    }

});

