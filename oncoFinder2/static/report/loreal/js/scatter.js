
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
	
    $.getJSON('/report-portal/genescatterjson/',
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

	drawGeneScatter(name="L'Oreal_preprocessed_NHK. Case VS NHE",
			        renderTo='genes-nhk',
			        xname='log2(Case counts)', yname='log2(NHE counts)',
			        file_name='output_loreal_preprocessed_NHK.txt.xlsx')
    drawGeneScatter(name="L'Oreal_preprocessed_RhE (Type 1). Case VS NHE",
			        renderTo='genes-type1',
			        xname='log2(Case counts)', yname='log2(NHE counts)',
			        file_name='output_loreal_preprocessed_RhE (Type 1).txt.xlsx')
	drawGeneScatter(name="L'Oreal_preprocessed_RhE (Type 2). Case VS NHE",
			        renderTo='genes-type2',
			        xname='log2(Case counts)', yname='log2(NHE counts)',
			        file_name='output_loreal_preprocessed_RhE (Type 2).txt.xlsx')
	drawGeneScatter(name="L'Oreal_preprocessed_RhE (Type 3). Case VS NHE",
			        renderTo='genes-type3',
			        xname='log2(Case counts)', yname='log2(NHE counts)',
			        file_name='output_loreal_preprocessed_RhE (Type 3).txt.xlsx')
    
	// SIGNALING
	drawPathScatter(name="NHK VS Type1",
	        renderTo='path-nhk-type1',
	        xname='NHK', yname='Type1',
	        file_name1='output_loreal_preprocessed_NHK.txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 1).txt.xlsx', false)
	        
	drawPathScatter(name="NHK VS Type2",
	        renderTo='path-nhk-type2',
	        xname='NHK', yname='Type2',
	        file_name1='output_loreal_preprocessed_NHK.txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 2).txt.xlsx', false)
	
	drawPathScatter(name="NHK VS Type3",
	        renderTo='path-nhk-type3',
	        xname='NHK', yname='Type3',
	        file_name1='output_loreal_preprocessed_NHK.txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 3).txt.xlsx', false)
	
    drawPathScatter(name="Type1 VS Type2",
	        renderTo='path-type1-type2',
	        xname='Type1', yname='Type2',
	        file_name1='output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 2).txt.xlsx', false)
	        
	drawPathScatter(name="Type1 VS Type3",
	        renderTo='path-type1-type3',
	        xname='Type1', yname='Type3',
	        file_name1='output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 3).txt.xlsx', false)
	
	 drawPathScatter(name="Type2 VS Type3",
	        renderTo='path-type2-type3',
	        xname='Type2', yname='Type3',
	        file_name1='output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 3).txt.xlsx', false)
  

	// METABolIC
	drawPathScatter(name="NHK VS Type1",
	        renderTo='meta_path-nhk-type1',
	        xname='NHK', yname='Type1',
	        file_name1='output_loreal_preprocessed_NHK.txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 1).txt.xlsx', true)
	        
	drawPathScatter(name="NHK VS Type2",
	        renderTo='meta_path-nhk-type2',
	        xname='NHK', yname='Type2',
	        file_name1='output_loreal_preprocessed_NHK.txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 2).txt.xlsx', true)
	
	drawPathScatter(name="NHK VS Type3",
	        renderTo='meta_path-nhk-type3',
	        xname='NHK', yname='Type3',
	        file_name1='output_loreal_preprocessed_NHK.txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 3).txt.xlsx', true)
	
    drawPathScatter(name="Type1 VS Type2",
	        renderTo='meta_path-type1-type2',
	        xname='Type1', yname='Type2',
	        file_name1='output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 2).txt.xlsx', true)
	        
	drawPathScatter(name="Type1 VS Type3",
	        renderTo='meta_path-type1-type3',
	        xname='Type1', yname='Type3',
	        file_name1='output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 3).txt.xlsx', true)
	
	 drawPathScatter(name="Type2 VS Type3",
	        renderTo='meta_path-type2-type3',
	        xname='Type2', yname='Type3',
	        file_name1='output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
	        file_name2='output_loreal_preprocessed_RhE (Type 3).txt.xlsx', true)

});


