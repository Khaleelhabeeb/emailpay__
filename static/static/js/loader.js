function loginUser() {
    // Add a delay of 1000 milliseconds (1 seconds) before showing the loader
    setTimeout(function() {
        showLoader(); // Show loader after the delay
    }, 1000);

    // Perform AJAX request to login
    $.ajax({
        url: '/login', // Your login endpoint
        method: 'POST',
        data: { /* your login data */ },
        success: function(response) {
            // Handle successful login
            hideLoader(); // Hide loader after successful login
        },
        error: function(error) {
            // Handle login error
            hideLoader(); // Hide loader in case of login error
        }
    });
}


function registerUser() {
    // Add a delay of 1000 milliseconds (1 seconds) before showing the loader
    setTimeout(function() {
        showLoader(); // Show loader after the delay
    }, 1000);

    // Perform AJAX request to register
    $.ajax({
        url: '/register', // Ymy regin endpoint
        method: 'POST',
        data: { /* your login data */ },
        success: function(response) {
            // Handle successful login
            hideLoader(); // Hide loader after successful login
        },
        error: function(error) {
            // Handle login error
            hideLoader(); // Hide loader in case of login error
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

