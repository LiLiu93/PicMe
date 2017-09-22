$(document).ready(function(){
	$('body').on("click",'.heart',function(){

		var A=$(this).attr("id");
		var B=A.split("like");
		var messageID=B[1];
		var C=parseInt($("#likeCount"+messageID).html());
		$(this).css("background-position","")
		var D=$(this).attr("rel");
  
		if(D === 'like') {      
			$("#likeCount"+messageID).html(C+1);
			$(this).addClass("heartAnimation").attr("rel","unlike");
		}
		else{
			$("#likeCount"+messageID).html(C-1);
			$(this).removeClass("heartAnimation").attr("rel","like");
			$(this).css("background-position","left");
		}
		updateLike(messageID);
	});
});

function updateLike(id) {
  	$.ajax({
   		url: "/posts/like_post/"+id
	});
}