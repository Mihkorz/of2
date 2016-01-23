function drawGeneBoxplot(name, renderTo, gene){
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
            categories: ['NHK', 'RhE (Type1)', 'RhE (Type2)', 'RhE (Type3)'],
            title: {
                text: 'Skin type'
            }
        },

        yAxis: {
            title: {
                text: 'Expression'
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
        },
        {
            name: 'Observations1',
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
	
	$.getJSON('/report-portal/genesboxplotjson/',
    		{    	     
    	     gene: gene
    		},
    		function(data) { 
    	
    	options.series[0] = data[0];
    	options.series[1] = data[1];
        var chart = new Highcharts.Chart(options);
    });
}
$(function () {
	
	arGenes = ['COL1A1', 'COL1A2', 'KRT7', 'HYAL1', 'HYAL2', 'HYAL4', 'HAS1', 'HAS2',
	           'ELN', 'MMP1', 'MMP13', 'MMP8', 'FN1', 'WNT1', 'EGF', 'EGFR', 'GH1', 'TGFB1',
	           'TGFBR1', 'TGFBR2',
	           'FGF1', 'FGFR1']
	
	for (var i in arGenes) {
		
		  drawGeneBoxplot(name=arGenes[i]+' (NHE vs Case)', renderTo=arGenes[i], gene=arGenes[i]);
		  
		}
	

    
});