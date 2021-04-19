document.addEventListener("DOMContentLoaded", () => {

    // Load map
    requestToken(loadMap);

    // Assign launch modal to "About" anchor tag
    document.getElementById('launch-modal').addEventListener('click', launchModal);

    // Assign close modal to all classes "close-modal"
    closeModalElements = document.querySelectorAll('.close-modal');
    closeModalElements.forEach(elem => {
        elem.addEventListener('click', closeModal);
    });

    // Assign click listener to prevent event propagation (prevent close modal when modal content is clicked)
    document.getElementById('modal-content').addEventListener('click', contentClick);
});

// Initialize map
let myMap;

function requestToken(callback) {
    // Get accessToken from backend

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

function loadMap(token) {
    // Leaflet.js map
    myMap = L.map('map');
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

    // Request route data
    getRouteData(myMap)
};

function getRouteData(map) {
    // Request route data for open and closures
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
        loadRoute(map, data);
        loadUpdate(data);
    });
};

function loadRoute(map, data) {
    // Create polylines and add to map
    let polylines = createPolylines(data['segments']);
    polylines.forEach(polyline => {
        polyline.addTo(map);
    });
};

function createPolylines(segmentArray) {
    // Parse segment data and return array of L.polyline objects
    let polylines = [];
    segmentArray.forEach(segObject => {

        // Create polyline
        polyline = L.polyline(segObject['points'], {
            color: segObject['status'] == 'Closed'? 'red': 'green',
            weight: 10,
            opacity: 0.5
        });

        // Polyline click function
        polyline.on('click', zoomPoly)

        // Polyline hover tooltip
        text = `<b>Mileposts:</b> ${segObject['post_range']}<br>
        <b>Crossroads:</b> ${segObject['cross_roads']}<br>
        <b>Status:</b> ${segObject['status']}<br>
        <b>Notes:</b> ${segObject['notes']}`
        polyline.bindTooltip(text, {sticky: true}).openTooltip();

        polylines.push(polyline);
    });
    return polylines
}

function zoomPoly() {
    // Zoom to segment after click
    myMap.fitBounds(this.getBounds());
}

function loadUpdate(data) {
    // Format and apply time and date to DOM
    const strUpdate = formatUpdate(data['update'])
    const strNextUpdate = formatNextUpdate(data['next_update'])
    document.getElementById('update').innerHTML = `Road Status as of <b>${strUpdate}</b>`
    document.getElementById('next-update').innerHTML = `Next update: <b>${strNextUpdate}</b>`
}

function formatUpdate(isoString) {
    // Format: Tuesday, March 2nd at 5:00 AM
    const date = new Date(isoString);
    const options = { weekday: 'long', month: 'long', day: 'numeric' };
    let strDate = date.toLocaleDateString('en-NY', options);

    // Format time to 12 Hour (https://stackoverflow.com/a/17538193/14984232)
    let strTime = date.toLocaleTimeString().replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3")

    return `${strDate} at ${strTime}`;
}

function formatNextUpdate(isoString) {
    // Format: March 3rd
    const date = new Date(isoString);
    const options = {month: 'long', day: 'numeric' };
    let strDate = date.toLocaleDateString('en-NY', options);
                
    return `${strDate}`;
}

function launchModal() {
    event.preventDefault()
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

function contentClick() {
    event.stopPropagation()
}
