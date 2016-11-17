// BOX PLOT FOR GENES
	
	var options = {

        chart: {
            type: 'boxplot',
            renderTo: 'gene_plot',
            
        },

        title: {
            text: name
        },

        legend: {
            enabled: false
        },

        xAxis: {
            categories: ['ES', 'EPL', 'ASC', 'ABC', 'AEC', 'ANC' , 'CCL'],
            title: {
                text: 'Group'
            }
        },

        yAxis: {
            title: {
                text: 'Log2(Expression level)'
            },
            
        },

        series: [{
            name: 'Observations',
            data: [
                [760, 801, 848, 895, 965],
                [733, 853, 939, 980, 1080],
                [714, 762, 817, 870, 918],
                [724, 802, 806, 871, 950],
                [834, 836, 864, 882, 910]
            ],
            tooltip: {
                headerFormat: '<em>Experiment No {point.key}</em><br/>'
            }
        }]

    }

	
function drawGeneChart(reportID, gene_name, categories){
		
		$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 80%; height: 400px; margin: 0 auto"></div>');
		
		$("#myModalLabel").text(gene_name);
		
		$('#pathmodal').modal('show');
		
		categories = categories.replace(/u&#39;/g, "");
		categories = categories.replace(/&#39;/g, "");
		categories = categories.replace('[', "");
		categories = categories.replace(']', "");
		
		$.getJSON('/report-portal/report-genesboxplotjson/',
				{
			     'reportID': reportID,
			     'gene': gene_name,
			     'categories': categories
			     },
			     function(data) {
			    	 
			    	$("#loading").empty();
			     	options.series[0] = data;
			     	options.title.text = gene_name;
			     	
			     	if (reportID == 4){
			     	  //if only one category for vulcano
			     	  lcategories = categories.split(',')
			     	  if (lcategories.length<2){
			     		  if(lcategories[0].indexOf('A549') !== -1) categories+=',DMSO_A549';
			     		  if(lcategories[0].indexOf('MCF7') !== -1) categories+=',DMSO_MCF7';
			     	  }
			     	  else{
			     		categories+=',DMSO_A549,DMSO_MCF7';
			     	  }
			     	
			       }
			     	
			     	options.xAxis.categories = categories.split(',');
			     	
			     	if (reportID == 6){
			     		
			     		if (categories.split(',').length<=2) options.xAxis.categories = ['Case', 'Reference'];
			     		
			     	}
			     	
			        var chart = new Highcharts.Chart(options);
			        
			     }).fail(function( jqxhr, textStatus, error ) {
			    	    var err = textStatus + ", " + error;
			    	    console.log( "Request Failed: " + err );
			    	    
			    	    $("#loading").empty().text(err);
			    	    
			    	    
			    	});

	}
	
function showPathDetails(reportID, path_name, group_name, organism){
	$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="f" style="width: 800px; height: 400px; margin: 0 auto"></div>');
	
	$("#myModalLabel").text(path_name);
	
	$('#pathmodal').modal('show');
	
	$.get("/report-portal/report-ajaxpathdetail/",
			{
		     reportID: reportID,
		     pathway: path_name,
		     group_name: group_name,
		     organism: organism,
		     		
			},
			function(data){
				$("#modalBody").html(data);
			}
			);
}



function drawGeneTable(reportID, id, file_name, categories){
	
	// FIRST DOC
	var table = $('#'+id).DataTable( {
    	"paging":   true,
        "iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        "dom": 'Bfrtip',
        "scrollX": true,
        "buttons": [
                   {extend: 'csv', title: file_name},
                   {extend: 'print', title: file_name}
                   
              ],
        
        "ajax": {'url':'/report-portal/report-genetablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	     reportID: reportID,
        	            'file_name': file_name,
        	            'categories': categories
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table#"+id+".path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	
    	drawGeneChart(reportID, gene_name, categories);    	
    	
    });
}


function drawGeneTableScatter(reportID, id, file_name, categories){
	
	// FIRST DOC
	var table = $('#'+id).DataTable( {
    	"paging":   true,
        "iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        "dom": 'Bfrtip',
        "scrollX": true,
        "buttons": [
                   {extend: 'csv', title: file_name},
                   {extend: 'print', title: file_name}
                   
              ],
        
        "ajax": {'url':'/report-portal/report-genetablescatterjson/',
        	     'type': 'GET',
        	     'data':{
        	    	     reportID: reportID,
        	            'file_name': file_name,
        	            'categories': categories
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table#"+id+".path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	
    	drawGeneChart(reportID, gene_name, categories);    	
    	
    });
}

function drawPathwayTable(reportID, id, file_name1, file_name2, is_metabolic, organism){
	
	
	var table = $('#'+id).DataTable( {
    	"paging":   true,
    	"iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        
        "info":     false,
        "autoWidth": false,
        "scrollX": false,
        "dom": 'Bfrtip',
        "buttons": [{extend: 'csv', title: id}, {extend: 'pdf', title: id} , {extend: 'print', title: id}],
        
        "ajax": {'url':'/report-portal/report-pathwaytablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	    'reportID': reportID,
        	            'file_name1': file_name1,
        	            'file_name2': file_name2,
        	            'is_metabolic': is_metabolic}
        	    	 }
    } );
	
	if(!is_metabolic){
	
		if(file_name1!='all'){
	
	    $('#'+id).on( 'draw.dt', function () {
	    	
	    	var path_name_td = $(table).find(" tr td:first-child()");
	    	path_name_td.each(function(){
	    		var path_long_name = $(this).text();
	    		if(path_long_name.length > 50){
		    		var short_name = $.trim(path_long_name).substring(0, 50)
	                .trim(this) + "...";
		    		$(this).html("<span title='"+path_long_name+"'>"+short_name+"</span>");
		    	}
	    	});	    	
	    	
	    	$("table#"+id+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
    	    $("table#"+id+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>')
        } );
	    
        $('#'+id+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
    	    var path_name = $(this).prev().text();    	
    	    showPathDetails(reportID, path_name, file_name1);
    	   
    	
                                                                        });
        $('#'+id+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
    	    var path_name = $(this).prev().prev().text();    	
    	    showPathDetails(reportID, path_name, file_name2);
    	    
    	
                                                                        });
	    }
	    else {
		    $('#'+id).on( 'draw.dt', function () {
		    	
		    	var path_name_td = $("table#"+id+".path tr td:first-child()");
		    	//alert('draw')
		    	
		    	
		    	
		    	path_name_td.each(function(){
		    		var path_long_name = $(this).text();	    		
		    		
		    		
		    		
		    		if ($(this).text().indexOf("...") >= 0) $(this).text($(this).attr('long_name'));
		    		
		    		if($(this).text().length > 50){
			    		var short_name = $.trim(path_long_name).substring(0, 50)
		                .trim(this) + "...";
			    		$(this).html("<span title='"+path_long_name+"' long_name='"+path_long_name+"'>"+short_name+"</span>");
			    	}
		    		else {
		    			//alert(path_long_name)
		    			$(this).html("<span title='"+path_long_name+"'>"+path_long_name+"</span>");
		    		}
		    		
		    		
		    		
		    		
		    	});	  
		    	
		    	
		    	
	    	    $("table#"+id+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(4)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(5)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(6)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(7)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(8)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(9)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(10)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(11)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(12)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(13)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(14)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(15)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(16)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(17)").wrapInner('<a href="#/"></a>');
	    	    
	    	    
	        } );
		    
		    table.columns.adjust().draw();
		
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
	    	    var path_name = $(this).prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
	    	    var path_name = $(this).prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(4)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(5)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(6)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(7)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(8)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(9)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(10)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(11)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(12)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(13)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    //////
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(14)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(15)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(16)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(17)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, organism);    	    	
	                                                                              });
		
	}
	
	} // end of is_metabolic
	else{
         $('#'+id).on( 'draw.dt', function () {
	    	
	    	var path_name_td = $("table#"+id+".path tr td:first-child()");
	    	path_name_td.each(function(){
	    		var path_long_name = $(this).text();
	    		if(path_long_name.length > 50){
		    		var short_name = $.trim(path_long_name).substring(0, 50)
	                .trim(this) + "...";
		    		$(this).html("<span title='"+path_long_name+"'>"+short_name+"</span>");
		    	}
	    	});	    	
    	    
	    	
        } );
	}
}




$(document).ready(function() {
	
/*	
	// GENES
	
	drawGeneTable('tbl-EPL_vs_ABC', 'EPL_vs_ABC.DE.tab');
	drawGeneTable('tbl-EPL_vs_AEC', 'EPL_vs_AEC.DE.tab');
	drawGeneTable('tbl-EPL_vs_ANC', 'EPL_vs_ANC.DE.tab');
	drawGeneTable('tbl-EPL_vs_ASC', 'EPL_vs_ASC.DE.tab');
	drawGeneTable('tbl-EPL_vs_CCL', 'EPL_vs_CCL.DE.tab');
	drawGeneTable('tbl-EPL_vs_ES', 'EPL_vs_ES.DE.tab');
	
	drawGeneTable('tbl-gene_all', 'all');
		
	
	
	
	// SIGNALING PATHS
	
	
    
    drawPathwayTable('tbl-path_all', 
			         'all', 
			         'all', false);
			     
    	
 // METABOLIC PATHS
	
	

    drawPathwayTable('tbl-meta_all', 
	         'all', 
	         'all', true);
	
	
 */   
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
