
// Correlation

function drawCorrelationTable(reportID, id, file_name, tf_group_name){
	
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
        
        "ajax": {'url':'/report-portal/report-corrtablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	     reportID: reportID,
        	            'file_name': file_name,
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	$('#'+id).on( 'draw.dt', function () {
		
		var substring = 'MEXP'
		
		if ($(this).text().indexOf(substring) == -1) {
		
    	$("table#"+id+".path tr td:first-child").each(function(){
    		$(this).wrapInner('<a target="_blanc" href="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='+$(this).text()+'"></a>');
    	});
    	        
    	$("table#"+id+".path tr td:nth-child(4)").each(function(){
    		$(this).wrapInner('<a target="_blanc" href="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='+$(this).text()+'"></a>');
    	});
		}
		else{
			$("table#"+id+".path tr td:first-child").each(function(){
	    		$(this).wrapInner('<a target="_blanc" href="https://www.ebi.ac.uk/arrayexpress/experiments/'+$(this).text()+'/"></a>');
	    	});
	    	        
	    	$("table#"+id+".path tr td:nth-child(4)").each(function(){
	    		$(this).wrapInner('<a target="_blanc" href="https://www.ebi.ac.uk/arrayexpress/experiments/'+$(this).text()+'/"></a>');
	    	});
		}
    
	} );
	
	
	

}




