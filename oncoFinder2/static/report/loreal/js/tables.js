
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


function drawGeneTable(id, file_name){
	
	// FIRST DOC
	$('#'+id).DataTable( {
    	"paging":   true,
        "iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        
        "dom": 'Bfrtip',
        "buttons": [
                  {extend: 'csv',
                  title: file_name},
                  
                  {extend: 'pdf',
                  title: file_name},
                 'print'
                 ],
        "ajax": {'url':'/report-portal/genetablejson/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': file_name,
        	            }
        	    	 }
    } );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table.path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var path_name = $(this).text();
    	var db = $(this).next().text();
    	showPathDetails(path_name, db, file_name, sample);    	
    	
    });
}


function drawPathwayTable(id, file_name1, file_name2){
	
	// FIRST DOC
	$('#'+id).DataTable( {
    	"paging":   true,
    	"iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        
        "dom": 'Bfrtip',
        "buttons": ['csv', 'pdf', 'print'],
        
        "ajax": {'url':'/report-portal/pathwaytablejson/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name1': file_name1,
        	            'file_name2': file_name2}
        	    	 }
    } );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table.path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var path_name = $(this).text();
    	var db = $(this).next().text();
    	showPathDetails(path_name, db, file_name, sample);    	
    	
    });
}




$(document).ready(function() {
	
	
	drawGeneTable('tbl-gene-nhk', 'output_loreal_preprocessed_NHK.txt.xlsx')
	drawGeneTable('tbl-gene-type1', 'output_loreal_preprocessed_RhE (Type 1).txt.xlsx')
	drawGeneTable('tbl-gene-type2', 'output_loreal_preprocessed_RhE (Type 2).txt.xlsx')
	drawGeneTable('tbl-gene-type3', 'output_loreal_preprocessed_RhE (Type 3).txt.xlsx')
	
	
	drawPathwayTable('tbl-nhk-type1', 
			         'output_loreal_preprocessed_NHK.txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx')
	drawPathwayTable('tbl-nhk-type2', 
			         'output_loreal_preprocessed_NHK.txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx')
	drawPathwayTable('tbl-nhk-type3', 
			         'output_loreal_preprocessed_NHK.txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx')
	drawPathwayTable('tbl-type1-type2', 
			         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx')
    drawPathwayTable('tbl-type1-type3', 
			         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx')
	drawPathwayTable('tbl-type2-type3', 
			         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx')
    drawPathwayTable('tbl-all', 
			         'all', 
			         'all')
	
    
	
	
    
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
