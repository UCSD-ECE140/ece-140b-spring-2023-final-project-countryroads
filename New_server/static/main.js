const roomInput = document.getElementById("roomInput");
const chatLog = document.getElementById("chatLog");
const messageInput = document.getElementById("messageInput");
const startButton = document.getElementById("startButton");
const stopButton = document.getElementById("stopButton");
const clientId = "client" + Math.floor(Math.random() * 100000);
let socket = null;

startButton.addEventListener("click", startSpeechRecognition);
stopButton.addEventListener("click", stopSpeechRecognition);

function joinRoom() {
  const room = roomInput.value;

  if (room && !socket) {
    const url = `ws://${window.location.host}/ws/${room}/${clientId}`;
    socket = new WebSocket(url);

    socket.onopen = () => {
      logMessage("Connected to the room");
    };

    socket.onmessage = (event) => {
      logMessage(event.data);
    };

    socket.onclose = () => {
      logMessage("Disconnected from the room");
      socket = null;
    };
  }
}

startButton.addEventListener("click", startSpeechRecognition);
stopButton.addEventListener("click", stopSpeechRecognition);

const recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.lang = 'en-US';

recognition.onresult = function(event) {
  const result = event.results[event.results.length - 1];
  const message = result[0].transcript.trim();
  console.log(message);
  socket.send(message);
};

recognition.onerror = function(event) {
  console.error("Speech recognition error:", event.error);
};

function startSpeechRecognition() {
  recognition.start();
}

function stopSpeechRecognition() {
  recognition.stop();
}

function sendMessage() {
    console.log("sendMessage called!")
    const message = messageInput.value;
  
    if (message && socket) {
    //   socket.send(JSON.stringify({ message: message }));
        socket.send(message);
        messageInput.value = "";
    }
  }

function logMessage(message) {
    const messageElement = document.createElement("div");
    messageElement.innerText = message;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight;

    // Convert the message to speech
    const utterance = new SpeechSynthesisUtterance(message);
    speechSynthesis.speak(utterance);
}
