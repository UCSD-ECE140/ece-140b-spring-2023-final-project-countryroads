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
recognition.lang = "en-US";

recognition.onresult = function (event) {
  const result = event.results[event.results.length - 1];
  const message = result[0].transcript.trim();
  console.log(message);
  socket.send(message);
};

recognition.onerror = function (event) {
  console.error("Speech recognition error:", event.error);
};

function startSpeechRecognition() {
  recognition.start();
}

function stopSpeechRecognition() {
  recognition.stop();
}

function sendMessage() {
  console.log("sendMessage called!");
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
    credentials: "same-origin",
    method: verb,
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error:", response.statusText);
      }
    })
    .then(function (response) {
      if (callback) {
        callback(response);
      }
    })
    .catch((error) => console.error("Error:", error));
}

// initialize variable to null
let user_location = null;

function updateLocation() {
  navigator.geolocation.getCurrentPosition(function (position) {
    user_location = {
      client_id: clientId,
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
    };
    if (user_location) {
      server_request(
        "/update_location",
        user_location,
        "PUT",
        function (response) {
          console.log(user_location);
        }
      );
    }
  });
}

//code to remove user from database if tab is closed
window.addEventListener("beforeunload", function () {
  server_request("/delete_user", user_location, "DELETE", function () {});
});

updateLocation();
// update location every 10 seconds
setInterval(updateLocation, 10000);

// Requesting access to the Bluetooth device
function requestBluetoothDevice() {
  const serviceUuid = "99a1f7e6-2827-4ac4-8130-c58416fdac68";
  const characteristicUuid = "10b4b19c-d0f2-4571-9363-6c52986587df";
  // When building real app you need to make a bluetooth drag done
  // that pulls these values and utilzies them, you can't make a preset because it
  // is not safe. You would also need to put these unique values into a backend
  // because this is risky

  navigator.bluetooth
    .requestDevice({ acceptAllDevices: true, optionalServices: [serviceUuid] })
    .then((device) => {
      console.log("Device selected:", device.name);

      // Connecting to the Bluetooth device
      return device.gatt.connect();
    })
    .then((server) => {
      console.log("Connected to GATT server");

      // Getting the primary service
      return server.getPrimaryService(serviceUuid);
    })
    .then((service) => {
      console.log("Got primary service");

      // Getting the characteristic
      return service.getCharacteristic(characteristicUuid);
    })
    .then((characteristic) => {
      console.log("Got characteristic");

      // Adding a value change listener
      characteristic.addEventListener("characteristicvaluechanged", (event) => {
        const value = event.target.value;
        const decoder = new TextDecoder("utf-8");
        const decodedValue = decoder.decode(value.buffer);
        // This is the code you should change. Anything after the console.log you should change to do the actions needed

        console.log("Value changed:", decodedValue);
        if (decodedValue == "start") {
          startSpeechRecognition();
        } else if (decodedValue == "stop") {
          stopSpeechRecognition();
        } else if (decodedValue == "turn on") {
          roomInput.value = 1;
          joinRoom();
        }
      });

      // Start receiving notifications for value changes
      return characteristic.startNotifications();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Triggered by a user gesture, such as a button click
function getValues() {
  requestBluetoothDevice();
}

// Attach the function to a button's click event
const connectBT = document.getElementById("connect");
connectBT.addEventListener("click", getValues);
