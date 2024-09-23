document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('paymentModal');
    const confirmPurchaseBtn = document.getElementById('confirm-purchase');
    const clearCartBtn = document.getElementById('clear-cart');
    const closeBtn = document.getElementsByClassName('close')[0];
    const confirmPaymentBtn = document.getElementById('confirmPayment');
    const modalTotalAmount = document.getElementById('modalTotalAmount');
    const totalAmountSpan = document.getElementById('total-amount');
    const cartSummary = document.getElementById('cart-summary');
    const addressIdInput = document.getElementById('address-id');
    const paymentMethodInput = document.getElementById('payment-method'); 

    // Calculate total amount
    function calculateTotal() {
        let total = 0;
        document.querySelectorAll('.item-price').forEach(item => {
            total += parseFloat(item.textContent.replace('Price: $', ''));
        });
        return total.toFixed(2);
    }

    // Update total amount on page load
    totalAmountSpan.textContent = calculateTotal();

    confirmPurchaseBtn.addEventListener('click', function() {
        // Check if address and payment method are provided
        if (!addressIdInput.value || !paymentMethodInput.value) {
            modalTotalAmount.textContent = totalAmountSpan.textContent;
            modal.style.display = 'block'; // Show the modal if information is missing
        } else {
            // Proceed with the purchase if both are provided
            confirmPayment();
        }
    });

    function confirmPayment() {
        fetch('http://localhost:5000/api/purchase/confirm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                amount: modalTotalAmount.textContent,
                address_id: addressIdInput.value,
                payment_method: paymentMethodInput.value
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'receipt.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            alert('Thank you for your purchase! Your order has been confirmed.');
            window.location.href = '/';
        })
        .catch(error => {
            console.error('Error confirming purchase:', error);
            alert('An error occurred while processing your purchase. Please try again.');
        });
    }

    clearCartBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear your cart?')) {
            fetch('/cart/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    cartSummary.innerHTML = '<p>Your cart is empty.</p>';
                    totalAmountSpan.textContent = '0.00';
                    alert('Your cart has been cleared.');
                } else {
                    alert('Failed to clear cart. Please try again.');
                }
            })
            .catch(error => console.error('Error clearing cart:', error));
        }
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});