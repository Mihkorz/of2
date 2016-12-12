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
	                text: 'Probability'
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


function drawAntineoplasticColumn(report_id, renderTo){
	
	var options = {
				
			
		        chart: {
		        	renderTo: renderTo,
		            type: 'column',
		            marginLeft: 100,
		            height: 500,
		            
		        },
		        credits:{enabled:false},
		        title: {
		            text: 'Antineoplastic potential'
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
		                text: 'Probability'
		            },
		            
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
		            data: [['INS-541', 0.82],
		                   ['INS-186', 0.76],
		                   ['INS-523', 0.86],
		                   [' ', 0],
		                   [' ', 0],
		                   [' ', 0],
		                   ['Drug 10', 0.57],
		                   ['Drug 12', 0.64],
		                   ['Drug 15', 0.70],
		                   ['Drug 29', 0.67],
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
		        ]
		    }
		
		    
	var chart = new Highcharts.Chart(options); 
	   		

	}

function drawNumSideEffColumn(report_id, renderTo){
	
	var options = {
				
			
		        chart: {
		        	renderTo: renderTo,
		            type: 'column',
		            marginLeft: 100,
		            height: 500,
		            
		        },
		        credits:{enabled:false},
		        title: {
		            text: 'Number of predicted side effects'
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
		                text: 'Number'
		            },
		            
		        },
		        legend: {
		            enabled: false
		        },
		        tooltip: {
		            pointFormat: 'Side Effects number: <b>{point.y}</b>'
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
                           ['Drug 10', 48],
                           ['Drug 12', 39],
                           ['Drug 15', 46],
                           ['Drug 29', 50],
		                   [' ', 0],
		                   [' ', 0],
		                   [' ', 0],
		                   ['INS-541', 23],
		                   ['INS-186', 29],
		                   ['INS-523', 40],
		                   
		            ],
		            dataLabels: {
		                enabled: true,
		                rotation: -90,
		                color: '#FFFFFF',
		                align: 'right',
		                format: '{point.y}', // one decimal
		                y: 10, // 10 pixels down from the top
		                style: {
		                    fontSize: '13px',
		                    fontFamily: 'Verdana, sans-serif'
		                }
		            }
		        },
		        ]
		    }
		
		    
	var chart = new Highcharts.Chart(options); 
	   		

	}
