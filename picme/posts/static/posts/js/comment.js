// Sends a new request to update the to-do list
function getList() {
    var id = document.getElementById("ID").value;

    $.ajax({
        url: "/posts/get_comment/"+id,
        dataType : "json",
        success: getAllList
    });
}

function getAllList(items) {
    var list = document.getElementById("comments");
    if (!list.hasChildNodes()) {
        for (var i = items.length-1; i >= 0; i--) {
            // console.log(items);
            tem = '<li class="collection-item"><p>'+ 
            sanitize(items[i]["content"]) +
            '</p> </br> ' + items[i]["name"]+ '&nbsp&nbsp&nbsp' +
            items[i]["time"] +  '</li>';
            $("#comments").append(tem);
        }
    } else {
        if (list.childElementCount != items.length) {
            while (list.hasChildNodes()) {
                list.removeChild(list.firstChild);
            }
            for (var j = items.length-1; j >= 0; j--) {

                tem = '<li class="collection-item"><p>'+ sanitize(items[j]["content"]) +'</p> </br> ' +items[j]["name"] + '&nbsp&nbsp&nbsp' +items[j]["time"] + '</li>';
                $("#comments").append(tem);
            }
        }
    }
}

function add(items) {
    var list = document.getElementById("comments");
    // console.log(items);
    tem = '<li class="collection-item"><p>'+ 
    sanitize(items[0]["content"]) +
    '</p> </br> ' + items[0]["name"]+ '&nbsp&nbsp&nbsp' +
    items[0]["time"] +  '</li>';
    $("#comments").prepend(tem);
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/(\r\n|\n|\r)/gm,"");
}

function addComment() {
    var itemTextElement = document.getElementById("content");
    var itemTextValue   = itemTextElement.value;
    itemTextElement.value = '';
    var id = document.getElementById("ID").value;

    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var response = JSON.parse(req.responseText);
        if (Array.isArray(response)) {
            add(response);
        } else {
            displayError(response.error);
        }
    };

    req.open("POST", "/posts/add_comment/"+id+"/", true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("content="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());

}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

window.onload = getList;

window.setInterval(getList, 5000);