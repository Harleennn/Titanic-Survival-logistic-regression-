document.getElementById("survival-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const pclass = document.getElementById("Pclass").value;
    const age = document.getElementById("Age").value;
    const sex = document.querySelector('input[name="Sex"]:checked')?.value;
    const sibSp = document.getElementById("SibSp").value;
    const fare = document.getElementById("Fare").value;

    if (!sex) {
        displayResult("Please select a gender.");
        return;
    }

    if (age === "" || isNaN(age) || sibSp === "" || isNaN(sibSp) || fare === "" || isNaN(fare)) {
        displayResult("Please enter valid numerical values for Age, Siblings/Spouses Aboard, and Fare.");
        return;
    }

    const data = {
        Pclass: parseInt(pclass),
        Age: parseFloat(age),
        Sex: sex,
        SibSp: parseInt(sibSp),
        Fare: parseFloat(fare)
    };

    console.log("Data sent to API:", data);

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Data received from API:", data);
        if (data.survived === 1) {
            displayResult("Prediction: This passenger is likely to survive.");
        } else {
            displayResult("Prediction: This passenger is not likely to survive.");
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        displayResult("An error occurred during prediction.");
    });
});

function displayResult(message) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = message;
    resultDiv.style.display = "block";
}
