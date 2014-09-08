function switch_clicked(){
  var elem = $('#id_email_subscribed')[0];
  if(elem.checked)elem.checked = false;
  else elem.checked = true;
  $('#events-subscription-submit').click();
}
