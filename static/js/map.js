
    function addInfoWindow(marker, message) {
        var infoWindow = new google.maps.InfoWindow({
            content: message
        });
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.open(map, marker);
        });
    }
    function initMap() {
        var map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: {
                lat: 51.903614,
                lng: -8.468399
            }
        });
        
            var itemsLocations = document.querySelectorAll(".itemsLocations");
            for (var i = 0; i < itemsLocations.length; i++) {
                    var marker = new google.maps.Marker({
                    position: {lat: parseFloat(this.document.getElementsByClassName('lat')[i].innerHTML), lng : parseFloat(this.document.getElementsByClassName('long')[i].innerHTML)},
                    map: map,
            });
                    addInfoWindow(marker, this.document.getElementsByClassName('address')[i].innerHTML);
            };
        };
     
    
     

      

