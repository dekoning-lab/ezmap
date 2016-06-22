var margin = {
        top: 20
        , right: 90
        , bottom: 30
        , left: 70
    }
    , width = $('#collapseSeven').width() - margin.left - margin.right
    , height = ($(window).height() / 12 * 7) - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width - 100], .1);

var y = d3.scale.linear()
    .rangeRound([height, 0]);

var color = d3.scale.category10();

var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function (d) {
        return "<div style='text-align:center'>" + d.file + "</br></br><strong>" + d.name + " : </strong> <span>" + (d.y1 - d.y0).toFixed(2) + "%</span></div>";
    })

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .ticks(20)
    .orient("left")
    .tickFormat(d3.format(".2s"));

var svg = d3.select("#mappedTo-graph").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip);

d3.json("information/mappedto.json", function (error, data) {
    if (error) throw error;

    color.domain(d3.keys(data[0]).filter(function (key) {
        return key !== "File";
    }));

    data.forEach(function (d) {
        var y0 = 0;
        d.ages = color.domain().map(function (name) {
            return {
                name: name
                , file: d.File
                , y0: y0
                , y1: y0 += +d[name]

            };
        });
        d.total = d.ages[d.ages.length - 1].y1;
    });

    data.sort(function (a, b) {
        return b.total - a.total;
    });

    x.domain(data.map(function (d) {
        return d.File;
    }));
    y.domain([0, 100]);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -50)
        .attr("x", (-(height / 2) + 54 / 2))
        .attr("dy", ".81em")
        .style("text-anchor", "end")
        .text("Percent");

    var file = svg.selectAll(".file")
        .data(data)
        .enter().append("g")
        .attr("class", "g")
        .attr("transform", function (d) {
            return "translate(" + x(d.File) + ",0)";
        });

    file.selectAll("rect")
        .data(function (d) {
            return d.ages;
        })
        .enter().append("rect")
        .attr("fileName", function (d) {
            return d.File
        })
        .attr("width", x.rangeBand())
        .attr("y", function (d) {
            return y(d.y1);
        })
        .attr("height", function (d) {
            return y(d.y0) - y(d.y1);
        })
        .style("fill", function (d) {
            return color(d.name);
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    var legend = svg.selectAll(".legend")
        .data(color.domain().slice().reverse())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
            return "translate(30," + i * 20 + ")";
        });

    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width - 22)
        .attr("y", 7)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function (d) {
            return d;
        });
});