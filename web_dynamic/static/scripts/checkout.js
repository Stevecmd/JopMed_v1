document.getElementById('confirm-purchase').addEventListener('click', function() {
    fetch('/purchase/confirm', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Purchase successful! Redirecting to receipt...');
            window.location.href = data.receipt_url;
        } else {
            alert('Purchase failed. Please try again.');
        }
    })
    .catch(error => console.error('Error confirming purchase:', error));
});
