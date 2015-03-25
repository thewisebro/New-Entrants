$('.change_status_link').click(function(e) {
      var enrollment_no = this.id.replace('change_status_','');
      span = '#status_'+enrollment_no;
      old_status = $(span).html();
      $(span).html('Updating..');
      $.ajax({ url     : '/placement/changestatus/'+enrollment_no,
               async   : false,
               success : function(result) {
                           if(result.indexOf('ERROR') == 0)
                           {
                             $(span).html(old_status);
                             $('#error_popup').html(result);
                             $('#error_popup').dialog({
                                 modal     : true,
                                 resizable : false,
                                 heigth    : 300,
                                 width     : 600,
                                 buttons   : { Ok : function() { $(this).dialog('close'); }}
                               });
                           }
                           else $(span).html(result);
                         }
        });
      e.preventDefault();
    });


function change_status (enrollment_no, plac_status)
{
    old_status = document.getElementById('old_status_'+enrollment_no).innerHTML;
    if (old_status!=plac_status)
    {
      var xmlhttp;
      if (window.XMLHttpRequest) {
          xmlhttp=new XMLHttpRequest();
      } else {
          xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
      xmlhttp.onreadystatechange=function() {
          if (xmlhttp.readyState==4 && xmlhttp.status==200) {
              document.getElementById('status_'+plac_status+'_'+enrollment_no).className="btn btn-primary";
              document.getElementById('status_'+old_status+'_'+enrollment_no).className="btn";
              document.getElementById('old_status_'+enrollment_no).innerHTML = plac_status;
              if (xmlhttp.resonseText)
              {
                    $('#error_popup').html(xmlhttp.responseText);
                    $('#error_popup').dialog({
                                 modal     : true,
                                 resizable : false,
                                 heigth    : 300,
                                 width     : 600,
                                 buttons   : { Ok : function() { $(this).dialog('close'); }}
                               });
              }

          }
      }
    xmlhttp.open("GET","/placement/changestatus/"+enrollment_no+"/"+plac_status+"/",false);
    xmlhttp.send();
    }
    if (plac_status=='CLS')  
    {
                    $('#dialog_popup').html('You have changed the status to closed, This person will not appear in Search Results again unless you change his status.');
                    $('#dialog_popup').dialog({
                                 modal     : true,
                                 resizable : false,
                                 heigth    : 300,
                                 width     : 600,
                                 buttons   : { Ok : function() { $(this).dialog('close'); }}
                               });

    }
}


function change_debar_status(enrollment_no, new_status)
{
    if (new_status == 'N')
      old_status = 'Y';
    else
      old_status = 'N';
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp=new XMLHttpRequest();
    } else {
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            document.getElementById('debar_'+new_status+'_'+enrollment_no).className="btn btn-primary";
            document.getElementById('debar_'+old_status+'_'+enrollment_no).className="btn";
            if (xmlhttp.resonseText)
            {
                  $('#error_popup').html(xmlhttp.responseText);
                  $('#error_popup').dialog({
                               modal     : true,
                               resizable : false,
                               heigth    : 300,
                               width     : 600,
                               buttons   : { Ok : function() { $(this).dialog('close'); }}
                             });
            }

        }
    }
    xmlhttp.open("GET","/placement/changedebarstatus/"+enrollment_no+"/"+new_status+"/",false);
    xmlhttp.send();
}
