    function switchMemberStatus(group_id, username, anchor) {
      anchor_status = anchor.innerHTML.toLowerCase();
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
        if(anchor_status=="add")
          anchor.innerHTML="Delete";
        else
          anchor.innerHTML="Add";
        }
      }
      var url = '/groups/' + group_id + '/' + username + '/' + anchor_status + '/';
      xmlhttp.open("GET",url,false);
      xmlhttp.send(null);
    }
