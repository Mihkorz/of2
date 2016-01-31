
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
	
    $.getJSON('/report-portal/lrl-genescatterjson/',
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

    // Retinoic acid
	drawGeneScatter(name="Retinoic acid. 24h 0.1 micromol",
			        renderTo='ra_24_01_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_24h_01micromol_Retinoic_acid');
    drawGeneScatter(name="Retinoic acid. 24h 1 micromol",
			        renderTo='ra_24_1_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_24h_1micromol_Retinoic_acid');
	drawGeneScatter(name="Retinoic acid. 48h 0.1 micromol",
			        renderTo='ra_48_01_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_48h_01micromol_Retinoic_acid');
	drawGeneScatter(name="Retinoic acid. 48h 1 micromol",
			        renderTo='ra_48_1_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_48h_1micromol_Retinoic_acid');
			        
	//Metformin hydrochloride
	drawGeneScatter(name="Metformin hydrochloride. 24h 2 micromol",
			        renderTo='mh_24_2_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_24h_2millimol_Metformin_hydrochloride');
	drawGeneScatter(name="Metformin hydrochloride. 24h 4 micromol",
			        renderTo='mh_24_4_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_24h_4millimol_Metformin_hydrochloride');
	drawGeneScatter(name="Metformin hydrochloride. 48h 2 micromol",
			        renderTo='mh_48_2_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_48h_2millimol_Metformin_hydrochloride');
	drawGeneScatter(name="Metformin hydrochloride. 48h 4 micromol",
			        renderTo='mh_48_4_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_48h_4millimol_Metformin_hydrochloride');
	
	//Capryloylsalicylic acid
    drawGeneScatter(name="Capryloylsalicylic acid. 24h 5 micromol",
			        renderTo='ca_24_5_scatter',
			        xname='log2(Case expression level)', yname='log2(Norm expression level)',
			        file_name='Tumour_24h_5micromol_Capryloylsalicylic_acid');
    drawGeneScatter(name="Capryloylsalicylic acid. 24h 10 micromol",
	        renderTo='ca_24_10_scatter',
	        xname='log2(Case expression level)', yname='log2(Norm expression level)',
	        file_name='Tumour_24h_10micromol_Capryloylsalicylic_acid');
    drawGeneScatter(name="Capryloylsalicylic acid. 24h 5 micromol",
	        renderTo='ca_48_5_scatter',
	        xname='log2(Case expression level)', yname='log2(Norm expression level)',
	        file_name='Tumour_48h_5micromol_Capryloylsalicylic_acid');
    drawGeneScatter(name="Capryloylsalicylic acid. 24h 5 micromol",
	        renderTo='ca_48_10_scatter',
	        xname='log2(Case expression level)', yname='log2(Norm expression level)',
	        file_name='Tumour_48h_10micromol_Capryloylsalicylic_acid');
  //Resveratrol
    drawGeneScatter(name="Resveratrol. 24h 10 nmol",
	        renderTo='re_24_10_scatter',
	        xname='log2(Case expression level)', yname='log2(Norm expression level)',
	        file_name='Tumour_24h_10nmol_resveratrol');
    drawGeneScatter(name="Resveratrol. 24h 50 micromol",
	        renderTo='re_24_50_scatter',
	        xname='log2(Case expression level)', yname='log2(Norm expression level)',
	        file_name='Tumour_24h_50micromol_resveratrol');
    drawGeneScatter(name="Resveratrol. 48h 10 nmol",
	        renderTo='re_48_10_scatter',
	        xname='log2(Case expression level)', yname='log2(Norm expression level)',
	        file_name='Tumour_48h_10nmol_resveratrol');
    drawGeneScatter(name="Resveratrol. 48h 50 micromol",
	        renderTo='re_48_50_scatter',
	        xname='log2(Case expression level)', yname='log2(Norm expression level)',
	        file_name='Tumour_48h_50micromol_resveratrol');
    
});


