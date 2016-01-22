$(function () {
	
	//$('body').append('<script src="/static/report/loreal/js/3d.js" type="text/javascript"></script>');
        
        var series = [{"data": [[85.09840460245171, 65.4979919793391, 54.7659670378979], [33.2157099756499, 62.052086125375205, 13.420775414913098], [44.57002774365029, 46.016480543937995, -9.002421360827132], [21.813549936177896, 59.4559604641128, -42.0256945171101]], "name": "RhE(Type1)"}, {"data": [[21.8534765915116, 39.4155370315003, -56.4742305346142], [39.5412185424973, 54.618649039443, -4.452332248573639], [26.7228803018857, 58.0747206953156, -57.0362366667697]], "name": "RhE(Type3)"}, {"data": [[-129.205846413558, -10.743193452358401, 13.9945594483372], [-156.656084548068, -6.708653379319331, 23.9189159490728], [-132.936337425985, -17.708819748344702, 4.48138650020932], [-105.07311497720801, -6.87368000532608, 47.0154369237953]], "name": "NHK"}, {"data": [[62.350644938302494, 44.3008900383373, 100.03204214999], [12.8475571938309, 31.898758152122003, 8.559930973806889], [1.5705267912011103, 31.575390495918498, -25.8168675652842], [-27.4364186066918, 28.7593554094805, -59.0230964044116]], "name": "RhE(Type2)"}, {"data": [[36.0884278468725, -126.034128457482, -22.6903541603493], [29.3272942099548, -128.380562899777, -51.72399674614161], [57.3362524600144, -119.963767509518, 11.725566481676399], [78.9718308375093, -105.253014522756, 50.3306493243824]], "name": "NHE"}];
        
        
        // Give the points a 3D feel by adding a radial gradient
        /*
        Highcharts.getOptions().colors = $.map(Highcharts.getOptions().colors, function (color) {
            return {
                radialGradient: {
                    cx: 0.4,
                    cy: 0.3,
                    r: 0.5
                },
                stops: [
                    [0, color],
                    [1, Highcharts.Color(color).brighten(-0.2).get('rgb')]
                ]
            };
        });
        */
        // Set up the chart
        var chart = new Highcharts.Chart({
            chart: {
                renderTo: 'genes-3d',
                margin: 100,
                type: 'scatter',
                options3d: {
                    enabled: true,
                    alpha: 10,
                    beta: 30,
                    depth: 250,
                    viewDistance: 5,

                    frame: {
                        bottom: { size: 1, color: 'rgba(0,0,0,0.02)' },
                        back: { size: 1, color: 'rgba(0,0,0,0.04)' },
                        side: { size: 1, color: 'rgba(0,0,0,0.06)' }
                    }
                }
            },
            title: {
                text: 'Draggable box'
            },
            subtitle: {
                text: 'Click and drag the plot area to rotate in space'
            },
            tooltip: {
                pointFormatter: function(){
                    return ""
                }
            },

            plotOptions: {
                scatter: {
                    width: 10,
                    height: 10,
                    depth: 10,
                }
            },
            yAxis: {
                // min: 0,
                // max: 10,
                title: null
            },
            xAxis: {
                // min: 0,
                // max: 10,
                gridLineWidth: 1
            },
            zAxis: {
                // min: 0,
                // max: 10,
                showFirstLabel: false
            },
            legend: {
                enabled: true,
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: 0,
                y: 100
            },
            series: series
        });


        // Add mouse events for rotation
        $(chart.container).bind('mousedown.hc touchstart.hc', function (eStart) {
            eStart = chart.pointer.normalize(eStart);

            var posX = eStart.pageX,
                posY = eStart.pageY,
                alpha = chart.options.chart.options3d.alpha,
                beta = chart.options.chart.options3d.beta,
                newAlpha,
                newBeta,
                sensitivity = 5; // lower is more sensitive

            $(document).bind({
                'mousemove.hc touchdrag.hc': function (e) {
                    // Run beta
                    newBeta = beta + (posX - e.pageX) / sensitivity;
                    chart.options.chart.options3d.beta = newBeta;

                    // Run alpha
                    newAlpha = alpha + (e.pageY - posY) / sensitivity;
                    chart.options.chart.options3d.alpha = newAlpha;

                    chart.redraw(false);
                },
                'mouseup touchend': function () {
                    $(document).unbind('.hc');
                }
            });
        });

    });