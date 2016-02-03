// CHART FOR PATH LINE
var	line_options = {
        chart: {
        	renderTo: 'gene_plot',
            type: 'line'
        },
        title: {
            text: 'Concentration- and time-dependent pathway changes'
        },
        xAxis: {
        	type: 'category',
        	categories: ['24h', '48h']        	
            
        },
        yAxis: {
		      title: {
		        text: 'PAS'
		      }
		    },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Normal',
            data: [1,4],
            
        }, {
            name: 'Case',
            data: [5,6],
            
        }, ]
    }
	
//CHART FOR GENES
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
			        text: 'log2(Expression level)'
			      }
			    },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: 'Normal',
	            color: 'grey',
	            
	        }, {
	            name: 'Case',
	            color: 'red',
	            
	        }, ]
	    }

	
function drawGeneChart(gene_name, file_name){
		$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 500px; height: 400px; margin: 0 auto"></div>');
		
		$("#myModalLabel").text(gene_name);
		
		$('#pathmodal').modal('show');
		
		$.getJSON('/report-portal/lrl-genedetailjson/',
				{
			     'gene': gene_name,
			     'file_name': file_name
			     },
			     function(data){
						
						$("#loading").empty();
						
						options.title.text = gene_name+' gene'
						
						options.series[0].data = data['NHE'];
						options.series[1].data = data['Case'];
						
				        var chart = new Highcharts.Chart(options);
					})

	}
	
function showPathDetails(path_name, filename){
	$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 800px; height: 400px; margin: 0 auto"></div>');
	
	$("#myModalLabel").text(path_name);
	
	$('#pathmodal').modal('show');
	
	$.get("/report-portal/report/lrl-ajaxpathdetail/",
			{
		     pathway: path_name,
		     filename: filename,
		     		
			},
			function(data){
				$("#modalBody").html(data);
			}
			);
}

function showPathLinePlot(path_name, renderTo){
	$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 500px; height: 400px; margin: 0 auto"></div>');
	
	$("#myModalLabel").text(path_name);
	
	$('#pathmodal').modal('show');
	
	$.getJSON('/report-portal/lrl-ajaxpathline/',
			{
		     'path': path_name,
		     'renderTo': renderTo
		     },
		     function(data){
					
					$("#loading").empty();
					
					options.title.text = path_name
					
					line_options.series[0] = data['s1'];
					line_options.series[1] = data['s2'];
					
			        var chart = new Highcharts.Chart(line_options);
				});

}

function drawGeneTable(id, file_name){
	
	// FIRST DOC
	var table = $('#'+id).DataTable( {
    	"paging":   true,
        "iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        "dom": 'Bfrtip',
        "buttons": [
                   {extend: 'csv', title: file_name},
                   {extend: 'print', title: file_name}
                   
              ],
        
        "ajax": {'url':'/report-portal/lrl-genetablejson/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': file_name,
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table#"+id+".path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	
    	drawGeneChart(gene_name, file_name);    	
    	
    });
}


function pathTable(renderTo, file_name){
	
	$('#'+renderTo).DataTable( {
    	"paging":   true,
    	"iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        
        "dom": 'Bfrtip',
        "buttons": [{extend: 'csv', title: renderTo}, {extend: 'pdf', title: renderTo} , {extend: 'print', title: renderTo}],
        
        "ajax": {'url':'/report-portal/lrl-pathwaytablejson/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': file_name
        	            }
        	    	 }
    } );
	
	$('#'+renderTo).on( 'draw.dt', function () {
    	
    	var path_name_td = $("table#"+renderTo+".path tr td:first-child()");
    	path_name_td.each(function(){
    		var path_long_name = $(this).text();
    		if(path_long_name.length > 70){
	    		var short_name = $.trim(path_long_name).substring(0, 70)
                .trim(this) + "...";
	    		$(this).html("<span title='"+path_long_name+"'>"+short_name+"</span>");
	    	}
    		else {
    			$(this).html("<span title='"+path_long_name+"'>"+path_long_name+"</span>");
    		}
    	});	  
    	
    	$("table#"+renderTo+".path tr td:first-child()").wrapInner('<a href="#/"></a>');
	    $("table#"+renderTo+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	   
    } );
	
	$('#'+renderTo+' tbody').on( 'click', 'tr td:first-child()', function () {    	
	    var path_name = $(this).find('span').attr('title');    	
	    
	    showPathLinePlot(path_name, renderTo);    	    	
                                                                          });
	
	$('#'+renderTo+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
	    var path_name = $(this).prev().find('span').attr('title');    	
	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    var group = $th.text();
	    showPathDetails(path_name, file_name);    	    	
                                                                          });
	
}

function drawPathwayTable(id, file_name1, file_name2, is_metabolic){
	
	
	$('#'+id).DataTable( {
    	"paging":   true,
    	"iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        
        "dom": 'Bfrtip',
        "buttons": [{extend: 'csv', title: id}, {extend: 'pdf', title: id} , {extend: 'print', title: id}],
        
        "ajax": {'url':'/report-portal/bt-pathwaytablejson/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name1': file_name1,
        	            'file_name2': file_name2,
        	            'is_metabolic': is_metabolic}
        	    	 }
    } );
	
	if(!is_metabolic){
	
		if(file_name1!='all'){
	
	    $('#'+id).on( 'draw.dt', function () {
	    	
	    	var path_name_td = $("table#"+id+".path tr td:first-child()");
	    	path_name_td.each(function(){
	    		var path_long_name = $(this).text();
	    		if(path_long_name.length > 70){
		    		var short_name = $.trim(path_long_name).substring(0, 70)
	                .trim(this) + "...";
		    		$(this).html("<span title='"+path_long_name+"'>"+short_name+"</span>");
		    	}
	    	});	    	
    	    
	    	$("table#"+id+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
    	    $("table#"+id+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>')
        } );
	
        $('#'+id+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
    	    var path_name = $(this).prev().text();    	
    	    showPathDetails(path_name, file_name1);    	
    	
                                                                        });
        $('#'+id+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
    	    var path_name = $(this).prev().prev().text();    	
    	    showPathDetails(path_name, file_name2);    	
    	
                                                                        });
	    }
	    else {
		    $('#'+id).on( 'draw.dt', function () {
		    	
		    	var path_name_td = $("table#"+id+".path tr td:first-child()");
		    	path_name_td.each(function(){
		    		var path_long_name = $(this).text();
		    		if(path_long_name.length > 70){
			    		var short_name = $.trim(path_long_name).substring(0, 70)
		                .trim(this) + "...";
			    		$(this).html("<span title='"+path_long_name+"'>"+short_name+"</span>");
			    	}
		    		else {
		    			$(this).html("<span title='"+path_long_name+"'>"+path_long_name+"</span>");
		    		}
		    	});	  
		    	
		    	
	    	    $("table#"+id+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(4)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(5)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(6)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+id+".path tr td:nth-child(7)").wrapInner('<a href="#/"></a>');
	        } );
		
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
	    	    var path_name = $(this).prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
	    	    var path_name = $(this).prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(4)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(5)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(6)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		    $('#'+id+' tbody').on( 'click', 'tr td:nth-child(7)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
		
	}
	
	} // end of is_metabolic
}

function sideTable(renderTo, file_name){
	
	$('#'+renderTo).DataTable( {
    	"paging":   true,
    	"iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        "info":     false,
        
        "dom": 'Bfrtip',
        "buttons": [{extend: 'csv', title: renderTo}, {extend: 'pdf', title: renderTo} , {extend: 'print', title: renderTo}],
        
        "ajax": {'url':'/report-portal/lrl-sideefftablejson/',
        	     'type': 'GET',
        	     'data':{
        	            'file_name': file_name
        	            }
        	    	 }
    } );
	
	$('#'+renderTo).on( 'draw.dt', function () {
    	
    	var path_name_td = $("table#"+renderTo+".path tr td:first-child()");
    	path_name_td.each(function(){
    		var path_long_name = $(this).text();
    		if(path_long_name.length > 70){
	    		var short_name = $.trim(path_long_name).substring(0, 70)
                .trim(this) + "...";
	    		$(this).html("<span title='"+path_long_name+"'>"+short_name+"</span>");
	    	}
    		else {
    			$(this).html("<span title='"+path_long_name+"'>"+path_long_name+"</span>");
    		}
    	});	  
    	
    	
	    //$("table#"+renderTo+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	   
    } );
	
}


$(document).ready(function() {
	
	
	// GENES
	
	drawGeneTable('tbl-ra_24_01', 'Tumour_24h_01micromol_Retinoic_acid');
	drawGeneTable('tbl-ra_24_1', 'Tumour_24h_1micromol_Retinoic_acid');
	drawGeneTable('tbl-ra_48_01', 'Tumour_48h_01micromol_Retinoic_acid');
	drawGeneTable('tbl-ra_48_1', 'Tumour_48h_1micromol_Retinoic_acid');
	
	drawGeneTable('tbl-mh_24_2', 'Tumour_24h_2millimol_Metformin_hydrochloride');
	drawGeneTable('tbl-mh_24_4', 'Tumour_24h_4millimol_Metformin_hydrochloride');
	drawGeneTable('tbl-mh_48_2', 'Tumour_48h_2millimol_Metformin_hydrochloride');
	drawGeneTable('tbl-mh_48_4', 'Tumour_48h_4millimol_Metformin_hydrochloride');
	
	drawGeneTable('tbl-ca_24_5', 'Tumour_24h_5micromol_Capryloylsalicylic_acid');
	drawGeneTable('tbl-ca_24_10', 'Tumour_24h_10micromol_Capryloylsalicylic_acid');
	drawGeneTable('tbl-ca_48_5', 'Tumour_48h_5micromol_Capryloylsalicylic_acid');
	drawGeneTable('tbl-ca_48_10', 'Tumour_48h_10micromol_Capryloylsalicylic_acid');
	
	drawGeneTable('tbl-re_24_10', 'Tumour_24h_10nmol_resveratrol');
	drawGeneTable('tbl-re_24_50', 'Tumour_24h_50micromol_resveratrol');	
	drawGeneTable('tbl-re_48_10', 'Tumour_48h_10nmol_resveratrol');	
	drawGeneTable('tbl-re_48_50', 'Tumour_48h_50micromol_resveratrol');	
	
	
	
	// SIGNALING PATHS
	
	pathTable('tbl-p-ra_24_01', 'output_Tumour_24h_01micromol_Retinoic_acid.xlsx'); //Cum ROR=13.5215
	pathTable('tbl-p-ra_24_1', 'output_Tumour_24h_1micromol_Retinoic_acid.xlsx');
	pathTable('tbl-p-ra_48_01', 'output_Tumour_48h_01micromol_Retinoic_acid.xlsx');
	pathTable('tbl-p-ra_48_1', 'output_Tumour_48h_1micromol_Retinoic_acid.xlsx');
	
	pathTable('tbl-p-mh_24_2', 'output_Tumour_24h_2millimol_Metformin_hydrochloride.xlsx'); //Cum ROR=11.5703
	pathTable('tbl-p-mh_24_4', 'output_Tumour_24h_4millimol_Metformin_hydrochloride.xlsx');
	pathTable('tbl-p-mh_48_2', 'output_Tumour_48h_2millimol_Metformin_hydrochloride.xlsx');
	pathTable('tbl-p-mh_48_4', 'output_Tumour_48h_4millimol_Metformin_hydrochloride.xlsx');
	
	pathTable('tbl-p-ca_24_5', 'output_Tumour_24h_5micromol_Capryloylsalicylic_acid.xlsx'); //Cum ROR=13.5215
	pathTable('tbl-p-ca_24_10', 'output_Tumour_24h_10micromol_Capryloylsalicylic_acid.xlsx');
	pathTable('tbl-p-ca_48_5', 'output_Tumour_48h_5micromol_Capryloylsalicylic_acid.xlsx');
	pathTable('tbl-p-ca_48_10', 'output_Tumour_48h_10micromol_Capryloylsalicylic_acid.xlsx');
	
	pathTable('tbl-p-re_24_10', 'output_Tumour_24h_10nmol_resveratrol.xlsx'); //Cum ROR=8.7583
	pathTable('tbl-p-re_24_50', 'output_Tumour_24h_50micromol_resveratrol.xlsx');	
	pathTable('tbl-p-re_48_10', 'output_Tumour_48h_10nmol_resveratrol.xlsx');	
	pathTable('tbl-p-re_48_50', 'output_Tumour_48h_50micromol_resveratrol.xlsx');	
	
	
	
	// Side Effects
	
	sideTable('tbl-s-ra', 'Retinoic acid_side_effects.csv');
	sideTable('tbl-s-mh', 'metformin_side_effects.csv');
	sideTable('tbl-s-ca', 'salycilic_acid_adverse.csv');
	sideTable('tbl-s-re', 'Resveratrol_side_effects.csv');
	
 // Geroprotectors table colorising

	function roundToTwo(num) {    
	    return +(Math.round(num + "e+2")  + "e-2");
	}
	
	$('#tbl-gero > tbody  > tr').each(function() {
		
		var td = $(this).find("td").each(function(){
			var value = parseFloat($(this).text());
			if(value!=24 && value!=48){
			if(value>0) {
				
				$(this).text(roundToTwo(value));
				$(this).addClass('success');}
			if(value<0) {
				$(this).text(roundToTwo(value));
				$(this).addClass('danger');}
			}
		});
		
	});
      

	 $('#tbl-sim_ra').DataTable( {
		 "paging":   true,
	    	"iDisplayLength": 20,
	        "ordering": true,
	        "order": [[ 1, "desc" ]],
	        "info":     false,
	        
	        "dom": 'Bfrtip',
	        "buttons": [{extend: 'csv', title: 'RA_sim'}, {extend: 'pdf', title: 'RA_sim'} , {extend: 'print', title: 'RA_sim'}],
	        
	        "ajax": '/static/report/lrl2016/RA_sim.json'
	    } );
	 $('#tbl-sim_mh').DataTable( {
		 "paging":   true,
	    	"iDisplayLength": 20,
	        "ordering": true,
	        "order": [[ 1, "desc" ]],
	        "info":     false,
	        
	        "dom": 'Bfrtip',
	        "buttons": [{extend: 'csv', title: 'Sim_Metformin'}, {extend: 'pdf', title: 'Sim_Metformin'} , {extend: 'print', title: 'Sim_Metformin'}],
	        
	        "ajax": '/static/report/lrl2016/Sim_Metformin.json'
	    } );
	 $('#tbl-sim_ca').DataTable( {
		 "paging":   true,
	    	"iDisplayLength": 20,
	        "ordering": true,
	        "order": [[ 1, "desc" ]],
	        "info":     false,
	        
	        "dom": 'Bfrtip',
	        "buttons": [{extend: 'csv', title: 'Sim_Capro'}, {extend: 'pdf', title: 'Sim_Capro'} , {extend: 'print', title: 'Sim_Capro'}],
	        
	        "ajax": '/static/report/lrl2016/Sim_Capro.json'
	    } );
	 $('#tbl-sim_re').DataTable( {
		 "paging":   true,
	    	"iDisplayLength": 20,
	        "ordering": true,
	        "order": [[ 1, "desc" ]],
	        "info":     false,
	        
	        "dom": 'Bfrtip',
	        "buttons": [{extend: 'csv', title: 'sim_Resve'}, {extend: 'pdf', title: 'sim_Resve'} , {extend: 'print', title: 'sim_Resve'}],
	        
	        "ajax": '/static/report/lrl2016/sim_Resve.json'
	    } );
	 
	 $('#tbl-sim_ra').on( 'draw.dt', function () {
		 $('#tbl-sim_ra > tbody  > tr').each(function() {
				
				var td = $(this).find("td").each(function(){
					var value = parseFloat($(this).text());
					if(value!=24 && value!=48){
					if(value>0) {
						
						$(this).text(roundToTwo(value));
						$(this).addClass('success');}
					if(value<0) {
						$(this).text(roundToTwo(value));
						$(this).addClass('danger');}
					}
				});
				
			});
		 
	 });
	 $('#tbl-sim_mh').on( 'draw.dt', function () {
		 $('#tbl-sim_mh > tbody  > tr').each(function() {
				
				var td = $(this).find("td").each(function(){
					var value = parseFloat($(this).text());
					if(value!=24 && value!=48){
					if(value>0) {
						
						$(this).text(roundToTwo(value));
						$(this).addClass('success');}
					if(value<0) {
						$(this).text(roundToTwo(value));
						$(this).addClass('danger');}
					}
				});
				
			});
	 });
	 $('#tbl-sim_ca').on( 'draw.dt', function () {
		 $('#tbl-sim_ca > tbody  > tr').each(function() {
				
				var td = $(this).find("td").each(function(){
					var value = parseFloat($(this).text());
					if(value!=24 && value!=48){
					if(value>0) {
						
						$(this).text(roundToTwo(value));
						$(this).addClass('success');}
					if(value<0) {
						$(this).text(roundToTwo(value));
						$(this).addClass('danger');}
					}
				});
				
			});
	 });
	 $('#tbl-sim_re').on( 'draw.dt', function () {
		 $('#tbl-sim_re > tbody  > tr').each(function() {
				
				var td = $(this).find("td").each(function(){
					var value = parseFloat($(this).text());
					if(value!=24 && value!=48){
					if(value>0) {
						
						$(this).text(roundToTwo(value));
						$(this).addClass('success');}
					if(value<0) {
						$(this).text(roundToTwo(value));
						$(this).addClass('danger');}
					}
				});
				
			});
	 });
	 
	 
    
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
