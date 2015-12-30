$(document).ready(function(){

	var options = {
			
			chart: {
				  renderTo: 'signaling-pathways',
			      type: 'scatter',
			      zoomType: 'xy',
			      marginBottom : 100
			    },
			    title: {
			      text: 'Figure 4. Signaling pathways',
			      y: 360
			    },
			    credits: false,
			    subtitle: {
			      text: ''
			    },
			    xAxis: {
			      title: {
			        enabled: true,
			        text: 'Low GFP-p62 PAS'
			      },
			      startOnTick: true,
			      endOnTick: true,
			      showLastLabel: true
			    },
			    yAxis: {
			      title: {
			        text: 'High GFP-p62 PAS'
			      }
			    },
			    legend: {
			      enabled: false
			    },
			    plotOptions: {
			      scatter: {
			        turboThreshold: 19000,
			        marker: {
			          radius: 5,
			          states: {
			            hover: {
			              enabled: true,
			              lineColor: 'rgb(100,100,100)'
			            }
			          }
			        },
			        states: {
			          hover: {
			            marker: {
			              enabled: false
			            }
			          }
			        },
			        tooltip: {
			          headerFormat: '',
			          pointFormat: '{point.name}'
			        }
			      }
			    },

			    series: [{}]
			
	}
	
    $.getJSON('/static/report/signaling_paths.json', function(data) { 
    	
    	options.series[0].data = data;
        var chart = new Highcharts.Chart(options);
    });

  


});
