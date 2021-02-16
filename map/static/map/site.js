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

    load_route(myMap)
};

function load_route(map) {

    const latlngs = [
        [37.99848, -78.89204],
        [37.96237, -78.9065699],
        [37.94919, -78.91557]
    ];

    L.polyline(latlngs, {color: 'red', weight: 10, opacity: 0.5}).addTo(map);

    const another = [
        [37.94919, -78.91557],
        [37.94328,-78.9314699],
        [37.94127,-78.93691]
    ];

    L.polyline(another, {color: 'green', weight: 10, opacity: 0.5}).addTo(map);
}
