<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TIME-OFF REQUEST</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            text-align: center;
            padding: 20px;
            margin: 0;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: 0 auto;
        }
        label {
            display: block;
            text-align: left;
            margin: 5px 0;
            font-weight: bold;
        }
        input, select, textarea {
            width: 95%;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            display: block;
        }
        button {
            background-color: #28a745;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 95%;
            margin: 10px 0;
            display: block;
        }
        button:hover {
            background-color: #218838;
        }
        .message {
            margin-top: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>TIME-OFF REQUEST</h2>
    <form id="offRequestForm">
        <label for="name">Full Name:</label>
        <input type="text" id="name" name="name" required>

        <label for="truck_number">Truck Number:</label>
        <input type="text" id="truck_number" name="truck_number" required>

        <label for="company">Company:</label>
        <select id="company" name="company" required>
            <option value="">Select Company</option>
            <option value="Sayram Express LLC">Sayram Express LLC</option>
            <option value="Golden Mile LLC">Golden Mile LLC</option>
            <option value="Iconic Logistics LLC">Iconic Logistics LLC</option>
            <option value="Sayram Logistics CO">Sayram Logistics CO</option>
        </select>

        <label for="date_from">Off Since:</label>
        <input type="date" id="date_from" name="date_from" required>

        <label for="unknown_date_till">Off Until: Unknown</label>
        <input type="checkbox" id="unknown_date_till" name="unknown_date_till" onclick="toggleDateTill()">

        <label for="date_till">Off Until:</label>
        <input type="date" id="date_till" name="date_till" disabled>

        <label for="reason">Reason:</label>
        <textarea id="reason" name="reason" rows="3" required></textarea>

        <label for="pause_insurance_eld">Pause Insurance and ELD?</label>
        <select id="pause_insurance_eld" name="pause_insurance_eld" required>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
        </select>

        <button type="submit">Submit</button>
        <p class="message" id="statusMessage"></p>
    </form>
</div>

<script>
    function toggleDateTill() {
        const dateTillField = document.getElementById("date_till");
        const unknownDateTill = document.getElementById("unknown_date_till").checked;
        dateTillField.disabled = unknownDateTill;
    }

    document.getElementById("offRequestForm").addEventListener("submit", async function(event) {
        event.preventDefault();
        
        let name = document.getElementById("name").value;
        let truckNumber = document.getElementById("truck_number").value;
        let company = document.getElementById("company").value;
        let dateFrom = document.getElementById("date_from").value;
        let dateTill = document.getElementById("date_till").value;
        let unknownDateTill = document.getElementById("unknown_date_till").checked;
        let reason = document.getElementById("reason").value;
        let pauseInsuranceEld = document.getElementById("pause_insurance_eld").value;

        // If the checkbox is checked, set dateTill to an empty string to indicate unknown date
        if (unknownDateTill) {
            dateTill = "";
        }

        let statusMessage = document.getElementById("statusMessage");
        statusMessage.textContent = "Sending request...";

        try {
            let response = await fetch("http://127.0.0.1:5000/send-message", { 
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, truckNumber, company, dateFrom, dateTill, reason, pauseInsuranceEld, unknownDateTill })
            });

            let data = await response.json();
            if (data.success) {
                statusMessage.textContent = "✅ Request Sent Successfully!";
                statusMessage.style.color = "green";
            } else {
                statusMessage.textContent = "❌ Error sending request.";
                statusMessage.style.color = "red";
            }
        } catch (error) {
            statusMessage.textContent = "❌ Error sending request.";
            statusMessage.style.color = "red";
        }
    });
</script>

</body>
</html>
