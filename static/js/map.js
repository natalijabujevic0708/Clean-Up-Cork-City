
// Create the map
function initMap() {
    var map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: {
            lat: 51.903614,
            lng: -8.468399
        }
    });

    // Create the markers
    var items_locations = document.querySelectorAll(".address_of_locations");
    for (var i = 0; i < items_locations.length; i++) {
        var marker = new google.maps.Marker({
            position: { lat: parseFloat(this.document.getElementsByClassName('lat')[i].innerHTML), lng: parseFloat(this.document.getElementsByClassName('long')[i].innerHTML) },
            map: map,
        });
        infoWindow(marker, this.document.getElementsByClassName('address')[i].innerHTML);
    }

    // Create info window when clicked on the marker
    var iw = new google.maps.InfoWindow();
    function infoWindow(marker, message) {
        google.maps.event.addListener(marker, 'click', function () {
            var html = "<p id='search_address' onclick = search_address()>" + message + "</p>";
            // set the content 
            iw.setContent(html);
            // open the infowindow on the marker
            iw.open(map, marker);
        });
    }

    // Create default bounds for autocomplete
    var defaultBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(51.8722517, -8.53925228),
        new google.maps.LatLng(51.91886165, -8.42110634));
    var options = {
        bounds: defaultBounds,
        strictBounds: true,
        types: ['address']
    };
    var input = document.getElementById('input_address');

    autocomplete = new google.maps.places.Autocomplete(input, options);


}
