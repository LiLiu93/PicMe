// chat room functions

$(document).ready(function() {
    $('.modal').modal();
});

// setTimeout("get_new_messages()", 1);
// setInterval("get_new_messages()", 4000);

function goToFinal() {
    var objDiv = document.getElementsByClassName("chat-content");
    objDiv.scrollTop = objDiv.scrollHeight;
}
function read_messages() {
    $.ajax({
        url: "/chat/"+user_id+"/read/",
        method: "GET",

        success: function (json) {

        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });
}
function get_new_messages() {
    $.ajax({
        url: "/chat/"+user_id+"/new_messages/",
        method: 'GET',

        success: function (json) {
            console.log("Seaching new messages...");
            for (var i = 0; i < json.length; i++) {
                $('#new-message')
                    .append("<li class='other'>" +
                            "   <div class='avatar'>" +
                            "       <img src='" + json[i][2] + "' draggable='false'>" +
                            "   </div>" +
                            "   <div class='msg'>" +
                            "       <p>" + json[i][0] + "</p>" +
                            "       <time>" + json[i][1] + "</time>" +
                            "   </div>" +
                            "</li>"
                    );

                goToFinal();
            }
            read_messages();
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');
        }
    })
}


function send_message() {
    var content = $("#field").val();
    console.log(content);
    if (content !== '') {
        $.ajax({
            url: "/chat/"+user_id+"/send/",
            method: "POST",
            data: {
                content: content
            },

            success: function (json) {
                if (json !== false) {
                    $('#new-message')
                        .append("<li class='self'>" +
                                "   <div class='avatar'>" +
                                "       <img src='"+ json[2] + "' draggable='false'>" +
                                "   </div>" +
                                "   <div class='msg'>" +
                                "       <p>" + json[0] + "</p>" +
                                "       <time>" + json[1] + "</time>" +
                                "   </div>" +
                                "</li>");

                    $('#field').val('');
                    goToFinal();
                } else {
                    alert('Could not send message');
                }
            },

            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                alert("Something went wrong");
            }
        })
    }

}

function getCookie(name) {
    var cookieValue = null;
    var i = 0;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (i; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
