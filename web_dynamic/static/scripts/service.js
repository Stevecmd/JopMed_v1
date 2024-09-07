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
                `;
                servicesContainer.appendChild(serviceCard);
            });
        })
        .catch(error => console.error('Error fetching services:', error));
});
