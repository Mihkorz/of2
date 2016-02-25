$(document).ready(function(){

	var options = {
			
			chart: {
				  renderTo: 'genes-unsorted-low',
			      type: 'scatter',
			      zoomType: 'xy',
			      marginBottom : 100
			    },
			    title: {
			      text: 'Figure 1. Scatterplot representing significant mean log2 gene counts of Unsorted vs Low GFP-p62 ',
			      y: 360
			    },
			    credits: false,
			    subtitle: {
			      text: ''
			    },
			    xAxis: {
			      title: {
			        enabled: true,
			        text: 'log2(Unsorted counts)'
			      },
			      startOnTick: true,
			      endOnTick: true,
			      showLastLabel: true
			    },
			    yAxis: {
			      title: {
			        text: 'log2(Low GFP-p62 counts)'
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
	
    $.getJSON('/static/report/demo/genes-unsorted-low.json', function(data) { 
    	
    	options.series[0].data = data;
        var chart = new Highcharts.Chart(options);
    });

  


});


