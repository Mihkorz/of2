
function showPathDetails(path_name, db, filename, sample){
	$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 600px; height: 400px; margin: 0 auto"></div>');
	
	$("#myModalLabel").text(path_name);
	
	$('#pathmodal').modal('show');
	
	$.get("/report-portal/report/ajaxpathdetail/",
			{
		     pathway: path_name,
		     db: db,
		     
		     filename: filename,
		     sample: sample		
			},
			function(data){
				$("#modalBody").html(data);
			}
			);
}

$(document).ready(function() {
	
	// FIRST DOC
	$('#tbl-A1209_04').DataTable( {
    	"paging":   true,
        "iDisplayLength": 10,
        "ordering": true,
        "order": [[ 3, "desc" ]],
        "info":     false,
        "bFilter": false,
        "ajax": {'url':'/report-portal/json/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': 'output_loreal_preprocessed_NHK.txt.xlsx',
        	            'sample': 'A1209_04'}
        	    	 }
    } );
	
	$('#tbl-A1209_04').on( 'draw.dt', function () {
    	$("table.path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#tbl-A1209_04 tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var path_name = $(this).text();
    	var db = $(this).next().text();
    	showPathDetails(path_name, db, 'output_loreal_preprocessed_NHK.txt.xlsx', 'A1209_04');    	
    	
    });
	
    $('#tbl-A1209_08').DataTable( {
    	"paging":   true,
        "iDisplayLength": 10,
        "ordering": true,
        "order": [[ 3, "desc" ]],
        "info":     false,
        "bFilter": false,
        "ajax": {'url':'/report-portal/json/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': 'output_loreal_preprocessed_NHK.txt.xlsx',
        	            'sample': 'A1209_08'}
        	    	 }
    } );
	
	$('#tbl-A1209_08').on( 'draw.dt', function () {
    	$("table.path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#tbl-A1209_08 tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var path_name = $(this).text();
    	var db = $(this).next().text();
    	showPathDetails(path_name, db, 'output_loreal_preprocessed_NHK.txt.xlsx', 'A1209_08');    	
    	
    });
    
    
    $('#tbl-A1209_12').DataTable( {
    	"paging":   true,
        "iDisplayLength": 10,
        "ordering": true,
        "order": [[ 3, "desc" ]],
        "info":     false,
        "bFilter": false,
        "ajax": {'url':'/report-portal/json/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': 'output_loreal_preprocessed_NHK.txt.xlsx',
        	            'sample': 'A1209_12'}
        	    	 }
    } );
	
	$('#tbl-A1209_12').on( 'draw.dt', function () {
    	$("table.path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#tbl-A1209_12 tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var path_name = $(this).text();
    	var db = $(this).next().text();
    	showPathDetails(path_name, db, 'output_loreal_preprocessed_NHK.txt.xlsx', 'A1209_12');    	
    	
    });
    
    $('#tbl-A1209_15').DataTable( {
    	"paging":   true,
        "iDisplayLength": 10,
        "ordering": true,
        "order": [[ 3, "desc" ]],
        "info":     false,
        "bFilter": false,
        "ajax": {'url':'/report-portal/json/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': 'output_loreal_preprocessed_NHK.txt.xlsx',
        	            'sample': 'A1209_15'}
        	    	 }
    } );
	
	$('#tbl-A1209_15').on( 'draw.dt', function () {
    	$("table.path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#tbl-A1209_15 tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var path_name = $(this).text();
    	var db = $(this).next().text();
    	showPathDetails(path_name, db, 'output_loreal_preprocessed_NHK.txt.xlsx', 'A1209_15');    	
    	
    });
	
	
    
} );


/*
function _render(jsonRes, templateRes, container) {
  var data = $.isArray(jsonRes) ? _.first(jsonRes) : jsonRes,
    templateString = _.first(templateRes),//.replace(/\s\s+/g, ''),
    compiled = _.template(templateString),
    compiledHtmlString = compiled(data);
  $(container).append( compiledHtmlString );
}

var names = {
  '.container5': ['metabolism_high_down', 'metabolism_high_up', 'metabolism_low_down', 'metabolism_low_up']
};

var titles = [''];



_.each(names, function(val, key){

  _.each(val, function(file){
    $.when(
      $.getJSON(file + '.json'),
      $.ajax('/js/tp/table.tp')
    ).done(function(data,tp){
        _render({lines: data[0]}, tp, key)
      })
  });


});

;*/
