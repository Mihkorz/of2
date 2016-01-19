// CHART FOR GENES
	
	var options = {
	        chart: {
	        	renderTo: 'gene_plot',
	            type: 'column'
	        },
	        title: {
	            text: 'MTOR gene'
	        },
	        xAxis: {
	        	type: 'category',
	        	labels: {
	        		rotation: -45,
	        	}
	            
	        },
	        yAxis: {
			      title: {
			        text: 'log2(Expression level)'
			      }
			    },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: 'NHE',
	            color: 'grey',
	            
	        }, {
	            name: 'Case',
	            color: 'red',
	            
	        }, ]
	    }

	
function drawGeneChart(gene_name, file_name){
		$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 500px; height: 400px; margin: 0 auto"></div>');
		
		$("#myModalLabel").text(gene_name);
		
		$('#pathmodal').modal('show');
		
		$.getJSON('/report-portal/genedetailjson/',
				{'gene': gene_name,
			     'file_name': file_name},
				function(data){
					
					$("#loading").empty();
					
					options.title.text = gene_name+' gene'
					
					options.series[0].data = data['NHE'];
					options.series[1].data = data['Case'];
					
			        var chart = new Highcharts.Chart(options);
				})

	}
	
function showPathDetails(path_name, filename){
	$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 800px; height: 400px; margin: 0 auto"></div>');
	
	$("#myModalLabel").text(path_name);
	
	$('#pathmodal').modal('show');
	
	$.get("/report-portal/report/ajaxpathdetail/",
			{
		     pathway: path_name,
		     filename: filename,
		     		
			},
			function(data){
				$("#modalBody").html(data);
			}
			);
}



function drawGeneTable(id, file_name){
	
	// FIRST DOC
	var table = $('#'+id).DataTable( {
    	"paging":   true,
        "iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: file_name},
                   'print'
              ],
        
        "ajax": {'url':'/report-portal/genetablejson/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': file_name,
        	            },
        	      
        
    },"deferRender": true });
	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table#"+id+".path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	
    	drawGeneChart(gene_name, file_name);    	
    	
    });
}


function drawPathwayTable(id, file_name1, file_name2, is_metabolic){
	
	
	$('#'+id).DataTable( {
    	"paging":   true,
    	"iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        
        "dom": 'Bfrtip',
        "buttons": [{extend: 'csv', title: id}, 'pdf', 'print'],
        
        "ajax": {'url':'/report-portal/pathwaytablejson/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name1': file_name1,
        	            'file_name2': file_name2,
        	            'is_metabolic': is_metabolic}
        	    	 }
    } );
	
	if(!is_metabolic){
	
		if(file_name1!='all'){
	
	    $('#'+id).on( 'draw.dt', function () {
    	    $("table#"+id+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
    	    $("table#"+id+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>')
        } );
	
        $('#'+id+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
    	    var path_name = $(this).prev().text();    	
    	    showPathDetails(path_name, file_name1);    	
    	
                                                                        });
        $('#'+id+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
    	    var path_name = $(this).prev().prev().text();    	
    	    showPathDetails(path_name, file_name2);    	
    	
                                                                        });
	    }
	    else {
		    $('#'+id).on( 'draw.dt', function () {
	    	    $("table#"+id+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(4)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(5)").wrapInner('<a href="#/"></a>');
	        } );
		
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
	    	    var path_name = $(this).prev().text();    	
	    	    showPathDetails(path_name, 'output_loreal_preprocessed_NHK.txt.xlsx');    	
	    	
	                                                                        });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
	    	   var path_name = $(this).prev().prev().text();    	
	    	   showPathDetails(path_name,  'output_loreal_preprocessed_RhE (Type 1).txt.xlsx');    	
	    	
	                                                                        });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(4)', function () {    	
	    	  var path_name = $(this).prev().prev().prev().text();    	
	    	  showPathDetails(path_name,  'output_loreal_preprocessed_RhE (Type 2).txt.xlsx');    	
	    	
	                                                                        });
		   $('#'+id+' tbody').on( 'click', 'tr td:nth-child(5)', function () {    	
	    	var path_name = $(this).prev().prev().prev().prev().text();    	
	    	showPathDetails(path_name,  'output_loreal_preprocessed_RhE (Type 3).txt.xlsx');    	
	    	
	                                                                        });
		
	}
	
	} // end of is_metabolic
}




$(document).ready(function() {
	
	
	// GENES
	
	drawGeneTable('tbl-gene-nhk', 'output_loreal_preprocessed_NHK.txt.xlsx');
		
	drawGeneTable('tbl-gene-type1', 'output_loreal_preprocessed_RhE (Type 1).txt.xlsx');
	drawGeneTable('tbl-gene-type2', 'output_loreal_preprocessed_RhE (Type 2).txt.xlsx');
	drawGeneTable('tbl-gene-type3', 'output_loreal_preprocessed_RhE (Type 3).txt.xlsx');
	
	
	
	// SIGNALING PATHS
	
	drawPathwayTable('tbl-nhk-type1', 
			         'output_loreal_preprocessed_NHK.txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx', false);
			        
	drawPathwayTable('tbl-nhk-type2', 
			         'output_loreal_preprocessed_NHK.txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx', false);
	drawPathwayTable('tbl-nhk-type3', 
			         'output_loreal_preprocessed_NHK.txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx', false);
	drawPathwayTable('tbl-type1-type2', 
			         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx', false);
    drawPathwayTable('tbl-type1-type3', 
			         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx', false);
	drawPathwayTable('tbl-type2-type3', 
			         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx', 
			         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx', false);
    
    drawPathwayTable('tbl-all', 
			         'all', 
			         'all', false);
			     
	
 // METABOLIC PATHS
	
	drawPathwayTable('meta_tbl-nhk-type1', 
	         'output_loreal_preprocessed_NHK.txt.xlsx', 
	         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx', true);
	        
    drawPathwayTable('meta_tbl-nhk-type2', 
	         'output_loreal_preprocessed_NHK.txt.xlsx', 
	         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx', true);
    drawPathwayTable('meta_tbl-nhk-type3', 
	         'output_loreal_preprocessed_NHK.txt.xlsx', 
	         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx', true);
    drawPathwayTable('meta_tbl-type1-type2', 
	         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx', 
	         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx', true);
    drawPathwayTable('meta_tbl-type1-type3', 
	         'output_loreal_preprocessed_RhE (Type 1).txt.xlsx', 
	         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx', true);
    drawPathwayTable('meta_tbl-type2-type3', 
	         'output_loreal_preprocessed_RhE (Type 2).txt.xlsx', 
	         'output_loreal_preprocessed_RhE (Type 3).txt.xlsx', true);

    drawPathwayTable('meta_tbl-all', 
	         'all', 
	         'all', true);
	
	
    
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
