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

function getLocation() {
  if (navigator.geolocation) {
    return navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  console.log("Latitude: " + position.coords.latitude +
  " Longitude: " + position.coords.longitude);
  return JSON.stringify({"latitude": position.coords.latitude, "longitude": position.coords.longitude})
}


function newUser(){
    data = getLocation()

    server_request("/new_user", data, "POST", function(){

    });
}


newUser()

// getLocation();

// //will make POST request to update database of USER's location
// function updateLocation(){

// }

// setInterval(updateLocation, 10000);

