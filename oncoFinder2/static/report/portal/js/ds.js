
// Drug Scoring

function drawDSTable(reportID, id, file_name, ds_group_name){
	
	// FIRST DOC
	var table = $('#'+id).DataTable( {
    	"paging":   true,
        "iDisplayLength": 20,
        "ordering": true,
        "order": [[ 7, "desc" ]],
        "info":     false,
        "dom": 'Bfrtip',
        "scrollX": true,
        "buttons": [
                   {extend: 'csv', title: file_name},
                   {extend: 'print', title: file_name}
                   
              ],
        
        "ajax": {'url':'/report-portal/report-dstablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	     reportID: reportID,
        	            'file_name': file_name,
        	            'ds_group_name': ds_group_name,
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	/*
	$('#'+id).on( 'draw.dt', function () {
    	$("table#"+id+".path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var tf_name = $(this).text();
    	
    	drawTFGraph(reportID, tf_name, tf_group_name);    	
    	
    });*/
}

function drawDSBarplot(reportID, renderTo, file_name, ds_group_name, pert_type){
	// BOX PLOT Drug Scoring
	
	var bar_options = {
	        chart: {
	        	renderTo: renderTo,
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
			        text: 'Effect'
			      }
			    },
	        credits: {
	            enabled: false
	        },
	        series: [{},]
	    }
	
	$.getJSON('/report-portal/report-dsboxplotjson/',
    		{
		     reportID: reportID,
		     file_name: file_name,
		     ds_group_name: ds_group_name,
		     pert_type: pert_type
    		},
    		function(data){
				
				
				bar_options.title.text = ds_group_name
				bar_options.xAxis.categories = data['categories_name'];						
				
				
				bar_options.series[0].data = data["series"];
				bar_options.series[0].name = ds_group_name+' effect';
				
				
		        var chart = new Highcharts.Chart(bar_options);
			});
}


