function drawDinamicTable(idx, tblRenderTo, path_gene){
	
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
			if(path_gene=='MCF7') htmlTable+='<th>Pathway Name</th>';
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
		                 
		        "ajax": {'url':'/report-portal/report/gp-ajaxpathvenntbl/',
		        	     'type': 'GET',
		        	     'data':{
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
		   
		   if(path_gene == 'pathways' || path_gene == 'MCF7'){
		    	$("table#"+tblId+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+tblId+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+tblId+".path tr td:nth-child(4)").wrapInner('<a href="#/"></a>');
		   }
		   else{
			   $("table#"+tblId+".path tr td:first-child()").wrapInner('<a href="#/"></a>');
		        } 
		   
			});
			if(path_gene == 'pathways' || path_gene == 'MCF7'){
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
	    	    var path_name = $(this).prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
	    	    var path_name = $(this).prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(4)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().find('span').attr('title');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(path_name, group);    	    	
	                                                                              });
			} // end of if path_gene==paths
			else{
				
				$('#'+tblId+' tbody').on( 'click', 'tr td:first-child', function () {				    	
				    	var gene_name = $(this).text();				    	
				    	drawGeneChart(gene_name);				    	
				    });
				
			}
			
	        
		    }
	}
	else{
		$("#tbl-all").fadeIn();
	}
}


function drawVenn(renderTo, file_name1, name1,
		                      file_name2, name2,
		                      file_name3, name3,
		                      is_metabolic, reg, tblRenderTo, path_gene){
	$.get("/report-portal/report/gp-ajaxpathvenn/",
			{
		file_name1: file_name1,
		name1: name1,
		file_name2: file_name2,
		name2: name2,
		file_name3: file_name3,
		name3: name3,
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
                   if(path_gene == 'MCF7') { tooltip.text(d.size + " pathways");}
                   else{tooltip.text(d.size + " "+path_gene);}
                   

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
                     drawDinamicTable(idx, tblRenderTo, path_gene);
                	 
                 });
			}
			);
	
}

$(document).ready(function(){

	
	// SIGNALING
	
		drawVenn('venn_path-up',
			'output_drug_BRD-K59058747_perttime_6_dose_10um.txt.xlsx', 'N-acetylcysteine',
			'output_drug_BRD-K43149758_perttime_6_dose_10um.txt.xlsx', 'Myricetin',
			'output_drug_BRD-K55591206_perttime_6_dose_10um.txt.xlsx', 'Epigallocatechin gallate', 
			'path', 'up', 'venn_path_dinamic', 'pathways');
		drawVenn('venn_path-down',
				'output_drug_BRD-K59058747_perttime_6_dose_10um.txt.xlsx', 'N-acetylcysteine',
				'output_drug_BRD-K43149758_perttime_6_dose_10um.txt.xlsx', 'Myricetin',
				'output_drug_BRD-K55591206_perttime_6_dose_10um.txt.xlsx', 'Epigallocatechin gallate', 
				'path', 'down', 'venn_path_dinamic', 'pathways');
		
		
		drawVenn('MCF7_venn_path-up',
				'output_N-acetylcysteine.xlsx', 'N-acetylcysteine',
				'output_Myricetin.xlsx', 'Myricetin1',
				'output_Epigallocatechin gallate.xlsx', 'Epigallocatechin gallate', 
				'path', 'up', 'MCF7_venn_path_dinamic', 'MCF7');
		drawVenn('MCF7_venn_path-down',
					'output_N-acetylcysteine.xlsx', 'N-acetylcysteine',
					'output_Myricetin.xlsx', 'Myricetin',
					'output_Epigallocatechin gallate.xlsx', 'Epigallocatechin gallate', 
					'path', 'down', 'MCF7_venn_path_dinamic', 'MCF7');
		
		
		// METABOLIC
		
		drawVenn('venn_meta-up',
			'output_drug_BRD-K59058747_perttime_6_dose_10um.txt.xlsx', 'N-acetylcysteine',
			'output_drug_BRD-K43149758_perttime_6_dose_10um.txt.xlsx', 'Myricetin',
			'output_drug_BRD-K55591206_perttime_6_dose_10um.txt.xlsx', 'Epigallocatechin gallate', 
			'meta', 'up', 'venn_meta_dinamic', 'pathways');
		drawVenn('venn_meta-down',
				'output_drug_BRD-K59058747_perttime_6_dose_10um.txt.xlsx', 'N-acetylcysteine',
				'output_drug_BRD-K43149758_perttime_6_dose_10um.txt.xlsx', 'Myricetin',
				'output_drug_BRD-K55591206_perttime_6_dose_10um.txt.xlsx', 'Epigallocatechin gallate', 
				'meta', 'down', 'venn_meta_dinamic', 'pathways');
		
		drawVenn('meta_MCF7_venn_path-up',
				'output_N-acetylcysteine.xlsx', 'N-acetylcysteine',
				'output_Myricetin.xlsx', 'Myricetin',
				'output_Epigallocatechin gallate.xlsx', 'Epigallocatechin gallate', 
				'meta', 'up', 'MCF7_venn_meta_dinamic', 'MCF7');
		drawVenn('meta_MCF7_venn_path-down',
					'output_N-acetylcysteine.xlsx', 'N-acetylcysteine',
					'output_Myricetin.xlsx', 'Myricetin',
					'output_Epigallocatechin gallate.xlsx', 'Epigallocatechin gallate', 
					'meta', 'down', 'MCF7_venn_meta_dinamic', 'MCF7');
		
// Aging
		
		drawVenn('venn_age-up',
			'output_drug_BRD-K59058747_perttime_6_dose_10um.txt.xlsx', 'N-acetylcysteine',
			'output_drug_BRD-K43149758_perttime_6_dose_10um.txt.xlsx', 'Myricetin',
			'output_drug_BRD-K55591206_perttime_6_dose_10um.txt.xlsx', 'Epigallocatechin gallate', 
			'age', 'up', 'venn_meta_dinamic', 'pathways');
		drawVenn('venn_age-down',
				'output_drug_BRD-K59058747_perttime_6_dose_10um.txt.xlsx', 'N-acetylcysteine',
				'output_drug_BRD-K43149758_perttime_6_dose_10um.txt.xlsx', 'Myricetin',
				'output_drug_BRD-K55591206_perttime_6_dose_10um.txt.xlsx', 'Epigallocatechin gallate', 
				'age', 'down', 'venn_meta_dinamic', 'pathways');
		
		drawVenn('MCF7_venn_age-up',
				'output_N-acetylcysteine.xlsx', 'N-acetylcysteine',
				'output_Myricetin.xlsx', 'Myricetin',
				'output_Epigallocatechin gallate.xlsx', 'Epigallocatechin gallate', 
				'age', 'up', 'MCF7_venn_meta_dinamic', 'MCF7');
		drawVenn('MCF7_venn_age-down',
					'output_N-acetylcysteine.xlsx', 'N-acetylcysteine',
					'output_Myricetin.xlsx', 'Myricetin',
					'output_Epigallocatechin gallate.xlsx', 'Epigallocatechin gallate', 
					'age', 'down', 'MCF7_venn_meta_dinamic', 'MCF7');
		
		
		
	
	
});