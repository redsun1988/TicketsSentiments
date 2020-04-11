$(function(){
    $("#gridContainer").dxDataGrid({
        dataSource: "http://172.22.4.38:5000/getTodayComments",
        showBorders: true
    });
});