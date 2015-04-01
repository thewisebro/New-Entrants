function switchApplicationStatus(company_id, anchor) {
    status = anchor.innerHTML.toLowerCase();
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp=new XMLHttpRequest();
    } else {
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if(xmlhttp.responseText != "True") {
                alert(xmlhttp.responseText);
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
        else  {
            alert('The server returned a status of '+xhttp.status+'. Please contact IMG to resolve this problem.');
        }
    }
    xmlhttp.open("GET","/internship/company/"+company_id+"/"+status+"/",false);
    xmlhttp.send();
}
