function check_all(string){
  buttons = document.getElementsByName('selected_'+string);
  for (i=0; i<buttons.length; i++)
    buttons[i].checked = true;
}

function uncheck_all(string){
  buttons = document.getElementsByName('selected_'+string);
  for (i=0; i<buttons.length; i++)
    buttons[i].checked = false;
}
