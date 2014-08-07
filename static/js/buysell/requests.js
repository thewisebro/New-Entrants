$(document).ready(function(){
    var reqid = $('#reqid').html();
    if(reqid!=''){
        $('[name="generic_form"]').attr("action", "/buysell/editsave/request/"+reqid+"/");
        }
    });
