// currency.js file for fetching realtime currency prices 
function fetchCurrencyPrices() {
    const currencies = ["USD", "EUR", "GBP", "NGN"];
    const apiUrl =  'https://api.exchangerate-api.com/v4/latest/USD' ;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            currencies.forEach(currency => {
                const priceElement = document.getElementById(currency).querySelector('.font-14.weight-700');
                const percentChangeElement = document.getElementById(currency).querySelector('.font-10.weight-400');
                const price = data.rates[currency].toFixed(2);
                const percentChange = ((data.rates[currency] - 1) * 100).toFixed(2);

                priceElement.textContent = `${price} USD`;
                percentChangeElement.textContent = `${percentChange}%`;
            });
        })
        .catch(error => {
            console.error("Error fetching currency data: ", error);
        });
}

// Fetch currency prices when the page loads
window.onload = function() {
    fetchCurrencyPrices();
    // Fetch currency prices every 10 seconds
    setInterval(fetchCurrencyPrices, 10000);
};
