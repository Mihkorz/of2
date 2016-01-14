
function drawVenn(renderTo, file_name1, file_name2, name1, name2){
	$.get("/report-portal/report/ajaxpathvenn/",
			{
		file_name1: file_name1,
		name1: name1,
		file_name2: file_name2,
		name2: name2
			},
			function(data){
				var sets = data;
				
				$("#"+renderTo).empty();
    
                var div = d3.select("#"+renderTo);
                div.datum(sets).call(venn.VennDiagram());
			}
			);
}

$(document).ready(function(){
	
	drawVenn('venn_path-nhk-type1',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'NHK', 'RhE (Type1)');
	drawVenn('venn_path-nhk-type2',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'NHK', 'RhE (Type2)');
	drawVenn('venn_path-nhk-type3',
			'output_loreal_preprocessed_NHK.txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'NHK', 'RhE (Type3)');
	drawVenn('venn_path-type1-type2',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'RhE (Type1)', 'RhE (Type2)');
	drawVenn('venn_path-type1-type3',
			'output_loreal_preprocessed_RhE (Type 1).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type1)', 'RhE (Type3)');
	drawVenn('venn_path-type2-type3',
			'output_loreal_preprocessed_RhE (Type 2).txt.xlsx',
			'output_loreal_preprocessed_RhE (Type 3).txt.xlsx',
			'RhE (Type2)', 'RhE (Type3)');
          
});