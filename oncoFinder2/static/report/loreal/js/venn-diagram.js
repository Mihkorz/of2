function drawDynamicTable(idx){
	
	var arParams = idx.split("_");
	var inter_num = arParams[0];
    var regulation = arParams[1];
    var members = arParams[2];
    var is_metabolic = arParams[3];
	
    tblId = members.split(' ').join('_')
    tblId = tblId.replace(/\(/g, '').replace(/\)/g, '')
    tblId+=regulation
    
    arMembers = members.split('vs');
    
    if(is_metabolic=='true'){$('#venn_meta_dynamic > div.dataTables_wrapper').fadeOut('fast');}
    else{$('#venn_path_dynamic > div.dataTables_wrapper').fadeOut('fast');}
    
    
	if (arParams[0]<4){
		if($( "#"+tblId ).length){ //check if required table already exists
			$("#"+tblId+"_wrapper").fadeIn();
		}
		else{
			if(is_metabolic=='true'){htmlTable = '<table id="'+tblId+'" class="path table table-striped table-bordered meta-dynamic" width="100%" >'}
			else {htmlTable = '<table id="'+tblId+'" class="path table table-striped table-bordered path-dynamic" width="100%" >'}
			
			htmlTable+='<thead><tr>';
			htmlTable+='<th>Pathway Name</th>';
			
			arMembers.forEach(function(item, i, arr) {
				htmlTable+='<th>'+item+'</th>';
			});
			
			htmlTable+='</tr></thead>';
			htmlTable+='</table>';			
			
			if(is_metabolic=='true'){$("#venn_meta_dynamic").append(htmlTable);}
			else{$("#venn_path_dynamic").append(htmlTable);}
			
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
		        "ajax": {'url':'/report-portal/report/ajaxpathvenntbl/',
		        	     'type': 'GET',
		        	     'data':{
		        	    	 inter_num: inter_num,
		    		         regulation: regulation,
		    		         members: members,
		    		         is_metabolic: is_metabolic
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
		    	});
			});
	        
		    }
	}
	else{
		$("#tbl-all").fadeIn();
	}
}


function drawVenn(renderTo, file_name1, file_name2, name1, name2, is_metabolic, reg){
	$.get("/report-portal/report/ajaxpathvenn/",
			{
		file_name1: file_name1,
		name1: name1,
		file_name2: file_name2,
		name2: name2,
		is_metabolic: is_metabolic,
		regulation: reg
			},
			function(data){
				var sets = data;
				
				$("#"+renderTo).empty();
    
                var div = d3.select("#"+renderTo);
                div.datum(sets).call(venn.VennDiagram()
                		                              .width(300)
                                                      .height(300));
                
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
                   tooltip.text(d.size + " pathways");
                   

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
                     drawDynamicTable(idx);
                	 
                 });
			}
			);
	
}

$(document).ready(function(){
	// SYGNALING
	
	drawVenn('venn_path-all',
			'all',
			'all',
			'all', 'all', false, 'updown');
		drawVenn('venn_path-all-up',
			'all',
			'all',
			'all', 'all', false, 'up');
	drawVenn('venn_path-all-down',
			'all',
			'all',
			'all', 'all', false, 'down');
	
	/*
	drawVenn('venn_path-nhk-type1',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)', false, 'updown');
	drawVenn('venn_path-nhk-type1-up',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)', false, 'up');
	drawVenn('venn_path-nhk-type1-down',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)', false, 'down');
	
	drawVenn('venn_path-nhk-type2',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)', false, 'updown');
	drawVenn('venn_path-nhk-type2-up',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)', false, 'up');
	drawVenn('venn_path-nhk-type2-down',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)', false, 'down');
	
	
	drawVenn('venn_path-nhk-type3',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)', false, 'updown');
	drawVenn('venn_path-nhk-type3-up',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)', false, 'up');
	drawVenn('venn_path-nhk-type3-down',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)', false, 'down');
	
	drawVenn('venn_path-type1-type2',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)', false, 'updown');
	drawVenn('venn_path-type1-type2-up',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)', false, 'up');
	drawVenn('venn_path-type1-type2-down',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)', false, 'down');
	
	drawVenn('venn_path-type1-type3',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)', false, 'updown');
	drawVenn('venn_path-type1-type3-up',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)', false, 'up');
	drawVenn('venn_path-type1-type3-down',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)', false, 'down');
	
	drawVenn('venn_path-type2-type3',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)', false, 'updown');
	drawVenn('venn_path-type2-type3-up',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)', false, 'up');
	drawVenn('venn_path-type2-type3-down',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)', false, 'down');
	*/
	// METABOLISM
	
	drawVenn('venn_meta-all',
			'all',
			'all',
			'all', 'all', true, 'updown')
	drawVenn('venn_meta-all-up',
			'all',
			'all',
			'all', 'all', true, 'up')
	drawVenn('venn_meta-all-down',
			'all',
			'all',
			'all', 'all', true, 'down')
	
	/*		
	drawVenn('venn_meta-nhk-type1',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)', true, 'updown');
	drawVenn('venn_meta-nhk-type1-up',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)', true, 'up');
	drawVenn('venn_meta-nhk-type1-down',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)', true, 'down');
	
	drawVenn('venn_meta-nhk-type2',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)', true, 'updown');
	drawVenn('venn_meta-nhk-type2-up',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)', true, 'up');
	drawVenn('venn_meta-nhk-type2-down',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)', true, 'down');
	
	drawVenn('venn_meta-nhk-type3',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)', true, 'updown');
	drawVenn('venn_meta-nhk-type3-up',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)', true, 'up');
	drawVenn('venn_meta-nhk-type3-down',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)', true, 'down');
	
	drawVenn('venn_meta-type1-type2',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)', true, 'updown');
	drawVenn('venn_meta-type1-type2-up',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)', true, 'up');
	drawVenn('venn_meta-type1-type2-down',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)', true, 'down');
	
	drawVenn('venn_meta-type1-type3',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)', true, 'updown');
	drawVenn('venn_meta-type1-type3-up',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)', true, 'up');
	drawVenn('venn_meta-type1-type3-down',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)', true, 'down');
	
	drawVenn('venn_meta-type2-type3',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)', true, 'updown');
	drawVenn('venn_meta-type2-type3-up',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)', true, 'up');
	drawVenn('venn_meta-type2-type3-down',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)', true, 'down');
  */       
});
