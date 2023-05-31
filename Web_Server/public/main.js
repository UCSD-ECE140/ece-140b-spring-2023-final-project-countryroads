// var location = document.getElementById("loc");
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// Define the 'request' function to handle interactions with the server
function server_request(url, data={}, verb, callback) {
    return fetch(url, {
      credentials: 'same-origin',
      method: verb,
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(function(response) {
      if(callback)
        callback(response);
    })
    .catch(error => console.error('Error:', error));
}

// initialize variable to null
let user_location = null; 

// function to update user_location variable with current locationS
function updateLocation() {
  console.log(user_location);
  navigator.geolocation.getCurrentPosition(function(position) {
    user_location = {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude
    };
  });
  if(user_location){
    server_request("/update_location", user_location, "POST", function(){

    });
  }
}

updateLocation();
// update location every 10 seconds
setInterval(updateLocation, 10000);

// Handle Start button click event
document.getElementById('startButton').addEventListener('click', () => {
    // Set up WebSocket connection
    let socket = new WebSocket('ws://localhost:6543/ws');

    // Handle WebSocket connection open event
    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    // Handle WebSocket connection close event
    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
    // Request microphone access
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            // Add local audio track to PeerConnection
            const audioTracks = stream.getAudioTracks();
            const peerConnection = new RTCPeerConnection();
            peerConnection.addTrack(audioTracks[0], stream);

            // Handle audio data available event
            peerConnection.addEventListener('datachannel', event => {
                const dataChannel = event.channel;

                // Send audio data to WebSocket server
                dataChannel.addEventListener('message', event => {
                    socket.send(event.data);
                });
            });

            // Create a data channel for audio transmission
            const dataChannel = peerConnection.createDataChannel('audio');

            // Handle Stop button click event
            document.getElementById('stopButton').addEventListener('click', () => {
                stream.getTracks().forEach(track => track.stop());
                peerConnection.close();
                socket.close();    
            });
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
});


