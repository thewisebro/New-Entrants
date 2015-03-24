function toggle() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp=new XMLHttpRequest();
    } else {
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
                $( "#status_message").html(xmlhttp.response);
                $( "#status_change_alert" ).dialog({
                    modal: true,
                    width:500,
                    buttons: {
                        Ok: function() { $( this ).dialog( "close" ); }
                    }
                });
                return 0;
        }
        else  {
            $( "#status_message").html('The server returned a status of '+xmlhttp.status+'. Please contact IMG to resolve this problem.');
            $( "#status_change_alert" ).dialog({
                modal: true,
                width:500,
                buttons: {
                    Ok: function() { $( this ).dialog( "close" ); }
                }
            });
            return 0;
        }
    }
    xmlhttp.open("GET","/placement/toggle/",false);
    xmlhttp.send();
}
