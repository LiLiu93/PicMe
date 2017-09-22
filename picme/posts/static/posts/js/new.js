$(document).ready(function() {
	$('select').material_select();
});

$('select').on('contentChanged', function() {
    // re-initialize (update)
    $(this).material_select();
});


// getCityList Function

function getCityList(code){ 
	$.ajax({   
		type: "GET",
		url: "/address/getCityList?code="+code,       
		dataType:'json',   
		success: function(data,textStatus){
			var select = document.getElementById("id_post_city");
			select.options.length = 0
			if(data.length > 0) {
				// $("#id_post_province").show();  
				for ( i=0; i<data.length; i++ ) {   
					select.options[i] = new Option();   
					select.options[i].text = data[i].name;   
					select.options[i].value = data[i].code; 
				}
				// trigger event
    			$('#id_post_city').trigger('contentChanged');
			} 
		}    
	})   
}  

$('select').change(function(){
	// alert(this.value)
	if (this.id === "id_post_state" ) {
		getCityList(this.value)
	}
});