const checkBtn = document.getElementById("checkBtn");

checkBtn.addEventListener("click", async () => {

    const newsText = document.getElementById("newsInput").value;

    if (newsText.trim() === "") {
        alert("Please enter news text");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: newsText
            })
        });

        const data = await response.json();

        document.getElementById("resultBox").style.display = "block";

        const predictionElement =
            document.getElementById("prediction");

        predictionElement.innerText =
            data.prediction.toUpperCase();

        if (data.prediction.toLowerCase() === "fake") {

            predictionElement.className = "fake";

            document.getElementById("warning").innerText =
                "WARNING: This news may be fake or misleading.";

        }
        else {

            predictionElement.className = "real";

            document.getElementById("warning").innerText =
                "This news appears reliable.";
        }

        document.getElementById("confidence").innerText =
            data.confidence + "%";

        document.getElementById("explanation").innerText =
            data.explanation;

    }
    catch (error) {

        console.error(error);

        alert("Error connecting to backend");
    }
});