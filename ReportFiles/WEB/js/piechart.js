var w = 444;
var h = 444;
var r = h / 2; //radius

var colorScale = ['#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476', '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9']

function colorMaker2(x) {
    if (x != null) {
        x = x.split('[')[0].replace(' ', '');
        var num = 0;
        for (var i = 0, len = x.length; i < len; i++) {
            num += x.charCodeAt(i);
        }
        var selectedColor = num % colorScale.length;
        return colorScale[selectedColor];
    }
}

d3.json("information/emal-tbl-2.json", function (error, data, taxLevel) {
    var vis = d3.select("#summedPieChart")
        .append("svg:svg") //create the SVG element inside the <body>
        .data([data]) //associate our data with the document
        .attr("width", w) //set the width and height of our visualization (these will be attributes of the <svg> tag
        .attr("height", h)
        .append("svg:g") //make a group to hold our pie chart
        .attr("transform", "translate(" + r + "," + r + ")") //move the center of the pie chart from 0, 0 to radius, radius

    //Get the summed over taxonomic level
    if (Object.getOwnPropertyNames(data[0])[0] == 'GRA') {
        taxLevel = Object.getOwnPropertyNames(data[0])[1]
    }
    if (Object.getOwnPropertyNames(data[0])[1] == 'GRA') {
        taxLevel = Object.getOwnPropertyNames(data[0])[0]
    }

    var arc = d3.svg.arc() //this will create <path> elements for us using arc data
        .outerRadius(r);

    var pie = d3.layout.pie() //this will create arc data for us given a list of values
        .value(function (d) {
            return d.GRA;
        }); //we must tell it out to access the value of each element in our data array

    var arcs = vis.selectAll("g.slice") //this selects all <g> elements with class slice (there aren't any yet)
        .data(pie) //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties) 
        .enter() //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
        .append("svg:g") //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
        .attr("class", "slice")
        .attr('id', function (d, i) {
            return (data[i][taxLevel]);
        })
        .on("mouseover", mouseover)
        .on("mouseleave", mouseleave); //allow us to style things in the slices (like text)

    arcs.append("svg:path")
        .attr("fill", function (d, i) {
            return colorMaker2(data[i][taxLevel]);
        }) //set the color function inside of sequences.js
        .attr("d", arc)
        //this creates the actual SVG path using the associated data (pie) with the arc drawing function

});

function mouseover(d) {
    if (this.nodeName == 'g') {
        var name = this.getAttribute('id');
        name = name.substring(0, name.indexOf('['));

        var row = document.getElementById(name);
        row.style.backgroundColor = '#ADD8E6'
    }
}

function mouseleave(d) {
    if (this.nodeName == 'g') {
        var name = this.getAttribute('id');
        name = name.substring(0, name.indexOf('['));

        var row = document.getElementById(name);
        row.style.backgroundColor = '#ffffff'
    }
}