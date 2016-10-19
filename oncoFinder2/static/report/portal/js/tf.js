
// Transcription Factor

function drawTFTable(reportID, id, file_name, tf_group_name){
	
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
        
        "ajax": {'url':'/report-portal/report-tftablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	     reportID: reportID,
        	            'file_name': file_name,
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table#"+id+".path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var tf_name = $(this).text();
    	
    	drawTFGraph(reportID, tf_name, tf_group_name);    	
    	
    });
}

function drawTFGraph(reportID, tf_name, tf_group_name){
	$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 800px; height: 400px; margin: 0 auto"></div>');
	
	$("#myModalLabel").text(tf_name);
	
	$('#pathmodal').modal('show');
	
	
	$.get("/report-portal/report-ajaxtfdetail/",
			{
		     reportID: reportID,
		     tf_name: tf_name,
		     group_name: tf_group_name,
		     		
			},
			function(data){
				$("#modalBody").html(data);
			}
			);
}



