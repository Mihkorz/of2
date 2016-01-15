
function drawVenn(renderTo, file_name1, file_name2, name1, name2, is_metabolic){
	$.get("/report-portal/report/ajaxpathvenn/",
			{
		file_name1: file_name1,
		name1: name1,
		file_name2: file_name2,
		name2: name2,
		is_metabolic: is_metabolic
			},
			function(data){
				var sets = data;
				
				$("#"+renderTo).empty();
    
                var div = d3.select("#"+renderTo);
                div.datum(sets).call(venn.VennDiagram());
                
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
                 .on("click", function(d, i){alert(d.size)});
			}
			);
	
}

$(document).ready(function(){
	// SYGNALING
	drawVenn('venn_path-all',
			'all',
			'all',
			'all', 'all', false)
	drawVenn('venn_path-nhk-type1',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)', false);
	drawVenn('venn_path-nhk-type2',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)', false);
	drawVenn('venn_path-nhk-type3',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)', false);
	drawVenn('venn_path-type1-type2',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)', false);
	drawVenn('venn_path-type1-type3',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)', false);
	drawVenn('venn_path-type2-type3',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)', false);
	
	// METABOLISM
	drawVenn('venn_meta_all',
			'all',
			'all',
			'all', 'all', true)
	drawVenn('venn_meta_nhk-type1',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)', true);
	drawVenn('venn_meta_nhk-type2',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)', true);
	drawVenn('venn_meta_nhk-type3',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)', true);
	drawVenn('venn_meta_type1-type2',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)', true);
	drawVenn('venn_meta_type1-type3',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)', true);
	drawVenn('venn_meta_type2-type3',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)', true);
          
});