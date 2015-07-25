function setup_datetimepicker() {
    $(".iDateField").datepicker({dateFormat:'dd-mm-yy',changeMonth:true,changeYear:true,yearRange:"1980:2020"});
    $(".iDateTimeField").datetimepicker({dateFormat:'dd-mm-yy',timeformat:'hh:mm:ss',changeMonth:true,changeYear:true,yearRange:"1980:2020"});
    $(".iTimeField").timepicker();
}
$(window).load(setup_datetimepicker);
