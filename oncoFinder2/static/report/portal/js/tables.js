
var paths_to_highlight = [
		'Akt_Signaling_Pathway_Elevation_of_Glucose_Import',
		'Akt_Signaling_Pathway_Glucose_Uptake',
		'Growth_Hormone_Signaling_Pathway_Glucose_Uptake',
		'IGF1R_Signaling_Pathway_Glucose_Uptake',
		'cAMP_Pathway_Fatty_Acid_Metabolism',
		'PPAR_Pathway_Fatty_Acid_Metabolism_Lipid_Homeostasis_and_Skin_Proliferation',
		'PPAR_Pathway_Peroxisome_Proliferation_Hepatocarcinogenesis_Fatty_Acid_Metbolism_and_Lipid_Homeostasis',
		'mTOR_Pathway_Lipid_Synthesis',
		'NGF_Pathway_Gene_Expression_via_MYC_ELK1_CREB3_NFKB2',
		'p38_Signaling_Pathway_Gene_Expression_Cell_Motility_Inflammation_Apoptosis_Osmoregulation_via_MEF2D_TP53_CREB1_ATF2_JUND_ETV1_NFKB2_AP2A1_MAX_FOSL1_CEBPG_ELK1_CDC25C_JUNB_STAT1_SP1_DDIT3_ELK4_CEBPA',
		'RANK_Signaling_in_Osteoclasts_Pathway_Expression_of_Osteoclastic_Genes_via_JUN_NFAT5_NFKB2_MITF_FOS',
		'TNF_Signaling_Pathway_Gene_Expression_and_Cell_Survival_via_FOS_NFKB2_JUN_ELK1_ATF6',
		'cAMP_Pathway_Gene_Expression_via_NFKB2_CREBBP_ELK1',
		'CD40_Pathway_Gene_Expression_Pro-Inflamatory_Cytokines_via_NFKB2',
		'CD40_Pathway_Gene_Expression_Procoagulant_Activity_via_NFKB2',
		'EGF_Pathway_Gene_Expression_via_FOS_NFKB2_MYC_STAT1_ELK1_STAT3_JUN',
		'ERK_Signaling_Pathway_Gene_Expression_via_CAPN6_TP53_FOS_ATF1_MYC_ELK3_MYLK_ETS1_SRF_HIST1H3B_CREB3_STAT3_NFKB2_HMGN1_ESR2_ELK1_PAX6_JUN',
		'Estrogen_Pathway_Gene_Expression_via_FOS_JUN_ELK1_SP1_POLR2B_CREB3_NFKB2',
		'GPCR_Pathway_Gene_Expression_via_JUN_NFKB2_ELK1_SRF_FOS_CREB3',
		'MAPK_Family_Pathway_Gene_Expression_via_ATF2_JUN_ELK1_NFKB2_CREB3',
		'Akt_Signaling_Pathway_NF-kB_dependent_transciption',
		'Akt_Signaling_Pathway_NF-kB_pathway',
		'Glucocorticoid_Receptor_Signaling_Pathway_Inflammatory_Cytokines',
		'IL-10_Pathway_Inflammatory_Cytokine_Genes_Expression_via_STAT3',
		'JNK_Pathway_Gene_Expression_Apoptosis_Inflammation_Tumorigenesis_Cell_Migration_via_SMAD4_STAT4_HSF1_TP53_MAP2_DCX_ATF2_NFATC3_SPIRE1_MAP1B_TCF15_ELK1_BCL2_JUN_PXN_NFATC2',
		'MAPK_Signaling_Pathway_Cell_Motility_Inflammation_Apoptosis_Osmoregulation',
		'MAPK_Signaling_Pathway_Gene_Expression_Apoptosis_Inflammation_Tumorigenesis_via_MYC_HSF1_STAT2',
		'mTOR_Pathway_Inflammation_Stress_Resistance'
	]

var paths_fatty_acid = [
	'cAMP_Pathway_Fatty_Acid_Metabolism',
	'PPAR_Pathway_Fatty_Acid_Metabolism_Lipid_Homeostasis_and_Skin_Proliferation',
	'PPAR_Pathway_Peroxisome_Proliferation_Hepatocarcinogenesis_Fatty_Acid_Metbolism_and_Lipid_Homeostasis',
	'mTOR_Pathway_Lipid_Synthesis'
]

var paths_glucose_uptake = [
	'Akt_Signaling_Pathway_Elevation_of_Glucose_Import',
	'Akt_Signaling_Pathway_Glucose_Uptake',
	'Growth_Hormone_Signaling_Pathway_Glucose_Uptake',
	'IGF1R_Signaling_Pathway_Glucose_Uptake'
]

var paths_inflamation = [
	'Glucocorticoid_Receptor_Signaling_Pathway_Inflammatory_Cytokines',
	'IL-10_Pathway_Inflammatory_Cytokine_Genes_Expression_via_STAT3',
	'JNK_Pathway_Gene_Expression_Apoptosis_Inflammation_Tumorigenesis_Cell_Migration_via_SMAD4_STAT4_HSF1_TP53_MAP2_DCX_ATF2_NFATC3_SPIRE1_MAP1B_TCF15_ELK1_BCL2_JUN_PXN_NFATC2',
	'MAPK_Signaling_Pathway_Cell_Motility_Inflammation_Apoptosis_Osmoregulation',
	'MAPK_Signaling_Pathway_Gene_Expression_Apoptosis_Inflammation_Tumorigenesis_via_MYC_HSF1_STAT2',
	'mTOR_Pathway_Inflammation_Stress_Resistance' 
]

var paths_nkkb = [
	'NGF_Pathway_Gene_Expression_via_MYC_ELK1_CREB3_NFKB2',
	'p38_Signaling_Pathway_Gene_Expression_Cell_Motility_Inflammation_Apoptosis_Osmoregulation_via_MEF2D_TP53_CREB1_ATF2_JUND_ETV1_NFKB2_AP2A1_MAX_FOSL1_CEBPG_ELK1_CDC25C_JUNB_STAT1_SP1_DDIT3_ELK4_CEBPA',
	'RANK_Signaling_in_Osteoclasts_Pathway_Expression_of_Osteoclastic_Genes_via_JUN_NFAT5_NFKB2_MITF_FOS',
	'TNF_Signaling_Pathway_Gene_Expression_and_Cell_Survival_via_FOS_NFKB2_JUN_ELK1_ATF6',
	'cAMP_Pathway_Gene_Expression_via_NFKB2_CREBBP_ELK1',
	'CD40_Pathway_Gene_Expression_Pro-Inflamatory_Cytokines_via_NFKB2',
	'CD40_Pathway_Gene_Expression_Procoagulant_Activity_via_NFKB2',
	'EGF_Pathway_Gene_Expression_via_FOS_NFKB2_MYC_STAT1_ELK1_STAT3_JUN',
	'ERK_Signaling_Pathway_Gene_Expression_via_CAPN6_TP53_FOS_ATF1_MYC_ELK3_MYLK_ETS1_SRF_HIST1H3B_CREB3_STAT3_NFKB2_HMGN1_ESR2_ELK1_PAX6_JUN',
	'Estrogen_Pathway_Gene_Expression_via_FOS_JUN_ELK1_SP1_POLR2B_CREB3_NFKB2',
	'GPCR_Pathway_Gene_Expression_via_JUN_NFKB2_ELK1_SRF_FOS_CREB3',
	'MAPK_Family_Pathway_Gene_Expression_via_ATF2_JUN_ELK1_NFKB2_CREB3',
	'Akt_Signaling_Pathway_NF-kB_dependent_transciption',
	'Akt_Signaling_Pathway_NF-kB_pathway' 
]


// BOX PLOT FOR GENES
	
	var options = {

        chart: {
            type: 'boxplot',
            renderTo: 'gene_plot',
            
        },

        title: {
            text: name
        },

        legend: {
            enabled: false
        },

        xAxis: {
            categories: ['ES', 'EPL', 'ASC', 'ABC', 'AEC', 'ANC' , 'CCL'],
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

	
function drawGeneChart(reportID, gene_name, categories){
		
		$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 80%; height: 400px; margin: 0 auto"></div>');
		
		$("#myModalLabel").text(gene_name);
		
		$('#pathmodal').modal('show');
		
		categories = categories.replace(/u&#39;/g, "");
		categories = categories.replace(/&#39;/g, "");
		categories = categories.replace('[', "");
		categories = categories.replace(']', "");
		
		$.getJSON('/report-portal/report-genesboxplotjson/',
				{
			     'reportID': reportID,
			     'gene': gene_name,
			     'categories': categories
			     },
			     function(data) {
			    	 
			    	$("#loading").empty();
			     	options.series[0] = data;
			     	options.title.text = gene_name;
			     	
			     	if (reportID == 4){
			     	  //if only one category for vulcano
			     	  lcategories = categories.split(',')
			     	  if (lcategories.length<2){
			     		  if(lcategories[0].indexOf('A549') !== -1) categories+=',DMSO_A549';
			     		  if(lcategories[0].indexOf('MCF7') !== -1) categories+=',DMSO_MCF7';
			     	  }
			     	  else{
			     		categories+=',DMSO_A549,DMSO_MCF7';
			     	  }
			     	
			       }
			     	
			     	options.xAxis.categories = categories.split(',');
			     	
			     	
			     	
			     	
			     	//if (reportID == 6){
			     		
			     		if (categories.split(',').length<=2) options.xAxis.categories = ['Case', 'Reference'];
			     		else {
			     			
			     			categories+=', Reference'; 
			     			options.xAxis.categories = categories.split(',');	
			     		}
			     		
			     	//}
			     		
			     		if ($.inArray(reportID, [35, 32, 31, 29])!== -1 ){ //For Novartis reports only!
				     		
				     		var cat = [];
				     		
				     		for(let c_name of categories.split(',')){
				     			c_arr = c_name.split('_');
				     			c_arr.splice(-1,1);
				     			c_name = c_arr.join('_');
				     			cat.push(c_name);
				     		}
				     		
				     		if (reportID == 29 || reportID == 31) {
				     			               cat.pop();
                                               cat.push('Norm'); //For Nasal and PBMC Reports
				     		}
				     		
				     		
				     		
				     		
				     		options.xAxis.categories = cat; //For Novartis reports only!
				     		
				     		if (categories.split(',').length<=2) options.xAxis.categories = ['Case', 'Reference']; // Duplicate for Novartis reports
				     		
				     		
				     	}
			     	
			        var chart = new Highcharts.Chart(options);
			        
			     }).fail(function( jqxhr, textStatus, error ) {
			    	    var err = textStatus + ", " + error;
			    	    console.log( "Request Failed: " + err );
			    	    
			    	    $("#loading").empty().text(err);
			    	    
			    	    
			    	});

	}

/////////////////////////// TEST FUNCTION FOR 2 SEPARATE WINDOWS
function drawGeneChartTest(reportID, gene_name, categories){
		
		$("#modalBodyGene").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 80%; height: 400px; margin: 0 auto"></div>');
		
		$("#myModalLabelGene").text(gene_name);
		
		$('#genemodal').modal('show');
		
		categories = categories.replace(/u&#39;/g, "");
		categories = categories.replace(/&#39;/g, "");
		categories = categories.replace('[', "");
		categories = categories.replace(']', "");
		
		$.getJSON('/report-portal/report-genesboxplotjson/',
				{
			     'reportID': reportID,
			     'gene': gene_name,
			     'categories': categories
			     },
			     function(data) {
			    	 
			    	$("#loading").empty();
			     	options.series[0] = data;
			     	options.title.text = gene_name;
			     	
			     	if (reportID == 4){
			     	  //if only one category for vulcano
			     	  lcategories = categories.split(',')
			     	  if (lcategories.length<2){
			     		  if(lcategories[0].indexOf('A549') !== -1) categories+=',DMSO_A549';
			     		  if(lcategories[0].indexOf('MCF7') !== -1) categories+=',DMSO_MCF7';
			     	  }
			     	  else{
			     		categories+=',DMSO_A549,DMSO_MCF7';
			     	  }
			     	
			       }
			     	
			     	options.xAxis.categories = categories.split(',');
			     	
			     	//if (reportID == 6){
			     		
			     		if (categories.split(',').length<=2) options.xAxis.categories = ['Case', 'Reference'];
			     		else {
			     			
			     			categories+=', Reference';
			     			options.xAxis.categories = categories.split(',');	
			     		}
			     		
			     	//}
			     	
			        var chart = new Highcharts.Chart(options);
			        
			     }).fail(function( jqxhr, textStatus, error ) {
			    	    var err = textStatus + ", " + error;
			    	    console.log( "Request Failed: " + err );
			    	    
			    	    $("#loading").empty().text(err);
			    	    
			    	    
			    	});

	}	
	
	
	
function showPathDetails(reportID, path_name, group_name, organism){
	$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="f" style="width: 800px; height: 400px; margin: 0 auto"></div>');
	
	$("#myModalLabel").text(path_name);
	
	$('#pathmodal').modal('show');
	//alert(path_name)
	$.get("/report-portal/report-ajaxpathdetail/",
			{
		     reportID: reportID,
		     pathway: path_name,
		     group_name: group_name,
		     organism: organism,
		     		
			},
			function(data){
				$("#modalBody").html(data);
			}
			);
}



function drawGeneTable(reportID, id, file_name, categories, is_barplot){
	
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
                   {extend: 'csv', title: file_name},
                   {extend: 'print', title: file_name}
                   
              ],
        
        "ajax": {'url':'/report-portal/report-genetablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	     reportID: reportID,
        	            'file_name': file_name,
        	            'categories': categories
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table#"+id+".path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	if (is_barplot) 	drawGeneBarPlot(reportID, gene_name, categories);    
    	else drawGeneChart(reportID, gene_name, categories); 
    	    	
    	
    });
}


//CHART FOR GENES
var bar_options = {
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
	        series: [{},
	                 {}]
	    }

	
function drawGeneBarPlot(reportID, gene_name, categories){
		$("#modalBody").html('<h4 id="loading">Loading ...</h4><div id="gene_plot" style="width: 500px; height: 400px; margin: 0 auto"></div>');
		
		$("#myModalLabel").text(gene_name);
		
		$('#pathmodal').modal('show');
		
		categories = categories.replace(/u&#39;/g, "");
		categories = categories.replace(/&#39;/g, "");
		categories = categories.replace('[', "");
		categories = categories.replace(']', "");
		
		var arr_categories = categories.split(',');
		
		var cat_case_name = arr_categories[0];
		var cat_norm_name = cat_case_name.replace('w', ''); 
				
		$.getJSON('/report-portal/report-genesbarplotjson/',
				{
			     'reportID': reportID,
			     'gene': gene_name,
			     'categories': categories
			     },
			     function(data){
						
						$("#loading").empty();
						
						bar_options.title.text = gene_name+' gene'
						bar_options.xAxis.categories = data['categories_name'];						
						
						
						bar_options.series[0].data = data["tumour"];
						bar_options.series[0].name = 'Poolw';
						
						bar_options.series[1].data = data["norm"];
						bar_options.series[1].name = 'Pool';
						
				        var chart = new Highcharts.Chart(bar_options);
					})

	}

function drawGeneTableScatter(reportID, id, file_name, categories, is_barplot){
	
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
                   {extend: 'csv', title: file_name},
                   {extend: 'print', title: file_name}
                   
              ],
        
        "ajax": {'url':'/report-portal/report-genetablescatterjson/',
        	     'type': 'GET',
        	     'data':{
        	    	     reportID: reportID,
        	            'file_name': file_name,
        	            'categories': categories
        	            },        	      
        
    },"deferRender": true });	
	
	
	table.buttons().container()
    .appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );
	
	$('#'+id).on( 'draw.dt', function () {
    	$("table#"+id+".path tr td:first-child").wrapInner('<a href="#/"></a>')
    } );
	
    $('#'+id+' tbody').on( 'click', 'tr td:first-child', function () {
    	
    	var gene_name = $(this).text();
    	
    	if (is_barplot) 	drawGeneBarPlot(reportID, gene_name, categories);    
    	else drawGeneChart(reportID, gene_name, categories);    
    	
    		
    	
    });
}

function drawPathwayTable(reportID, id, file_name1, file_name2, is_metabolic, organism){
	
	alert(file_name1)
	var table = $('#'+id).DataTable( {
    	"paging":   true,
    	"iDisplayLength": 20,
        "ordering": true,
        "order": [[ 1, "desc" ]],
        
        "info":     false,
        "autoWidth": false,
        "scrollX": false,
        "dom": 'Bfrtip',
        "buttons": [{extend: 'csv', title: id} , {extend: 'print', title: id}],
        
        "ajax": {'url':'/report-portal/report-pathwaytablejson/',
        	     'type': 'GET',
        	     'data':{
        	    	    'reportID': reportID,
        	            'file_name1': file_name1,
        	            'file_name2': file_name2,
        	            'is_metabolic': is_metabolic}
        	    	 }
    } );
	
	
	
	
	
	if(!is_metabolic){
	
		if(file_name1!='all' || file_name1!='tox'){
			
	
	    $('#'+id).on( 'draw.dt', function () {
	    	
	    	var path_name_td = $(table).find(" tr td:first-child()");
	    	path_name_td.each(function(){
	    		var path_long_name = $(this).text();
	    		
	    		if ($.inArray(path_long_name, paths_to_highlight)!== -1 && reportID==26){ /// inswx-report
	    			$(this).parent().addClass("success");
	    			//alert(path_long_name)
	    			
	    		}
	    		
	    		
	    		
	    		if(path_long_name.length > 50){
		    		var short_name = $.trim(path_long_name).substring(0, 50)
	                .trim(this) + "111";
		    		$(this).html("<span title='"+path_long_name+"' long_name='"+path_long_name+"'>"+short_name+"</span>");
		    	}
	    	});	    	
	    	
	    	$("table#"+id+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
    	    $("table#"+id+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>')
        } );
	    
        $('#'+id+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
    	    var path_name = $(this).prev().text();    	
    	    showPathDetails(reportID, path_name, file_name1);
    	   
    	
                                                                        });
        $('#'+id+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
    	    var path_name = $(this).prev().prev().text();    	
    	    showPathDetails(reportID, path_name, file_name2);
    	    
    	
                                                                        });
	    }
	    else {
		    $('#'+id).on( 'draw.dt', function () {
		    	
		    	var path_name_td = $("table#"+id+".path tr td:first-child()");
		    	//alert('draw')
		    	
		    	
		    	
		    	path_name_td.each(function(){
		    		var path_long_name = $(this).text();	    		
		    		
		    		/////////////////////////////// inswx-report
		    		if ($.inArray(path_long_name, paths_fatty_acid)!== -1 && reportID==36){ /// inswx-report
		    			$(this).parent().addClass("success");		    			
		    		}
		    		if ($.inArray(path_long_name, paths_glucose_uptake)!== -1 && reportID==36){ /// inswx-report
		    			$(this).parent().addClass("warning");		    			
		    		}
		    		if ($.inArray(path_long_name, paths_inflamation)!== -1 && reportID==36){ /// inswx-report
		    			$(this).parent().addClass("danger");		    			
		    		}
		    		if ($.inArray(path_long_name, paths_nkkb)!== -1 && reportID==36){ /// inswx-report
		    			$(this).parent().addClass("info");		    			
		    		}
                    /////////////////////////////// inswx-report
		    		
		    		
		    		
		    		if ($(this).text().indexOf("...") >= 0) {
		    			//alert($(this).find('span').attr('long_name'));
		    			path_long_name = $(this).find('span').attr('long_name');
		    			$(this).text(path_long_name);
		    			
		    		}
		    		
		    		if($(this).text().length > 50){
			    		var short_name = $.trim(path_long_name).substring(0, 50)
		                .trim(this) + "...";
			    		$(this).html("<span title='"+path_long_name+"' long_name='"+path_long_name+"'>"+short_name+"</span>");
			    	}
		    		else {
		    			//alert(path_long_name)
		    			$(this).html("<span title='"+path_long_name+"' long_name='"+path_long_name+"'>"+path_long_name+"</span>");
		    		}
		    		
		    		
		    		
		    		
		    	});	  
		    	
		    	row_num= $("table#"+id+" thead th").length;
		    	
		    	for (i=2; i<=row_num; i++){
		    		$("table#"+id+".path tr td:nth-child("+i+")").wrapInner('<a href="#/"></a>');
		    		
		    		$('#'+id+' tbody').on( 'click', 'tr td:nth-child('+i+')', function () {    	
			    	    var path_name = $(this).prevAll().find('span').attr('title');    	
			    	    var $th = $(this).closest('table').find('th').eq($(this).index());
			    	    var group = $th.text();
			    	    showPathDetails(reportID, path_name, group, organism);    	    	
			                                                                              });
		    		
		    	}
		    	
	    	  
	    	    
	        } );
		    
		    table.columns.adjust().draw();
		
	}
	
	} // end of is_metabolic
	else{
         $('#'+id).on( 'draw.dt', function () {
	    	
	    	var path_name_td = $("table#"+id+".path tr td:first-child()");
	    	path_name_td.each(function(){
	    		var path_long_name = $(this).text();
	    		if(path_long_name.length > 50){
		    		var short_name = $.trim(path_long_name).substring(0, 50)
	                .trim(this) + "...";
		    		$(this).html("<span title='"+path_long_name+"' long_name='"+path_long_name+"'>"+short_name+"</span>");
		    	}
	    	});	    	
    	    
	    	
        } );
	}
}




$(document).ready(function() {
	
/*	
	// GENES
	
	drawGeneTable('tbl-EPL_vs_ABC', 'EPL_vs_ABC.DE.tab');
	drawGeneTable('tbl-EPL_vs_AEC', 'EPL_vs_AEC.DE.tab');
	drawGeneTable('tbl-EPL_vs_ANC', 'EPL_vs_ANC.DE.tab');
	drawGeneTable('tbl-EPL_vs_ASC', 'EPL_vs_ASC.DE.tab');
	drawGeneTable('tbl-EPL_vs_CCL', 'EPL_vs_CCL.DE.tab');
	drawGeneTable('tbl-EPL_vs_ES', 'EPL_vs_ES.DE.tab');
	
	drawGeneTable('tbl-gene_all', 'all');
		
	
	
	
	// SIGNALING PATHS
	
	
    
    drawPathwayTable('tbl-path_all', 
			         'all', 
			         'all', false);
			     
    	
 // METABOLIC PATHS
	
	

    drawPathwayTable('tbl-meta_all', 
	         'all', 
	         'all', true);
	
	
 */   
} );


/*
function _render(jsonRes, templateRes, container) {
  var data = $.isArray(jsonRes) ? _.first(jsonRes) : jsonRes,
    templateString = _.first(templateRes),//.replace(/\s\s+/g, ''),
    compiled = _.template(templateString),
    compiledHtmlString = compiled(data);
  $(container).append( compiledHtmlString );
}false

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
