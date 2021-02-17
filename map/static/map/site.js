document.addEventListener("DOMContentLoaded", () => {
    request_token(load_map);
});

function request_token(callback) {
    // Get accessToken from backend
    // Temp solution to prevent committing token to source control
    // Still visible to site user when public, TODO: setup restrictions

    // Grab Django csrftoken from cookie
    const csrftoken = Cookies.get('csrftoken');

    // Create request
    let request = new Request(
        "/token",
        {
            method: "GET",
            headers: {'X-CSRFToken': csrftoken},
            mode: "same-origin"
        }
    );
    
    // Fetch api token and load map
    fetch(request)
    .then(response => response.json())
    .then(data => callback(data.key));
}

/** Leaflet */
function load_map(token) {
    var myMap = L.map('leaflet').setView([37.99848, -78.89204], 10);

    let tile = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: token
    })
    tile.addTo(myMap);

    get_route_data(myMap)
};

function get_route_data(map) {
    const csrftoken = Cookies.get('csrftoken');
    let request = new Request(
        "/route_data",
        {
            method: "GET",
            headers: {'X-CSRFToken': csrftoken},
            mode: "same-origin"
        }
    );
    
    // Grab all GPS data points and load route
    fetch(request)
    .then(response => response.json())
    .then(data => {
        load_route(map, data);
    });
};

function load_route(map, data) {

    // Add a polyline route
    let route = L.polyline(data, {color: 'red', weight: 10, opacity: 0.5}).addTo(map);

    map.fitBounds(route.getBounds());
};
