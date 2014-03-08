var adv_flag=false,search_flag=false;
document.onkeydown=keymanager;

function adv_mouseover()
{ adv_flag=true;
}

function adv_mouseout()
{ adv_flag=false;
}

function openAdvSearch()
{ e=document.getElementById("adv-search-popup");
  e.style.display="block";	
  search_flag=true;
}
function closeAdvSearch()
{ if(!adv_flag)
  { e=document.getElementById("adv-search-popup");  
    e.style.display="none";
  }    
  search_flag=false;
}

function checkbox_click(checkbox)
{ var checked = Array();
  for(var i=1;i<=5;i++)
  {checked.push(document.getElementById("adv"+i).checked);
  }
  var no = eval(checkbox.id[3]);
  if(no==1 || no==2)
  { 
     if(!checked[0]&&!checked[1])
	checkbox.checked = true;
  }
  if(no==3||no==4||no==5)
  { if(!checked[2]&&!checked[3]&&!checked[4])
     checkbox.checked = true;
  }
}  
var b=0;
function loginform_display(e)
{
if(b)
{document.forms['lform'].style.display="none";b=0;document.getElementById('backy-dummy').style.display="none";}
else{document.forms['lform'].style.display="block";b=1;document.getElementById('backy-dummy').style.display="block";}
}

function subscriber_open()
{
document.getElementById("backy_subby").style.display="block";
document.getElementById("subscriber_show").style.display="block";
}

function subscriber_close()
{
document.getElementById("backy_subby").style.display="none";
document.getElementById("subscriber_show").style.display="none";

}










function exec_focus()
{   
    var i = document.getElementById("search_field");
    if(i.className=="pseudo_off")
    {i.className="on";return;}
    
    if(i.className=="off")
    {i.className="on";i.value="";}
    else 
    {
	if(i.value=="")
	{
	 i.value="L";
	 i.className="off";
	}
	else
	i.className="pseudo_off";
    }
}
  
function sform_display(e)
{
  document.getElementById('backy-2-dummy').style.display="block";
}search_from_b(this.value);
function sform_undisplay(e)
{
  document.getElementById('backy-2-dummy').style.display="none"; closeAdvSearch();
}


function search_from_b()
{

if(document.getElementById("search_field").value=="L")
return;
else
search();
}

function keymanager(e)
{
var evtobj = window.event ? event : e;
var unicode = evtobj.charCode ? evtobj.charCode : evtobj.keyCode;
if(unicode == 13 && document.getElementById('search_field').value!="L")
search();

}



