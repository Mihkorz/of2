// CHART FOR GENES
	
	var options = {
	        chart: {
	        	renderTo: 'gene_plot',
	            type: 'column'
	        },
	        title: {
	            text: 'MTOR gene'
	        },
	        xAxis: {
	        	type: 'category',
	        	labels: {
	        		rotation: -45,
	        	}
	            
	        },
	        yAxis: {
			      title: {
			        text: '# of counts'
			      }
			    },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: 'Unsorted',
	            color: 'grey',
	            
	        }, {
	            name: 'GFP-p62 low',
	            color: 'red',
	            
	        }, {
	            name: 'GFP-p62 high',
	            color: 'green',
	            
	        }]
	    }
	
function drawGeneChart(gene_name){
		$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 500px; height: 400px; margin: 0 auto"></div>');
    	
    	$("#myModalLabel").text(gene_name);
    	
    	$('#genemodal').modal('show');
    	
    	$.getJSON('/report-portal/demo/json/',
    			{'gene': gene_name},
    			function(data){
    				
    				$("#loading").empty();
    				
    				options.title.text = gene_name+' gene'
    				
    				options.series[0].data = data['Unsorted'];
    				options.series[1].data = data['Low'];
    				options.series[2].data = data['High'];
    		        var chart = new Highcharts.Chart(options);
    			})
	
}

$(document).ready(function() {
	
	
	
	
	// GENE TABLES
	
    $('#tbl-genes-undorted-low').DataTable( {
    	"paging":   false,
        "ordering": false,
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'res_unsorted_vs_low_genes'},
                   {extend: 'pdf', title: 'res_unsorted_vs_low_genes'},
                   {extend: 'print', title: 'res_unsorted_vs_low_genes'}
                   
              ],
        "ajax": '/static/report/demo/res_unsorted_vs_low_genes.json'
    } );
    
    $('#tbl-genes-undorted-low').on( 'draw.dt', function () {
    	$("table.genes tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
    
    $('#tbl-genes-undorted-low tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	drawGeneChart(gene_name);    	
    	
    });
    
    
    
    $('#tbl-genes-undorted-high').DataTable( {
    	"paging":   false,
        "ordering": false,
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'res_unsorted_vs_high_genes'},
                   {extend: 'pdf', title: 'res_unsorted_vs_high_genes'},
                   {extend: 'print', title: 'res_unsorted_vs_high_genes'}
                   
              ],
        "ajax": '/static/report/demo/res_unsorted_vs_high_genes.json'
    } );
    
    $('#tbl-genes-undorted-high').on( 'draw.dt', function () {
    	$("table.genes tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
    
    $('#tbl-genes-undorted-high tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	drawGeneChart(gene_name);    	
    	
    });
    
    $('#tbl-genes-low-high').DataTable( {
    	"paging":   false,
        "ordering": false,
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'res_low_vs_high_genes'},
                   {extend: 'pdf', title: 'res_low_vs_high_genes'},
                   {extend: 'print', title: 'res_low_vs_high_genes'}
                   
              ],
        "ajax": '/static/report/demo/res_low_vs_high_genes.json'
    } );
    
    $('#tbl-genes-low-high').on( 'draw.dt', function () {
    	$("table.genes tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
    
    $('#tbl-genes-low-high tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	drawGeneChart(gene_name);    	
    	
    });
    
    
    
    $('#tRNA-genes-low-high').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 3, "asc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'trna_charging_low_vs_high'},
                   {extend: 'pdf', title: 'trna_charging_low_vs_high'},
                   {extend: 'print', title: 'trna_charging_low_vs_high'}
                   
              ],
        "ajax": '/static/report/demo/trna_charging_low_vs_high.json'
    } );
    
    $('#tRNA-genes-low-high').on( 'draw.dt', function () {
    	$("table.genes tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
    
    $('#tRNA-genes-low-high tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	drawGeneChart(gene_name);    	
    	
    });
    
    
 // PATHWAY TABLES
    
    
    $('#tbl-signal-high-up').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 2, "desc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'signal_high_up'},
                   {extend: 'pdf', title: 'signal_high_up'},
                   {extend: 'print', title: 'signal_high_up'}
                   
              ],
        "ajax": '/static/report/demo/path/signal_high_up.json'
    } );
    
    $('#tbl-signal-high-down').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 2, "asc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'signal_high_down'},
                   {extend: 'pdf', title: 'signal_high_down'},
                   {extend: 'print', title: 'signal_high_down'}
                   
              ],
        "ajax": '/static/report/demo/path/signal_high_down.json'
    } );
    
    $('#tbl-signal-low-up').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'signal_low_up'},
                   {extend: 'pdf', title: 'signal_low_up'},
                   {extend: 'print', title: 'signal_low_up'}
                   
              ],
        "ajax": '/static/report/demo/path/signal_low_up.json'
    } );
    
    $('#tbl-signal-low-down').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 1, "asc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'signal_low_down'},
                   {extend: 'pdf', title: 'signal_low_down'},
                   {extend: 'print', title: 'signal_low_down'}
                   
              ],
        "ajax": '/static/report/demo/path/signal_low_down.json'
    } );
    
    // Metabolic
    
    $('#tbl-metabolic-high-up').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 2, "desc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'metabolic_high_up'},
                   {extend: 'pdf', title: 'metabolic_high_up'},
                   {extend: 'print', title: 'metabolic_high_up'}
                   
              ],
        "ajax": '/static/report/demo/path/metabolic_high_up.json'
    } );
    
    $('#tbl-metabolic-high-down').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 2, "asc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'metabolic_high_down'},
                   {extend: 'pdf', title: 'metabolic_high_down'},
                   {extend: 'print', title: 'metabolic_high_down'}
                   
              ],
        "ajax": '/static/report/demo/path/metabolic_high_down.json'
    } );
    
    $('#tbl-metabolic-low-up').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'metabolic_low_up'},
                   {extend: 'pdf', title: 'metabolic_low_up'},
                   {extend: 'print', title: 'metabolic_low_up'}
                   
              ],
        "ajax": '/static/report/demo/path/metabolic_low_up.json'
    } );
    
    $('#tbl-metabolic-low-down').DataTable( {
    	"paging":   false,
        "ordering": true,
        "order": [[ 1, "asc" ]],
        "info":     false,
        "bFilter": true,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: 'metabolic_low_down'},
                   {extend: 'pdf', title: 'metabolic_low_down'},
                   {extend: 'print', title: 'metabolic_low_down'}
                   
              ],
        "ajax": '/static/report/demo/path/metabolic_low_down.json'
    } );
    
} );


/*
function _render(jsonRes, templateRes, container) {
  var data = $.isArray(jsonRes) ? _.first(jsonRes) : jsonRes,
    templateString = _.first(templateRes),//.replace(/\s\s+/g, ''),
    compiled = _.template(templateString),
    compiledHtmlString = compiled(data);
  $(container).append( compiledHtmlString );
}

var names = {
  '.container5': ['metabolism_high_down', 'metabolism_high_up', 'metabolism_low_down', 'metabolism_low_up']
};

var titles = [''];



_.each(names, function(val, key){

  _.each(val, function(file){
    $.when(
      $.getJSON(file + '.json'),
      $.ajax('/js/tp/table.tp')
    ).done(function(data,tp){
        _render({lines: data[0]}, tp, key)
      })
  });


});

;*/
