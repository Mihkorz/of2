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
	function sameOrigin(url) {
	    // test that a given url is a same-origin URL
	    // url could be relative or scheme relative or absolute
	    var host = document.location.host; // host + port
	    var protocol = document.location.protocol;
	    var sr_origin = '//' + host;
	    var origin = protocol + sr_origin;
	    // Allow absolute or scheme relative URLs to same origin
	    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	        // or any other URL that isn't scheme relative or absolute i.e relative.
	        !(/^(\/\/|http:|https:).*/.test(url));
	}

 $.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	    	if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
	            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	        }
	    }
	});

/** organism and database arguments may be nulls. */
function autocompleteAjaxSearch(searchObj, organism, database, loadObj, url) {
    var query = $(searchObj).val();

    if (query.length == 0) {
        //alert($(location).attr('href') + "#"+$(loadObj).attr('id'))
        $(loadObj).load($(location).attr('href') + " #" + $(loadObj).attr('id'));
    }

    if (query.length >= 3) {
        var fullQuery = url + "/search/?q=" + query;
        if (organism != null) {
            fullQuery += "&o=" + organism;
        }
        if (database != null) {
            fullQuery += "&db=" + database;
        }

        $(loadObj).fadeOut('slow', function () {
            $(loadObj).load(fullQuery, function () {
                $(loadObj).fadeIn('slow');
            });
        });
    }
}
