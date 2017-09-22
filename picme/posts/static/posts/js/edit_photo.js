var myImage = new Image();
var csrftoken = getCookie('csrftoken');

window.onload = function () {
            myImage.src = document.getElementById('photo_src').value; // change this later
            var container = document.getElementById('editor');
            var editor = new PhotoEditorSDK.UI.ReactUI({
                title: "Picture Editor",
                container: container,
                apiKey: 'pLuxL_CL24sm4JN5UIZGWQ', // <-- Please replace this with your API key
                assets: {
                    baseUrl: '/static/posts/assets' // <-- This should be the absolute path to your `assets` directory
                },
                enableWebcam: false,
                enableUpload: false,
                editor: {
                    image: myImage,
                    export: {
                        showButton: true,
                        download: false,
                        type: PhotoEditorSDK.RenderType.DATAURL
                    }
                }

            });


            editor.on('export', (dataURL) => {
                id = document.getElementById('ID').value;
                $.ajax({
                    type: "POST",
                    url: "/posts/update_photo/"+id,
                    data: {
                        image: dataURL,
                        csrfmiddlewaretoken: csrftoken
                    },
                    success: function(response){
                        window.location = "/posts/edit/"+id
                    }
                }).done(function() {
                    console.log('saved');
                })
            })
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


