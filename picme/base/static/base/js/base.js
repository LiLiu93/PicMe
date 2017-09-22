$( document ).ready(function() {
    $(".button-collapse").sideNav();
});

function unread_message() {
    $('.unread').remove();
    var location = window.location;
    var domain = location.protocol + "//" + location.hostname + ":" + location.port;

    $.ajax({
        url: domain + '/dialogs/unread/message',
        method: 'GET',

        success: function (json) {
            console.log(json);
            if (json === false) {
                $('#dropdown1')
                    .append("<li class='unread'><a href='#'>No new message</a></li>");
            } else {
                for (var i = 0; i < json.length; i++) {
                    $('#dropdown1')
                        .append("<li class='unread'><a href='"+ domain + "/dialogs/"+ json[i][0] + "'>" + json[i][0] + "  (" + json[i][2] + ") </a></li>");
                }
            }

        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            alert("Something went wrong");
        }
    })
}

