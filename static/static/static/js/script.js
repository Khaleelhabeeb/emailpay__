// JavaScript to handle modal pop-up
const sendMoneyBtn = document.getElementById('sendMoneyBtn');
const sendMoneyModal = document.getElementById('sendMoneyModal');
const closeSendMoneyModal = document.getElementById('closeSendMoneyModal');

sendMoneyBtn.addEventListener('click', () => {
    sendMoneyModal.style.display = 'block';
});

closeSendMoneyModal.addEventListener('click', () => {
    sendMoneyModal.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target == sendMoneyModal) {
        sendMoneyModal.style.display = 'none';
    }
});z

function send_money() {
    // Add a delay of 1000 milliseconds (1 seconds) before showing the loader
    setTimeout(function() {
        showLoader(); // Show loader after the delay
    }, 10000);

    // Perform AJAX request to register
    $.ajax({
        url: '/send_money', // Ymy regin endpoint
        method: 'POST',
        data: {},
        success: function(response) {
            hideLoader(); 
        },
        error: function(error) {
            
            hideLoader();
        }
    });
}

// Show loader during AJAX request
function showLoader() {
    document.getElementById("loader").style.display = "block";
}

// Hide loader after AJAX request is complete
function hideLoader() {
    document.getElementById("loader").style.display = "none";
}