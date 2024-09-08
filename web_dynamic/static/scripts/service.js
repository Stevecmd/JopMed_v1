document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/api/services')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const servicesContainer = document.getElementById('services-container');
            data.forEach(service => {
                const serviceCard = document.createElement('div');
                serviceCard.className = 'service-card';
                serviceCard.innerHTML = `
                    <img src="${service.image_url || '/static/images/default-service.jpg'}" alt="${service.name}" class="service-image">
                    <h2 class="service-name">${service.name}</h2>
                    <p class="service-description">${service.description}</p>
                    <p class="service-price">$${parseFloat(service.price).toFixed(2)}</p>
                    <button class="add-to-cart" data-service-id="${service.id}">Add to Cart</button>
                `;
                servicesContainer.appendChild(serviceCard);
            });

            // Add event listener for "Add to Cart" buttons
            servicesContainer.addEventListener('click', function(event) {
                if (event.target.classList.contains('add-to-cart')) {
                    const serviceId = event.target.getAttribute('data-service-id');
                    addToCart(serviceId, event.target);
                }
            });
        })
        .catch(error => console.error('Error fetching services:', error));
});

function addToCart(serviceId, buttonElement) {
    fetch('http://localhost:5000/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            service_id: serviceId,
            user_id: sessionStorage.getItem('user_id'),
            quantity: 1
        }),
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            buttonElement.textContent = 'Added to Cart';
            buttonElement.disabled = true;
            buttonElement.classList.add('added');
        } else {
            alert('Failed to add service to cart.');
        }
    })
    .catch(error => console.error('Error adding service to cart:', error));
}