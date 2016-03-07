function switch_clicked(type){
  if(type===1)
    var elem = $('#id_email_subscribed')[0];
  else
    var elem = $('#id_subscribed')[0];
  if(elem.checked)elem.checked = false;
  else elem.checked = true;
  $('#events-subscription-submit').click();
}
