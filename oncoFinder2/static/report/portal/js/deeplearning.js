//-------------------------------------------------------
Highcharts.Renderer.prototype.symbols.hline = function(x, y, width, height) {
    return ['M',x ,y + height / 2,'L',x+width,y + width / 2];
};
//-------------------------------------------------------


function drawDLColumn(report_id, renderTo, group_name, type){
	
var options = {
			
		
	        chart: {
	        	renderTo: renderTo,
	            type: 'column',
	            marginLeft: 100,
	            height: 500,
	            
	        },
	        credits:{enabled:false},
	        title: {
	            text: 'Side Effects'
	        },
	        subtitle: {
	            text: ''
	        },
	        xAxis: {
	            type: 'category',
	            labels: {
	            	step:1,
	                rotation: -45,
	                style: {
	                    fontSize: '10px',
	                    fontFamily: 'Verdana, sans-serif'
	                }
	            }
	        },
	        yAxis: {
	            min: 0,
	            title: {
	                text: 'Value'
	            }
	        },
	        legend: {
	            enabled: false
	        },
	        tooltip: {
	            pointFormat: 'Mean Value: <b>{point.y:.2f}</b>'
	        },
	        
	        plotOptions:{
	            
	            scatter:{
	                marker:{
	                    symbol:'hline',
	                    lineWidth:2,
	                    radius:9,
	                    lineColor:'#333'
	                }
	            }
	        },
	        
	        series: [{
	        	type: 'column',
	            name: 'Farm classes',
	            data: [
	                
	            ],
	            dataLabels: {
	                enabled: true,
	                rotation: -90,
	                color: '#FFFFFF',
	                align: 'right',
	                format: '{point.y:.2f}', // one decimal
	                y: 10, // 10 pixels down from the top
	                style: {
	                    fontSize: '13px',
	                    fontFamily: 'Verdana, sans-serif'
	                }
	            }
	        },
	        {
	            name:'threshold',
	            type:'scatter',
	            zIndex:20,
	            data:[],
	            tooltip: {
		            pointFormat: 'value: <b>{point.y}</b>'
		        },
	        }]
	    }
	
	    
	    
    $.getJSON('/report-portal/report-deeplearningfarmjson/',
    		{
    	     'report_id': report_id,
    	     'group_name': group_name,
    	     'type': type
    		},
    		function(data) {
    	data = $.parseJSON(data);
    	
    	options.series[0].data = data['barplot'];
    	options.series[1].data = data['threshold'];
    	options.title.text = data['title']
    	options.subtitle.text = data['subtitle']
    	
    	
        var chart = new Highcharts.Chart(options);
    });
	

}

function drawSimilarityTable(reportID, id, file_name, sim_group_name){
	
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
                   {extend: 'csv', title: 'similarity table'},
                   {extend: 'print', title: 'similarity table'}
                   
              ],
        
        "ajax": {'url':'/report-portal/report-similaritytablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	     'reportID': reportID,
        	    	     'sim_group_name': sim_group_name,
        	            
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	
}

function drawPotentialTargetsTable(reportID, id, file_name, pt_group_name){
	
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
                   {extend: 'csv', title: 'similarity table'},
                   {extend: 'print', title: 'similarity table'}
                   
              ],
        
        "ajax": {'url':'/report-portal/report-potenttargetstablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	     'reportID': reportID,
        	    	     'pt_group_name': pt_group_name,
        	            
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	
}


