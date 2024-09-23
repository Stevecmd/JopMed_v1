document.addEventListener('DOMContentLoaded', function() {
    updateDashboardCards();
    createCharts();
});

function updateDashboardCards() {
    document.getElementById('total-users').textContent = `Total Users: ${dashboardData.totalUsers}`;
    document.getElementById('total-products').textContent = `Total Products: ${dashboardData.totalProducts}`;
    document.getElementById('total-orders').textContent = `Total Orders: ${dashboardData.totalOrders}`;
    document.getElementById('total-revenue').textContent = `Total Revenue: $${dashboardData.totalRevenue.toFixed(2)}`;
}

function createCharts() {
    createUserChart();
    createProductChart();
    createOrderChart();
    createRevenueChart();
}

function createUserChart() {
    const ctx = document.getElementById('users-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dashboardData.userGrowth.map(item => item.date),
            datasets: [{
                label: 'New Users',
                data: dashboardData.userGrowth.map(item => item.count),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createProductChart() {
    const ctx = document.getElementById('products-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dashboardData.topProducts.map(item => item.name),
            datasets: [{
                label: 'Top Products',
                data: dashboardData.topProducts.map(item => item.total_sold),
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createOrderChart() {
    const ctx = document.getElementById('orders-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dashboardData.orderTrend.map(item => item.date),
            datasets: [{
                label: 'Orders',
                data: dashboardData.orderTrend.map(item => item.count),
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createRevenueChart() {
    const ctx = document.getElementById('revenue-chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dashboardData.revenueTrend.map(item => item.date),
            datasets: [{
                label: 'Revenue',
                data: dashboardData.revenueTrend.map(item => item.revenue),
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}