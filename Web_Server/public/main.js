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

// function to update user_location variable with current location
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




