// Dimensions of sunburst.
var width = (($(document).width() - 5) / 12) * 8;
var height = $(window).height() / 12 * 8;
var radius = Math.min(width, height) / 2;

var file = "../../information/emal-graph-1.csv";

var colorScale = ['#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476', '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9']

function colorMaker(x) {
    var selectedColor = (((x.charCodeAt(0) + x.charCodeAt(1) + x.charCodeAt(2))) % colorScale.length)
    return colorScale[selectedColor];
}

// Total size of all segments; we set this later, after loading the data.
var totalSize = 0;

var vis = d3.select("#chart").append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .append("svg:g")
    .attr("id", "GRAContainer")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var partition = d3.layout.partition()
    .size([2 * Math.PI, radius * radius])
    .value(function (d) {
        return d.size;
    });

var arc = d3.svg.arc()
    .startAngle(function (d) {
        return d.x;
    })
    .endAngle(function (d) {
        return d.x + d.dx;
    })
    .innerRadius(function (d) {
        return Math.sqrt(d.y);
    })
    .outerRadius(function (d) {
        return Math.sqrt(d.y + d.dy);
    });

d3.json("information/emal-graph-1.json", function (data2) {
    //    console.log(data2);
    var newArray = []
    for (key in data2) {
        //        console.log(data2[key]["Taxonomy"])
        newArray.push([data2[key]["Taxonomy"], data2[key]["GRA"]]);
    }
    //    console.log(newArray)
    var json = buildHierarchy(newArray);
    createVisualization(json);
});

// Use d3.text and d3.csv.parseRows so that we do not need to have a header
// row, and can receive the csv as an array of arrays.
//d3.text(file, function(text) {
//    var json = buildHierarchy(newArray);
//    createVisualization(json);
//});

// Main function to draw and set up the visualization, once we have the data.
function createVisualization(json) {
    // Bounding circle underneath the sunburst, to make it easier to detect
    // when the mouse leaves the parent g.
    vis.append("svg:circle")
        .attr("r", radius)
        .style("opacity", 0);

    // For efficiency, filter nodes to keep only those large enough to see.
    var nodes = partition.nodes(json)
        .filter(function (d) {
            return (d.dx > 0.005); // 0.005 radians = 0.29 degrees
        });

    //    console.log("nodes",JSON.stringify(nodes));

    var path = vis.data([json]).selectAll("path")
        .data(nodes)
        .enter().append("svg:path")
        .attr("display", function (d) {
            return d.depth ? null : "none";
        })
        .attr("d", arc)
        .attr("fill-rule", "evenodd")
        .style("fill", function (d) {
            return colorMaker(d.name);
        })
        .style("opacity", 1)
        .on("mouseover", mouseover);

    var svgWidth = d3.select('#chart').select("svg").style('height').replace('px', '');
    var textHeight = 60;
    var topValue = (textHeight / -2);

    var explanation = vis.append("svg:text")
        .attr('id', 'explanation')
        .attr('y', topValue)
        .attr("text-anchor", "middle")
        .data("TESTING");

    totalSize = path.node().__data__.value;
};

// Fade all but the current sequence, and show it in the breadcrumb trail.
function mouseover(d) {
    if (this.nodeName == 'path') {
        var percentage = (100 * d.value / totalSize).toPrecision(3);
        var percentageString = percentage + "%";
        if (percentage < 0.01) {
            percentageString = "< 0.1%";
        }

        var sequenceArray = getAncestors(d);

        var last_element = sequenceArray[sequenceArray.length - 1];

        d3.select('#explanation')
            .html('');

        d3.select('#explanation')
            .attr('class', '')
            .append('svg:tspan')
            .attr('x', 0)
            .attr('dy', 5)
            .text(last_element.name);
        d3.select('#explanation')
            .append('svg:tspan')
            .attr('x', 0)
            .attr('dy', 30)
            .attr('id', 'percentageString')
            .text(percentageString);
        d3.select('#explanation')
            .append('svg:tspan')
            .attr('x', 0)
            .attr('dy', 20)
            .text('Relative abundance');

        updateTable(sequenceArray);
        // Fade all the segments.
        d3.selectAll("#chart path")
            .style("opacity", 0.25);

        // Then highlight only those that are an ancestor of the current segment.
        vis.selectAll("path")
            .filter(function (node) {
                return (sequenceArray.indexOf(node) >= 0);
            })
            .style("opacity", 1);
    }
}

function updateTable(array) {
    var tableString = "<thead><tr><th>Classifier</th><th>Name</th></tr></thead><tbody id='emal-grph-1-tbl-tbody'>";
    while (array.length < 7) {
        array.push({
            name: ''
        })
    }

    tableString += '<tr><td>Super Kingdom</td><td>' + array[0].name + '</td></tr>';
    tableString += '<tr><td>Q1</td><td>' + array[1].name + '</td></tr>';
    tableString += '<tr><td>Order</td><td>' + array[2].name + '</td></tr>';
    tableString += '<tr><td>Family</td><td>' + array[3].name + '</td></tr>';
    tableString += '<tr><td>Sub Family</td><td>' + array[4].name + '</td></tr>';
    tableString += '<tr><td>Genus</td><td>' + array[5].name + '</td></tr>';
    tableString += '<tr><td>Species</td><td>' + array[6].name + '</td></tr>';

    tableString += '</tbody>';

    $('#emal-grph-1-tbl').html(tableString);
    //$('#emal-grph-1-tbl').css('width',((($( document ).width()-5)/12)*4));
}

// Given a node in a partition layout, return an array of all of its ancestor
// nodes, highest first, but excluding the root.
function getAncestors(node) {
    var path = [];
    var current = node;
    while (current.parent) {
        path.unshift(current);
        current = current.parent;
    }
    return path;
}

// Take a 2-column CSV and transform it into a hierarchical structure suitable
// for a partition layout. The first column is a sequence of step names, from
// root to leaf, separated by hyphens. The second column is a count of how 
// often that sequence occurred.
function buildHierarchy(csv) {
    var root = {
        "name": "root"
        , "children": []
    };
    for (var i = 0; i < csv.length; i++) {
        var sequence = csv[i][0];
        var size = +csv[i][1];
        if (isNaN(size)) { // e.g. if this is a header row
            continue;
        }
        var parts = sequence.split("=");
        var currentNode = root;
        for (var j = 0; j < parts.length; j++) {
            var children = currentNode["children"];
            var nodeName = parts[j];
            var childNode;
            if (j + 1 < parts.length) {
                // Not yet at the end of the sequence; move down the tree.
                var foundChild = false;
                for (var k = 0; k < children.length; k++) {
                    if (children[k]["name"] == nodeName) {
                        childNode = children[k];
                        foundChild = true;
                        break;
                    }
                }
                // If we don't already have a child node for this branch, create it.
                if (!foundChild) {
                    childNode = {
                        "name": nodeName
                        , "children": []
                    };
                    children.push(childNode);
                }
                currentNode = childNode;
            } else {
                // Reached the end of the sequence; create a leaf node.
                childNode = {
                    "name": nodeName
                    , "size": size
                };
                children.push(childNode);
            }
        }
    }
    return root;
};