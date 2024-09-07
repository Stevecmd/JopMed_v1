document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('paymentModal');
    const confirmPurchaseBtn = document.getElementById('confirm-purchase');
    const closeBtn = document.getElementsByClassName('close')[0];
    const confirmPaymentBtn = document.getElementById('confirmPayment');
    const modalTotalAmount = document.getElementById('modalTotalAmount');
    const totalAmountSpan = document.getElementById('total-amount');

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
        modalTotalAmount.textContent = totalAmountSpan.textContent;
        modal.style.display = 'block';
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    confirmPaymentBtn.addEventListener('click', function() {
        fetch('/purchase/confirm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: modalTotalAmount.textContent
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modal.style.display = 'none';
                alert('Thank you for your purchase! Your order has been confirmed.');
                window.location.href = data.receipt_url;
            } else {
                alert('Purchase failed. Please try again.');
            }
        })
        .catch(error => console.error('Error confirming purchase:', error));
    });
});