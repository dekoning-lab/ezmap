var w = 444;
var h = 444;
var r = h/2;                           //radius
color = d3.scale.category20c();     //builtin range of colors

d3.csv("../../information/emal-tbl-2.csv", function(error, data) {
    var vis = d3.select("#summedPieChart")
    .append("svg:svg")              //create the SVG element inside the <body>
    .data([data])                   //associate our data with the document
    .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
    .attr("height", h)
    .append("svg:g")                //make a group to hold our pie chart
    .attr("transform", "translate(" + r + "," + r + ")")    //move the center of the pie chart from 0, 0 to radius, radius

    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
    .outerRadius(r);

    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
    .value(function(d) { return d.GRA; });    //we must tell it out to access the value of each element in our data array

    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
    .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties) 
    .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
    .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
    .attr("class", "slice")
    .attr('id',function(d, i) { return 'test-'+data[i].Family; })
    .on("mouseover", mouseover)
    .on("mouseleave", mouseleave);//allow us to style things in the slices (like text)
    
    arcs.append("svg:path")
        .attr("fill", function(d, i) { return color(i); } ) //set the color for each slice to be chosen from the color function defined above
        .attr("d", arc)
    //this creates the actual SVG path using the associated data (pie) with the arc drawing function

});

function mouseover(d) {
    if (this.nodeName == 'g'){
        var name = this.getAttribute('id');
        name = name.substring(0,name.indexOf('['));

        var row = document.getElementById(name);
        row.style.backgroundColor = '#ADD8E6'
    }
}

function mouseleave(d) {
    if (this.nodeName == 'g'){
        var name = this.getAttribute('id');
        name = name.substring(0,name.indexOf('['));

        var row = document.getElementById(name);
        row.style.backgroundColor = '#ffffff'
    }
}

