function setup_form(){
  try{
    $('form.uniForm').uniform();
  }catch(e){};

  try{
    $(".iDateField").datepicker({dateFormat:'dd-mm-yy',changeMonth:true,changeYear:true,yearRange:"1980:2020"});
    $(".iDateTimeField").datetimepicker({dateFormat:'dd-mm-yy',timeformat:'hh:mm:ss',changeMonth:true,changeYear:true,yearRange:"1980:2020"});
    $(".iTimeField").timepicker();
  }catch(e){};

  try{
    $(".chosen-select").chosen();
  }catch(e){};
}

$(window).load(setup_form);
