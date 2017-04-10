function drawDynamicTable(reportID, idx, tblRenderTo, path_gene, categories, organism, is_barplot, is_metabolic){
	
	var arParams = idx.split("+");
	var inter_num = arParams[0];
    var regulation = arParams[1];
    var members = arParams[2];
    var is_metabolic = arParams[3];
    
    tblId = members.split(' ').join('_')
    tblId = tblId.replace(/\(/g, '').replace(/\)/g, '')
    tblId+=regulation
    tblId+=tblRenderTo
    tblId+=is_metabolic
    
    arMembers = members.split('vs');
    
    
    $('#'+tblRenderTo+' > div.dataTables_wrapper').fadeOut('fast');
    
    
	if (arParams[0]<5){
		if($( "#"+tblId ).length){ //check if required table already exists
			$("#"+tblId+"_wrapper").fadeIn();
		}
		else{
			if(is_metabolic=='true'){htmlTable = '<table id="'+tblId+'" class="path table table-striped table-bordered meta-dynamic" width="100%" >'}
			else {htmlTable = '<table id="'+tblId+'" class="path table table-striped table-bordered path-dynamic" width="100%" >'}
			
			htmlTable+='<thead><tr>';
			if(path_gene=='pathways') htmlTable+='<th>Pathway Name</th>';
			if(path_gene=='genes') htmlTable+='<th>Gene</th>';
			if(path_gene=='deeplearning') htmlTable+='<th>Gene</th><th>Probe</th>';
			
			
			arMembers.forEach(function(item, i, arr) {
				htmlTable+='<th>'+item+'</th>';
				if (reportID == 36 && path_gene=='pathways') htmlTable+='<th>'+item+' p-value</th>'; // for INSWX219 report
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
		        "scrollX": true,
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
		    		
		    		if ($(this).text().indexOf("...") >= 0) {
		    			//alert($(this).find('span').attr('long_name'));
		    			path_long_name = $(this).find('span').attr('long_name');
		    			$(this).text(path_long_name);
		    			
		    		}
		    		
		    		
		    		if(path_long_name.length > 50){
			    		var short_name = $.trim(path_long_name).substring(0, 50)
		                .trim(this) + "...";
			    		$(this).html("<span long_name='"+path_long_name+"'>"+short_name+"</span>");
			    	}
		    		else {
		    			$(this).html("<span long_name='"+path_long_name+"'>"+path_long_name+"</span>");
		    		}
		    	});
		   
		   if(path_gene == 'pathways'){
		    	$("table#"+tblId+".path tr td:nth-child(2)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+tblId+".path tr td:nth-child(3)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+tblId+".path tr td:nth-child(4)").wrapInner('<a href="#/"></a>');
	    	    $("table#"+tblId+".path tr td:nth-child(5)").wrapInner('<a href="#/"></a>');
		   }
		   else{
			   $("table#"+tblId+".path tr td:first-child()").wrapInner('<a href="#/"></a>');
		        } 
		   
			});
			
			if(path_gene == 'pathways'){
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(2)', function () {    	
	    	    var path_name = $(this).prev().find('span').attr('long_name');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, categories);    	    	
	                                                                              });
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(3)', function () {    	
	    	    var path_name = $(this).prev().prev().find('span').attr('long_name');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, categories);    	    	
	                                                                              });
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(4)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().find('span').attr('long_name');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, categories);    	    	
	                                                                              });
			$('#'+tblId+' tbody').on( 'click', 'tr td:nth-child(5)', function () {    	
	    	    var path_name = $(this).prev().prev().prev().prev().find('span').attr('long_name');    	
	    	    var $th = $(this).closest('table').find('th').eq($(this).index());
	    	    var group = $th.text();
	    	    showPathDetails(reportID, path_name, group, categories);    	    	
	                                                                              });
			
			} // end of if path_gene==paths
			else{
				
				$('#'+tblId+' tbody').on( 'click', 'tr td:first-child', function () {				    	
				    	var gene_name = $(this).text();	
				    	if (is_barplot) 	drawGeneBarPlot(reportID, gene_name, categories);    
				    	else drawGeneChart(reportID, gene_name, categories);
				    					    	
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
		                      is_metabolic, reg, tblRenderTo, path_gene, categories, organism, is_barplot){
	
	
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
                   
                   if(path_gene == 'deeplearning') tooltip.text(d.size + " genes");
                   else tooltip.text(d.size + " "+path_gene);
                   

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
                     
                     drawDynamicTable(reportID, idx, tblRenderTo, path_gene, categories, organism, is_barplot, is_metabolic);
                	 
                 });
			}
			);
	
}


function drawVennWithData(reportID, renderTo, tolltip, data, tblRenderTo){
	
	
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
           
           
           
           tooltip.text(d.size + " "+tolltip);
           

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
             
             
             drawSimpleTable(reportID, idx, tblRenderTo);
        	 
         });
	}
	

function drawSimpleTable(reportID, idx, tblRenderTo){
	tblId = 'tbl_'+idx;
	
	$('#'+tblRenderTo).empty();
	
	$('#'+tblRenderTo+' > div.dataTables_wrapper').fadeOut('fast');
	
	htmlTable = '<table id="'+tblId+'" class="path table table-striped table-bordered path-dynamic" width="100%" >';
	htmlTable+='<thead><tr><th>Tissue</th><th>Gene</th></tr></thead>';
	htmlTable+='</table>'
	
	$("#"+tblRenderTo).append(htmlTable);
	
	
	$('#'+tblId).DataTable( {
    	"paging":   true,
        "iDisplayLength": 20,
        "ordering": true,
        "order": [[ 0, "desc" ]],
        "info":     false,
        "scrollX": true,
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
        "ajax": {'url':'/report-portal/report-ajaxpathvenntbl-gsk/',
        	     'type': 'GET',
        	     'data':{
        	    	 reportID: reportID,
        	    	 group: idx
        	    	 
        	            }
        	    	 }
    } );

}

$(document).ready(function(){
	
});
