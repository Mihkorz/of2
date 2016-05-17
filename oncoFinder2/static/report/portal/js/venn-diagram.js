function drawDinamicTable(reportID, idx, tblRenderTo, path_gene, categories, organism){
	
	var arParams = idx.split("_");
	var inter_num = arParams[0];
    var regulation = arParams[1];
    var members = arParams[2];
    var is_metabolic = arParams[3];
	
    tblId = members.split(' ').join('_')
    tblId = tblId.replace(/\(/g, '').replace(/\)/g, '')
    tblId+=regulation
    tblId+=tblRenderTo
    
    arMembers = members.split('vs');
    
    
    $('#'+tblRenderTo+' > div.dataTables_wrapper').fadeOut('fast');
    
    
	if (arParams[0]<4){
		if($( "#"+tblId ).length){ //check if required table already exists
			$("#"+tblId+"_wrapper").fadeIn();
		}
		else{
			if(is_metabolic=='true'){htmlTable = '<table id="'+tblId+'" class="path table table-striped table-bordered meta-dinamic" width="100%" >'}
			else {htmlTable = '<table id="'+tblId+'" class="path table table-striped table-bordered path-dinamic" width="100%" >'}
			
			htmlTable+='<thead><tr>';
			if(path_gene=='pathways') htmlTable+='<th>Pathway Name</th>';
			if(path_gene=='genes') htmlTable+='<th>Gene</th>';
			
			
			arMembers.forEach(function(item, i, arr) {
				htmlTable+='<th>'+item+'</th>';
			});
			
			htmlTable+='</tr></thead>';
			htmlTable+='</table>';			
			
			$("#"+tblRenderTo).append(htmlTable);			    
			
			
			$('#'+tblId).DataTable( {
		    	"paging":   true,
		        "iDisplayLength": 20,
		        "ordering": true,
		        "order": [[ 1, "desc" ]],
		        "info":     false,
		        
		        "dom": 'Bfrtip',
		        "buttons": [
		                  {extend: 'csv',
		                   exportOptions: {
		                            columns: ':visible'
		                        },
		                  title: tblId},
		                  
		                  {extend: 'pdf',
		                  title: tblId},
		                  {extend: 'print',
			                  title: tblId},
		                 
		                 ],
		        "ajax": {'url':'/report-portal/report-ajaxpathvenntbl/',
		        	     'type': 'GET',
		        	     'data':{
		        	    	 reportID: reportID,
		        	    	 inter_num: inter_num,
		    		         regulation: regulation,
		    		         members: members,
		    		         is_metabolic: is_metabolic,
		    		         path_gene: path_gene
		        	            }
		        	    	 }
		    } );
			
			$('#'+tblId).on( 'draw.dt', function () {
				var path_name_td = $("table#"+tblId+".path tr td:first-child()");
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
		   
		   if(path_gene == 'pathways'){
		    	$("table#"+tblId+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+tblId+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+tblId+".path tr td:nth-child(4)").wrapInner('<a href="#/"></a>');
		   }
		   else{
			   $("table#"+tblId+".path tr td:first-child()").wrapInner('<a href="#/"></a>');
		        } 
		   
			});
			if(path_gene == 'pathways'){
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
	    	    var path_name = $(this).prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, categories);    	    	
	                                                                              });
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
	    	    var path_name = $(this).prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, categories);    	    	
	                                                                              });
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(4)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, categories);    	    	
	                                                                              });
			} // end of if path_gene==paths
			else{
				
				$('#'+tblId+' tbody').on( 'click', 'tr td:first-child', function () {				    	
				    	var gene_name = $(this).text();				    	
				    	drawGeneChart(reportID, gene_name, categories);				    	
				    });
				
			}
			
	        
		    }
	}
	else{
		$("#tbl-all").fadeIn();
	}
}


function drawVenn(reportID, renderTo, 
		                      group_names,		                      
		                      is_metabolic, reg, tblRenderTo, path_gene, categories, organism){
	
	alert(categories)
	$.get("/report-portal/report-ajaxpathvenn/",
			{
		reportID: reportID,
		group_names: group_names,
		is_metabolic: is_metabolic,
		regulation: reg,
		path_gene: path_gene
			},
			function(data){
				var sets = data;
				
				$("#"+renderTo).empty();
    
                var div = d3.select("#"+renderTo);
                div.datum(sets).call(venn.VennDiagram()
                		                              .width(400)
                                                      .height(400));
                
             // add a tooltip          
                var tooltip = d3.select("body").append("div").attr("class", "venntooltip");
                div.selectAll("path")
                .style("stroke-opacity", 0)
                .style("stroke", "#fff")
                .style("stroke-width", 0);
             // add listeners to all the groups to display tooltip on mousover
             div.selectAll("g")
                 .on("mouseover", function(d, i) {
                   // sort all the areas relative to the current item
                   venn.sortAreas(div, d);

                   // Display a tooltip with the current size
                   tooltip.transition().duration(400).style("opacity", .9);
                   tooltip.text(d.size + " "+path_gene);
                   

                   // highlight the current path
                   var selection = d3.select(this).transition("tooltip").duration(400);
                   selection.select("path")
                                          .style("stroke-width", 3)
                                          .style("fill-opacity", d.sets.length == 1 ? .4 : .1)
                                          .style("stroke-opacity", 1);
                                                  })
                 .on("mousemove", function() {
                                  tooltip.style("left", (d3.event.pageX) + "px")
                                         .style("top", (d3.event.pageY - 28) + "px");
                                              })
                 .on("mouseout", function(d, i) {
                      tooltip.transition().duration(400).style("opacity", 0);
                      var selection = d3.select(this).transition("tooltip").duration(400);
                      selection.select("path")
                               .style("stroke-width", 0)
                               .style("fill-opacity", d.sets.length == 1 ? .25 : .0)
                               .style("stroke-opacity", 0);
                                                 })
                 .on("click", function(d, i){
                	
                	 venn.sortAreas(div, d);
                     var idx = d.id;
                     drawDinamicTable(reportID, idx, tblRenderTo, path_gene, categories);
                	 
                 });
			}
			);
	
}

$(document).ready(function(){
	/*
	// GENES
	drawVenn('venn_gene-ESvsASCvsCCL-up',
			'EPL_vs_ES.DE.tab', 'ES',
			'EPL_vs_ASC.DE.tab', 'ASC',
			'EPL_vs_CCL.DE.tab', 'CCL', 
			false, 'up', 'venn_gene_dinamic_ESvsASCvsCCL', 'genes');
		drawVenn('venn_gene-ESvsASCvsCCL-down',
				'EPL_vs_ES.DE.tab', 'ES',
				'EPL_vs_ASC.DE.tab', 'ASC',
				'EPL_vs_CCL.DE.tab', 'CCL', 
				false, 'down', 'venn_gene_dinamic_ESvsASCvsCCL', 'genes');
		
		drawVenn('venn_gene-ESvsANCvsCCL-up',
				'EPL_vs_ES.DE.tab', 'ES',
				'EPL_vs_ANC.DE.tab', 'ANC',
				'EPL_vs_CCL.DE.tab', 'CCL', 
				false, 'up', 'venn_gene_dinamic_ESvsANCvsCCL', 'genes');
		drawVenn('venn_gene-ESvsANCvsCCL-down',
					'EPL_vs_ES.DE.tab', 'ES',
					'EPL_vs_ANC.DE.tab', 'ANC',
					'EPL_vs_CCL.DE.tab', 'CCL', 
					false, 'down', 'venn_gene_dinamic_ESvsANCvsCCL', 'genes');
		
		drawVenn('venn_gene-ESvsAECvsCCL-up',
				'EPL_vs_ES.DE.tab', 'ES',
				'EPL_vs_AEC.DE.tab', 'AEC',
				'EPL_vs_CCL.DE.tab', 'CCL', 
				false, 'up', 'venn_gene_dinamic_ESvsAECvsCCL', 'genes');
		drawVenn('venn_gene-ESvsAECvsCCL-down',
					'EPL_vs_ES.DE.tab', 'ES',
					'EPL_vs_AEC.DE.tab', 'AEC',
					'EPL_vs_CCL.DE.tab', 'CCL', 
					false, 'down', 'venn_gene_dinamic_ESvsAECvsCCL', 'genes');
			
		drawVenn('venn_gene-ESvsABCvsCCL-up',
					'EPL_vs_ES.DE.tab', 'ES',
					'EPL_vs_ABC.DE.tab', 'ABC',
					'EPL_vs_CCL.DE.tab', 'CCL', 
					false, 'up', 'venn_gene_dinamic_ESvsABCvsCCL', 'genes');
		drawVenn('venn_gene-ESvsABCvsCCL-down',
						'EPL_vs_ES.DE.tab', 'ES',
						'EPL_vs_ABC.DE.tab', 'ABC',
						'EPL_vs_CCL.DE.tab', 'CCL', 
						false, 'down', 'venn_gene_dinamic_ESvsABCvsCCL', 'genes');
	
	// SIGNALING
	
		drawVenn('venn_path-ESvsASCvsCCL-up',
			'pros_output_EPL_vs_ES.csv', 'ES',
			'pros_output_EPL_vs_ASC.csv', 'ASC',
			'pros_output_EPL_vs_CCL.csv', 'CCL', 
			false, 'up', 'venn_path_dinamic_ESvsASCvsCCL', 'pathways');
		drawVenn('venn_path-ESvsASCvsCCL-down',
				'pros_output_EPL_vs_ES.csv', 'ES',
				'pros_output_EPL_vs_ASC.csv', 'ASC',
				'pros_output_EPL_vs_CCL.csv', 'CCL', 
				false, 'down', 'venn_path_dinamic_ESvsASCvsCCL', 'pathways');
		
		drawVenn('venn_path-ESvsANCvsCCL-up',
				'pros_output_EPL_vs_ES.csv', 'ES',
				'pros_output_EPL_vs_ANC.csv', 'ANC',
				'pros_output_EPL_vs_CCL.csv', 'CCL', 
				false, 'up', 'venn_path_dinamic_ESvsANCvsCCL', 'pathways');
		drawVenn('venn_path-ESvsANCvsCCL-down',
					'pros_output_EPL_vs_ES.csv', 'ES',
					'pros_output_EPL_vs_ANC.csv', 'ANC',
					'pros_output_EPL_vs_CCL.csv', 'CCL', 
					false, 'down', 'venn_path_dinamic_ESvsANCvsCCL', 'pathways');
		
		drawVenn('venn_path-ESvsAECvsCCL-up',
				'pros_output_EPL_vs_ES.csv', 'ES',
				'pros_output_EPL_vs_AEC.csv', 'AEC',
				'pros_output_EPL_vs_CCL.csv', 'CCL', 
				false, 'up', 'venn_path_dinamic_ESvsAECvsCCL', 'pathways');
		drawVenn('venn_path-ESvsAECvsCCL-down',
					'pros_output_EPL_vs_ES.csv', 'ES',
					'pros_output_EPL_vs_AEC.csv', 'AEC',
					'pros_output_EPL_vs_CCL.csv', 'CCL', 
					false, 'down', 'venn_path_dinamic_ESvsAECvsCCL', 'pathways');
			
		drawVenn('venn_path-ESvsABCvsCCL-up',
					'pros_output_EPL_vs_ES.csv', 'ES',
					'pros_output_EPL_vs_ABC.csv', 'ABC',
					'pros_output_EPL_vs_CCL.csv', 'CCL', 
					false, 'up', 'venn_path_dinamic_ESvsABCvsCCL', 'pathways');
		drawVenn('venn_path-ESvsABCvsCCL-down',
						'pros_output_EPL_vs_ES.csv', 'ES',
						'pros_output_EPL_vs_ABC.csv', 'ABC',
						'pros_output_EPL_vs_CCL.csv', 'CCL', 
						false, 'down', 'venn_path_dinamic_ESvsABCvsCCL', 'pathways');
		
		// METABOLIC
		
		drawVenn('meta_venn_path-ESvsASCvsCCL-up',
			'pros_output_EPL_vs_ES.csv', 'ES',
			'pros_output_EPL_vs_ASC.csv', 'ASC',
			'pros_output_EPL_vs_CCL.csv', 'CCL', 
			true, 'up', 'meta_venn_path_dinamic_ESvsASCvsCCL', 'pathways');
		drawVenn('meta_venn_path-ESvsASCvsCCL-down',
				'pros_output_EPL_vs_ES.csv', 'ES',
				'pros_output_EPL_vs_ASC.csv', 'ASC',
				'pros_output_EPL_vs_CCL.csv', 'CCL', 
				true, 'down', 'meta_venn_path_dinamic_ESvsASCvsCCL', 'pathways');
		
		drawVenn('meta_venn_path-ESvsANCvsCCL-up',
				'pros_output_EPL_vs_ES.csv', 'ES',
				'pros_output_EPL_vs_ANC.csv', 'ANC',
				'pros_output_EPL_vs_CCL.csv', 'CCL', 
				true, 'up', 'meta_venn_path_dinamic_ESvsANCvsCCL', 'pathways');
		drawVenn('meta_venn_path-ESvsANCvsCCL-down',
					'pros_output_EPL_vs_ES.csv', 'ES',
					'pros_output_EPL_vs_ANC.csv', 'ANC',
					'pros_output_EPL_vs_CCL.csv', 'CCL', 
					true, 'down', 'meta_venn_path_dinamic_ESvsANCvsCCL', 'pathways');
		
		drawVenn('meta_venn_path-ESvsAECvsCCL-up',
				'pros_output_EPL_vs_ES.csv', 'ES',
				'pros_output_EPL_vs_AEC.csv', 'AEC',
				'pros_output_EPL_vs_CCL.csv', 'CCL', 
				true, 'up', 'venn_path_dinamic_ESvsAECvsCCL', 'pathways');
		drawVenn('venn_path-ESvsAECvsCCL-down',
					'pros_output_EPL_vs_ES.csv', 'ES',
					'pros_output_EPL_vs_AEC.csv', 'AEC',
					'pros_output_EPL_vs_CCL.csv', 'CCL', 
					true, 'down', 'meta_venn_path_dinamic_ESvsAECvsCCL', 'pathways');
			
		drawVenn('meta_venn_path-ESvsABCvsCCL-up',
					'pros_output_EPL_vs_ES.csv', 'ES',
					'pros_output_EPL_vs_ABC.csv', 'ABC',
					'pros_output_EPL_vs_CCL.csv', 'CCL', 
					true, 'up', 'meta_venn_path_dinamic_ESvsABCvsCCL', 'pathways');
		drawVenn('meta_venn_path-ESvsABCvsCCL-down',
						'pros_output_EPL_vs_ES.csv', 'ES',
						'pros_output_EPL_vs_ABC.csv', 'ABC',
						'pros_output_EPL_vs_CCL.csv', 'CCL', 
						true, 'down', 'meta_venn_path_dinamic_ESvsABCvsCCL', 'pathways');
*/	
});