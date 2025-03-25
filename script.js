document.addEventListener("DOMContentLoaded", function () {
    const emergencyButton = document.getElementById("emergencyButton");

    emergencyButton.addEventListener("click", function () {
        fetch("/emergency-alert", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ alert: "Emergency triggered!" }),
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    });
});
