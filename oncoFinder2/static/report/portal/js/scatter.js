
function drawGeneScatter(name, renderTo, xname, yname, file_name){
	
var options = {
			
			chart: {
				  renderTo: renderTo,
			      type: 'scatter',
			      zoomType: 'xy',
			      marginBottom : 100
			    },
			    title: {
			      text: name,
			      y: 360
			    },
			    credits: false,
			    subtitle: {
			      text: ''
			    },
			    xAxis: {
			      title: {
			        enabled: true,
			        text: xname
			      },
			      startOnTick: true,
			      endOnTick: true,
			      showLastLabel: true
			    },
			    yAxis: {
			      title: {
			        text: yname
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
	
    $.getJSON('/report-portal/report-genescatterjson/',
    		{
    	     'file_name': file_name
    		},
    		function(data) { 
    	
    	options.series[0].data = data;
        var chart = new Highcharts.Chart(options);
    });
	
	
} 


function drawPathScatter(name, renderTo, xname, yname, file_name1, file_name2, is_metabolic){
	
	var options = {
				
				chart: {
					  renderTo: renderTo,
				      type: 'scatter',
				      zoomType: 'xy',
				      marginBottom : 100
				    },
				    title: {
				      text: name,
				      y: 360
				    },
				    credits: false,
				    subtitle: {
				      text: ''
				    },
				    xAxis: {
				      title: {
				        enabled: true,
				        text: xname
				      },
				      startOnTick: true,
				      endOnTick: true,
				      showLastLabel: true
				    },
				    yAxis: {
				      title: {
				        text: yname
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
		
	    $.getJSON('/report-portal/pathscatterjson/',
	    		{
	    	     'file_name1': file_name1,
	    	     'file_name2': file_name2,
	    	     'is_metabolic': is_metabolic
	    		},
	    		function(data) { 
	    	
	    	options.series[0].data = data;
	        var chart = new Highcharts.Chart(options);
	    });
		
		
	}

$(document).ready(function(){


	
    


});

