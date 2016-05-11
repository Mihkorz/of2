function drawGeneBoxplot(name, renderTo, gene){
// BOX PLOT FOR GENES
	
	var options = {

        chart: {
            type: 'boxplot',
            renderTo: renderTo,
            
        },

        title: {
            text: name
        },

        legend: {
            enabled: false
        },

        xAxis: {
            categories: ['Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6' , 'Group7'],
            title: {
                text: 'Group'
            }
        },

        yAxis: {
            title: {
                text: 'Log2(Expression level)'
            },
            
        },

        series: [{
            name: 'Observations',
            data: [
                [760, 801, 848, 895, 965],
                [733, 853, 939, 980, 1080],
                [714, 762, 817, 870, 918],
                [724, 802, 806, 871, 950],
                [834, 836, 864, 882, 910]
            ],
            tooltip: {
                headerFormat: '<em>Experiment No {point.key}</em><br/>'
            }
        }]

    }
	
	$.getJSON('/report-portal/bt-genesboxplotjson/',
    		{    	     
    	     gene: gene
    		},
    		function(data) { 
    	
    	options.series[0] = data;
    	
        var chart = new Highcharts.Chart(options);
    });
}
$(function () {
	
	arEmbryonicGenes =[ 'PCDHB2', 'PCDHB17', 'CSTF3', 'LOC644919', 'ITGA11', 'SMA4',
                       'LOC727877', 'MAST2', 'TMEM18', 'LOC100130914', 'ADSSL1', 'ZNF767',
                       'C19orf25', 'C19orf6', 'NKTR', 'LOC286208', 'GOLGA8A', 'CDK5RAP3',
                       'OPN3', 'MGC16384', 'ZNF33A', 'LOC100190939', 'TPM1', 'GSDMB', 'NR3C1']
            
     arAdultGenes = ['COX7A1', 'ZNF280D', 'LOC441408', 'TRIM4', 'NIN', 'NAALADL1', 'ASF1B',
                    'COMT', 'CAT', 'C18orf56', 'LOC440731', 'HOXA5', 'LOC375295', 'POLQ',
                     'MEG3', 'CDT1', 'FOS']
	/*
	for (var i in arEmbryonicGenes) {
		
		  drawGeneBoxplot(name=arEmbryonicGenes[i], renderTo=arEmbryonicGenes[i], gene=arEmbryonicGenes[i]);
		  
		}
	
	for (var i in arAdultGenes) {
		
		  drawGeneBoxplot(name=arAdultGenes[i], renderTo=arAdultGenes[i], gene=arAdultGenes[i]);
		  
		}*/
	

    
});