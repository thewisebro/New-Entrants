function switchApplicationStatus(company_id, anchor) {
    status = $.trim(anchor.innerHTML).toLowerCase();
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp=new XMLHttpRequest();
    } else {
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if(xmlhttp.responseText != "True") {
                $( "#application_status_message").html(xmlhttp.response);
                $( "#application_status_change_alert" ).dialog({
                    modal: true,
                    width:500,
                    buttons: {
                        Ok: function() { $( this ).dialog( "close" ); }
                    }
                });
                return 0;
            }
            if(status=="apply") {//The user just applied to the company
                anchor.innerHTML="Withdraw";
                document.getElementById('resumelink'+company_id).style.visibility = 'visible';
            }
            else {
                anchor.innerHTML="Apply";
                document.getElementById('resumelink'+company_id).style.visibility = 'hidden';
            }
        }
        /*else  {
            $( "#application_status_message").html('The server returned a status of '+xmlhttp.status+'. Please contact IMG to resolve this problem.');
            $( "#application_status_change_alert" ).dialog({
                modal: true,
                width:500,
                buttons: {
                    Ok: function() { $( this ).dialog( "close" ); }
                }
            });
        }*/
    }
    xmlhttp.open("GET","/placement/company/"+company_id+"/"+status+"/",false);
    xmlhttp.send();
}
