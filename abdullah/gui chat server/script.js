let socket;
let username = "";

document.getElementById("connectBtn").onclick = () => {
    const ip = document.getElementById("ip").value.trim();
    if (!ip) {
        alert("Enter server WebSocket URL, e.g. ws://192.168.1.20:8765");
        return;
    }

    username = prompt("Enter your name:"); // ask user name
    if (!username) {
        alert("Name is required");
        return;
    }

    socket = new WebSocket(ip);

    socket.onopen = () => {
        socket.send(username); // send name first
        appendMessage("*** Connected to server as " + username + " ***");
        document.getElementById("message").disabled = false;
        document.getElementById("sendBtn").disabled = false;
    };

    socket.onmessage = (event) => appendMessage(event.data);
    socket.onclose = () => appendMessage("*** Disconnected ***");
    socket.onerror = (err) => appendMessage("Error: " + err);
};

document.getElementById("sendBtn").onclick = () => {
    const msg = document.getElementById("message").value;
    if (msg && socket.readyState === WebSocket.OPEN) {
        socket.send(msg);
        appendMessage(username + ": " + msg); // show own message too
        document.getElementById("message").value = "";
    }
};

function appendMessage(msg) {
    const chatDiv = document.getElementById("chat");
    const newMsg = document.createElement("div");
    newMsg.textContent = msg;
    chatDiv.appendChild(newMsg);
    chatDiv.scrollTop = chatDiv.scrollHeight;
}
