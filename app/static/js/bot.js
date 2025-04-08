// Clock update function
function updateTime() {
    var now = new Date();
    var hours = now.getHours().toString().padStart(2, '0');
    var minutes = now.getMinutes().toString().padStart(2, '0');
    var seconds = now.getSeconds().toString().padStart(2, '0');
    var timeString = hours + ':' + minutes + ':' + seconds;
    document.getElementById('clock').textContent = timeString;
}

// Update clock immediately and then every second
updateTime();
setInterval(updateTime, 1000);

// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const messagesContainer = document.getElementById("messages");

    // Function to append a message to the chat
    function appendMessage(sender, text) {
        const messageDiv = document.createElement("div");
        
        if (sender === "user") {
            messageDiv.className = "user-message";
        } else {
            messageDiv.className = "bot-message";
        }
        
        messageDiv.textContent = text;
        
        // Create a wrapper div to handle the flow
        const wrapperDiv = document.createElement("div");
        if (sender === "user") {
            wrapperDiv.style.textAlign = "right";
        } else {
            wrapperDiv.style.textAlign = "left";
        }
        
        wrapperDiv.appendChild(messageDiv);
        messagesContainer.appendChild(wrapperDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Handle form submission
    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Display user message
        appendMessage("user", message);
        userInput.value = "";

        // Send message to backend
        fetch("/get", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        })
        .then((response) => response.json())
        .then((data) => {
            // Display bot response
            appendMessage("bot", data.response || "No response from the bot.");
        })
        .catch((error) => {
            console.error("Error:", error);
            appendMessage("bot", "Sorry, something went wrong. Please try again.");
        });
    });
});