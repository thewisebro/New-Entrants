// Pass this function the 'id' of 2 elements in HTML to show/hide alternatively.
var current_visibility=false;
function element_display(a, b)
{
  if(current_visibility)
  {
    document.getElementById(a).style.display="none";
    document.getElementById(b).style.display="block";
    current_visibility=false;
  }
  else{
    document.getElementById(a).style.display="block";
    document.getElementById(b).style.display="none";
    current_visibility=true;
  }
}
