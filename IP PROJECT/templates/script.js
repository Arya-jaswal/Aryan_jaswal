document.getElementById("prediction-form").addEventListener("submit", function(event) {
    event.preventDefault();
    // Fetch form data
    let formData = new FormData(this);
    // Convert form data to JSON
    let jsonData = {};
    for (const [key, value] of formData.entries()) {
        jsonData[key] = value;
    }
    // Send JSON data to server
    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        // Display prediction result
        document.getElementById("result").innerHTML = `<p>Predicted Value: ${data.prediction}</p>`;
    })
    .catch(error => console.error("Error:", error));
});
