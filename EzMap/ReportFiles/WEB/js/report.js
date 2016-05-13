

$(document).ready(function(){
    getProjectInformation();
    
    var fullDate = new Date()
    var twoDigitMonth = ((fullDate.getMonth().length+1) === 1)? (fullDate.getMonth()+1) : '0' + (fullDate.getMonth()+1);
    var currentDate = fullDate.getDate() + "/" + twoDigitMonth + "/" + fullDate.getFullYear();
    $('#DATE').text(currentDate);

    $('#collapseOne').load("information/filelist.txt");
    csvToTable("information/prinseq-tbl-1.csv",$('#prinseqTblOneDiv'),'prinseqTblOne', 'PRINSEQ Results')
    csvToTable("information/bowtie2-tbl-1.csv",$('#humanMappingTblOneDiv'),'humanMappingTblOne', 'BowTie2 Results')
    csvToTable("information/samtools-tbl-1.csv",$('#unamppedTblOneDiv'),'unamppedTblOne', 'SamTools Results')
    csvToTable("information/blastn-tbl-1.csv",$('#blastTblOneDiv'),'blastTblOne', 'Blastn Results')
    csvToTable("information/emal-tbl-1.csv",$('#emalTblOneDiv'),'emalTblOne', 'EMAL Results')
    csvToTable("information/emal-tbl-2.csv",$('#emalTblTwoDiv'),'emalTblTwo', 'EMAL Family Results')

    $('#collapseAll').on('click', function (e) {
        $(".panel-collapse").collapse('hide');
        $(".panelIcon").removeClass('fa-chevron-down');
        $(".panelIcon").addClass('fa-chevron-right');
    });

    $('#uncollapseAll').on('click', function (e) {
        $(".panel-collapse").collapse('show');
        $(".panelIcon").removeClass('fa-chevron-right');
        $(".panelIcon").addClass('fa-chevron-down');
    });

    $('#print').on('click', function(e){
        window.print();
    });

    var resizeId;
    
    $(window).resize(function() {
        clearTimeout(resizeId);
        resizeId = setTimeout(doneResizing, 300);
    });
    
    $('.panel').on('show.bs.collapse', function (e) {
        $('#'+e.currentTarget.id+'Icon').removeClass('fa-chevron-righ').addClass('fa-chevron-down');
    })
    $('.panel').on('hide.bs.collapse', function (e) {
        $('#'+e.currentTarget.id+'Icon').removeClass('fa-chevron-down').addClass('fa-chevron-right');
    })
    $('#panel7').on('show.bs.collapse', function (e) {
        $('#mappedTo-graph').html('');
        initializeFileDistGraph();
    })
    
    $('#downloadFileMappingDist').on("click", saveFileMappingSVG);
    $('#downloadGRA').on("click", saveGRASVG);
    
    initializePieChart();
    initializeGRAGraph();
});

function initializeGRAGraph (){
    $.getScript( "WEB/js/sequences.js", function( data, textStatus, jqxhr ) {});
}

function initializePieChart (){
    $.getScript( "WEB/js/piechart.js", function( data, textStatus, jqxhr ) {});
}

function initializeFileDistGraph(){
    $.getScript( "WEB/js/mappedTo.js", function( data, textStatus, jqxhr ) {});
}

function saveFileMappingSVG (){
    try {
        var isFileSaverSupported = !!new Blob();
    } catch (e) {
        alert("blob not supported");
    }

    $('#mappedTo-graph').find("svg").attr("title", "test2").attr("version", 1.1).attr("xmlns", "http://www.w3.org/2000/svg");
    var innerHTML = $('#mappedTo-graph').html();

    var blob = new Blob([innerHTML], {type: "image/svg+xml"});
    saveAs(blob, "fileMappingDistribution.svg");
}

function saveGRASVG (){
    try {
        var isFileSaverSupported = !!new Blob();
    } catch (e) {
        alert("blob not supported");
    }

    $('#chart').find("svg").attr("title", "test2").attr("version", 1.1).attr("xmlns", "http://www.w3.org/2000/svg");
    var innerHTML = '<svg'+$('#chart').html().split('<svg').pop();
    
    var blob = new Blob([innerHTML], {type: "image/svg+xml"});
    saveAs(blob, "fileMappingDistribution.svg");
}

function getProjectInformation(){
    var file = 'information/projInfo.txt'
    $.get(file, function(data) {
        var rows = data.split("\n");
        for (i=0; i < rows.length;i++){
            var row = rows[i].split('=');
            if (i==0){
                $('#projTitle').text('Project: '+row[1]);
            }
            else if (i==1){
                $('#date').text(row[1]);
            }
        }
    });
}

function doneResizing(){
    $('#chart').html('');
    $('#summedPieChart').html('');
    initializeGRAGraph ();
    $('#mappedTo-graph').html('');
    initializeFileDistGraph();
    initializePieChart(); 
    console.log('Resize done!');
}

function csvToTable(file, $table, id, caption) {
    var table = $.get(file, function(data, dataSet) {

        // start the table
        var dataSet = [];
        var head = [];
        var count = 0;
        // split into lines
        var rows = data.split("\n");
        // parse lines
        rows.forEach( function getvalues(row) {
            // split line into columns
            var columns = row.split(",");
            if (count == 0 && columns[0].length > 0){
                head = columns
            }
            if (count > 0 && columns[0].length > 0){
                for (i = 0; i < columns.length; i++) {
                    start = columns[i].indexOf("[");
                    if (start > 0){
                        end = columns[i].indexOf("]");
                        taxid = columns[i].substring(start+1,end);
                        string = '[<a href="http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id='+taxid+'" target="_blank">'+taxid+'</a>'
                        columns[i] = columns[i].replace('['+taxid,string);
                    }
                }
                dataSet.push(columns);
            }
            count += 1;
        });
        var header = [];
        head.forEach(function createHeader(col) {
            dic = {};
            dic["title"] = col ;
            header.push(dic);
        });
        $table.html('<table class="table" id="'+id+'"></table>');
        $table = $('#'+id);
        if (id == 'emalTblTwo'){
            $('#summedOverTitle').text('Genome Relative Abundance Summed Over '+header[1].title)
        }
        if (id == 'emalTblOne' || id == 'emalTblTwo'){
            $table.DataTable( {
                "data": dataSet,
                "columns": header,
                "paging":   true,
                "info":     false,
                "responsive": true,
                "order": [[ 0, "desc" ]],
                "fnCreatedRow": function( nRow, aData, iDataIndex ) {
                    var name = aData[1]
                    name = name.substring(0,name.indexOf('['))
                    $(nRow).attr('id', 'test-'+name);
                }
            });
        }
        else{
            $table.dataTable( {
                "data": dataSet,
                "columns": header,
                "paging":   true,
                "info":     false,
                "responsive": true,
            } ); 
        }
    });

}

