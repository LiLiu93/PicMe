(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();
  }); // end of document ready
})(jQuery); // end of jQuery name space


// use this function to make the post clickable
// and direct to detail page
function goToPostDetail(web) {
	window.location.href = web;
}

