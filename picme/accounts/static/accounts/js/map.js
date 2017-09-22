$(document).ready(function () {
    jQuery(function () {
        // Asynchronously Load the map API
        var script = document.createElement('script');
        script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyCiyqhxEO_GOK25D9xry5vmOPanYLQZgIU&callback=refresh_map&language=en";
        document.body.appendChild(script);
    });
});

function refresh_map() {
    var markers = [];

    var infoWindowContent = [];

    var pathname = window.location.pathname;

    var username = pathname.split('/').slice(-2, -1)[0];

    var location = window.location;
    var domain = location.protocol + "//" + location.hostname + ":" + location.port;

    $.ajax({
        url: domain + '/posts/loc_post/' + username,
        method: 'GET',

        success: function (json) {
            for (var i = 0; i < json.length; i++) {
                var city_name;
                var cap_city = json[i][0][0];
                var name_array = cap_city.split(' ');
                var length = cap_city.split(' ').length;

                city_name = name_array[0].substring(0, 1) + name_array[0].substring(1, name_array[0].length).toLowerCase();
                if (length > 1) {
                    for (var j = 1; j < length; j++) {
                        city_name = city_name + ' ' + name_array[j].substring(0, 1) + name_array[j].substring(1, name_array[j].length).toLowerCase() + ' ';
                    }
                }

                var state_abv = json[i][1];
                var latitude = json[i][2];
                var longitude = json[i][3];
                var num_post = json[i][4];
                markers.push([
                    city_name + ', ' + state_abv, latitude, longitude
                ]);
                infoWindowContent.push([
                    '<div class="info_content">' +
                    '<h5>' + city_name + ', ' + state_abv + '</h5>' +
                    '<a href="/posts/search/?key='+city_name+'"><p>' + num_post + ' post(s)</p></a>' + '</div>'
                ]);
            }

            var map;
            var bounds = new google.maps.LatLngBounds();
            var mapOptions = {
                mapTypeId: 'roadmap'
            };

            // Display a map on the page
            map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

            var country = 'United States';

            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({'address': country}, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    map.setCenter(results[0].geometry.location);
                    map.setZoom(4);
                } else {
                    alert("Could not find location: " + location);
                }
            });

            map.setTilt(45);

            // Display multiple markers on a map
            var infoWindow = new google.maps.InfoWindow(), marker, i;

            // Loop through our array of markers & place each one on the map
            for (i = 0; i < markers.length; i++) {
                var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
                bounds.extend(position);
                marker = new google.maps.Marker({
                    position: position,
                    map: map,
                    title: markers[i][0]
                });

                // Allow each marker to have an info window
                google.maps.event.addListener(marker, 'click', (function (marker, i) {
                    return function () {
                        infoWindow.setContent(infoWindowContent[i][0]);
                        infoWindow.open(map, marker);
                    }
                })(marker, i));

                // Automatically center the map fitting all markers on the screen
                map.fitBounds(bounds);
            }
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + '  ' + err);
        }
    });
}

// window.onload = refresh_map;