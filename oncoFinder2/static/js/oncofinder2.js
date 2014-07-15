 $(function(){
	 
	 
	 $('div.pr_header_menu, span').tooltip();
	 
	 $('.with-tooltip').tooltip();
 
 
 
 });
 
 function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }
 
 function csrfSafeMethod(method) {
     // these HTTP methods do not require CSRF protection
     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
 }
 
 function autocompleteAjaxSearch(searchObj, loadObj, url){
	 var query = $(searchObj).val();
	 
	 if (query.length == 0) {
		 //alert($(location).attr('href') + "#"+$(loadObj).attr('id'))
		 $(loadObj).load($(location).attr('href') + " #"+$(loadObj).attr('id'));
	 }
	 
	 if (query.length >= 3){
		 
		 $(loadObj).fadeOut('slow', function(){
			                 $(loadObj).load(url+"/search/?q="+query, function(){
			                	 $(loadObj).fadeIn('slow');
			                  });
			                  
		 });
		 
	 }
	
	 
 }