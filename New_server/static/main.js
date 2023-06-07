const roomInput = document.getElementById("roomInput");
const chatLog = document.getElementById("chatLog");
const messageInput = document.getElementById("messageInput");
const startButton = document.getElementById("startButton");
const stopButton = document.getElementById("stopButton");  
const clientId = Math.floor(Math.random() * 100000);
console.log("CLIENT ID IS: " + clientId);
let socket = null;

startButton.addEventListener("click", startSpeechRecognition);
stopButton.addEventListener("click", stopSpeechRecognition);

function joinRoom() {
  const room = roomInput.value;

  if (room && !socket) {
    const url = `wss://${window.location.host}/ws/${room}/${clientId}`;
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

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// Define the 'request' function to handle interactions with the server
function server_request(url, data = {}, verb, callback) {
  return fetch(url, {
    credentials: 'same-origin',
    method: verb,
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Error:', response.statusText);
      }
    })
    .then(function(response) {
      if (callback) {
        callback(response);
      }
    })
    .catch(error => console.error('Error:', error));
}


// initialize variable to null
let user_location = null; 

function updateLocation() {
  navigator.geolocation.getCurrentPosition(function(position) {
    user_location = {
      client_id: clientId,
      latitude: position.coords.latitude,
      longitude: position.coords.longitude
    };
    if (user_location) {
      server_request("/update_location", user_location, "PUT", function(response) {
        console.log(user_location);
      });
    }
  });
}


//code to remove user from database if tab is closed
window.addEventListener('beforeunload', function() {
    server_request("/delete_user", user_location, "DELETE", function(){

    });
  });

updateLocation();
// update location every 10 seconds
setInterval(updateLocation, 10000);


