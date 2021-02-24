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

function load_map(token) {
    // Leaflet.js map
    var myMap = L.map('leaflet');
    const defBounds = L.latLngBounds(L.latLng(38.0306, -78.85724), L.latLng(35.29641, -83.29456))
    myMap.fitBounds(defBounds);

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

    // Parse data
    const update = data['update'];
    const nextUpdate = data['next_update'];
    const segments = data['segments'] // Array

    // Create polylines and add to map
    let polylines = createPolylines(segments);
    polylines.forEach(polyline => {
        polyline.addTo(map);
    });
};

function createPolylines(segment_array) {
    // Parse segment data and return array of L.polyline objects

    let polylines = [];
    segment_array.forEach(segObject => {
        let color = 'red';
        if (segObject['status'] === 'Open') {
            color = 'green';
        };
        polyline = L.polyline(segObject['points'], {color: color, weight: 10, opacity: 0.5});

        // Create hover tooltip
        text = `<b>Mileposts:</b> ${segObject['post_range']}<br>
        <b>Crossroads:</b> ${segObject['cross_roads']}<br>
        <b>Status:</b> ${segObject['status']}<br>
        <b>Notes:</b> ${segObject['notes']}`
        polyline.bindTooltip(text, {sticky: true}).openTooltip();

        polylines.push(polyline);
    });
    return polylines
}
