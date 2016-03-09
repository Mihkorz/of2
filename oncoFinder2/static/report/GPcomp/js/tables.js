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

	
function drawGeneChart(gene_name, file_name){
		$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 500px; height: 400px; margin: 0 auto"></div>');
		
		$("#myModalLabel").text(gene_name);
		
		$('#pathmodal').modal('show');
		
		$.getJSON('/report-portal/bt-genesboxplotjson/',
				{
			     'gene': gene_name,
			     },
			     function(data) { 
			    	 $("#loading").empty();
			     	options.series[0] = data;
			     	options.title.text = gene_name;
			     	
			     	
			        var chart = new Highcharts.Chart(options);
			     })

	}
	
function showPathDetails(path_name, filename, tab){
	
	if (tab == null) {
	    tab='mcf7' 
	}
	
	$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 800px; height: 400px; margin: 0 auto"></div>');
	
	$("#myModalLabel").text(path_name);
	
	$('#pathmodal').modal('show');
	
	$.get("/report-portal/report/gp-ajaxpathdetail/",
			{
		     pathway: path_name,
		     filename: filename,
		     tab: tab
		     		
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
                   {extend: 'print', title: file_name}
                   
              ],
        
        "ajax": {'url':'/report-portal/bt-genetablejson/',
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
    	
    	drawGeneChart(gene_name);    	
    	
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
        "buttons": [{extend: 'csv', title: id}, {extend: 'pdf', title: id} , {extend: 'print', title: id}],
        
        "ajax": {'url':'/report-portal/gp-pathwaytablejson/',
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
	    	
	    	var path_name_td = $("table#"+id+".path tr td:first-child()");
	    	path_name_td.each(function(){
	    		var path_long_name = $(this).text();
	    		if(path_long_name.length > 70){
		    		var short_name = $.trim(path_long_name).substring(0, 70)
	                .trim(this) + "...";
		    		$(this).html("<span title='"+path_long_name+"'>"+short_name+"</span>");
		    	}
	    	});	    	
    	    
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
		    	
		    	var path_name_td = $("table#"+id+".path tr td:first-child()");
		    	path_name_td.each(function(){
		    		var path_long_name = $(this).text();
		    		if(path_long_name.length > 70){
			    		var short_name = $.trim(path_long_name).substring(0, 70)
		                .trim(this) + "...";
			    		$(this).html("<span title='"+path_long_name+"'>"+short_name+"</span>");
			    	}
		    		else {
		    			$(this).html("<span title='"+path_long_name+"'>"+path_long_name+"</span>");
		    		}
		    	});	  
		    	
		    	
	    	    $("table#"+id+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(4)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(5)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(6)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(7)").wrapInner('<a href="#/"></a>');
	        } );
		
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
	    	    var path_name = $(this).prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
	    	    var path_name = $(this).prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(4)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(5)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(6)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(7)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		
	}
	
	} // end of is_metabolic
}




$(document).ready(function() {
	
	
	// GENES
	/*
	drawGeneTable('tbl-EPL_vs_ABC', 'EPL_vs_ABC.DE.tab');
	drawGeneTable('tbl-EPL_vs_AEC', 'EPL_vs_AEC.DE.tab');
	drawGeneTable('tbl-EPL_vs_ANC', 'EPL_vs_ANC.DE.tab');
	drawGeneTable('tbl-EPL_vs_ASC', 'EPL_vs_ASC.DE.tab');
	drawGeneTable('tbl-EPL_vs_CCL', 'EPL_vs_CCL.DE.tab');
	drawGeneTable('tbl-EPL_vs_ES', 'EPL_vs_ES.DE.tab');
	
	drawGeneTable('tbl-gene_all', 'all');
		
	*/
	
	
	// SIGNALING PATHS
	
	
    
    drawPathwayTable('tbl-path_all', 
			         'all', 
			         'all', false);
    
    drawPathwayTable('MCF7_tbl-path_all', 
	         'all', 
	         'MCF7', false);
			     
    	
 // METABOLIC PATHS
	
	

    drawPathwayTable('tbl-meta_all', 
	         'all', 
	         'all', true);
    drawPathwayTable('meta_MCF7_tbl-path_all', 
	         'all', 
	         'MCF7', true);
	
	
    
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
