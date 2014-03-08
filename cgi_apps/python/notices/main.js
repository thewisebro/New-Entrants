//current notices on display,are new notices here
//Expired notices on display,are old notices here

var count = 12;
// count is the number of notices being shown in a page

var pages = 5;
// no of max pages to show in pagelinks

var NewNotices, OldNotices=new Array(), CurNotices, SearchNotices, bulkcount = count*pages;
// NewNotices/OldNotices are array of new/old notices
// CurNotices is the array of Notices currently being shown on display 

var pageno = 1, bulkno = 1, type = "new", _cat = "all", _subcat, oldbulkno = 0, nomore=false, totalnew, totalold, totalsearch;
var noticepath;
//these are global variables corressponding to current state

var href="";
//assignes value to the address extension for the current state

//escapes html text
function HtmlEscape(str)
{ var result = "";
  for(var i = 0;i < str.length;i++)
  {  if(str[i] == "<")result += "&lt;";
     else if(str[i] == ">")result += "&gt;";
     else if(str[i] == "&")result += "&amp;";
     else result += str[i];
  }
  return result;
}

//returns XMLHttpRequest Object
function getXHRObject()
{ var xhr; 
  if(window.XMLHttpRequest)
     xhr =  new XMLHttpRequest();
  else if(window.ActiveXObject)
     xhr =  new ActiveXObject("Microsoft.XMLHTTP");
  xhr.onreadystatechange = function()
  {  if (xhr.readyState==4 && xhr.status==200)
       document.body.style.cursor = 'default';
     else 
       document.body.style.cursor = 'wait';     
  }
  return xhr;

}




//parse the xml-text to xml dom
function parsetoXml(txt)
{ 
  var xmlDoc;
  try 
  {
    xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
    xmlDoc.async="false";
    xmlDoc.loadXML(txt);
    return xmlDoc; 
  }
  catch(e)
  {
    parser=new DOMParser();
    xmlDoc=parser.parseFromString(txt,"text/xml");
    return xmlDoc;
  }
}


//updates new notices through ajax
//this function updates all new notices 
function updateNew()
{ 
  var xhr;
  xhr=getXHRObject();
  xhr.open("get","handle.cgi?action=new_notices&after=0&max=all",false);
  xhr.send();
  notices=parsetoXml(xhr.responseText);
  totalnew=eval(notices.getElementsByTagName("total")[0].childNodes[0].nodeValue);
  if(notices.getElementsByTagName("status")[0].childNodes[0].nodeValue=="failure")return false;
  NewNotices=notices.getElementsByTagName("notice")
  return true;
}

//update old notices through ajax
//this function updates bulkno(pages*count) notices at a time
function updateOld()
{
  if(nomore)return false;
  xhr=getXHRObject();
  xhr.open("get","handle.cgi?action=old_notices&after="+oldbulkno*bulkcount+"&max="+bulkcount,false);
  xhr.send();
  notices=parsetoXml(xhr.responseText);
  totalold=eval(notices.getElementsByTagName("total")[0].childNodes[0].nodeValue);
  if(notices.getElementsByTagName("nomore")[0].childNodes[0].nodeValue=="true")nomore=true;
  if(notices.getElementsByTagName("status")[0].childNodes[0].nodeValue=="failure")return false;
  notices=notices.getElementsByTagName("notice");
  
  for(i=0;i<notices.length;i++)
     OldNotices=OldNotices.concat(notices[i]);
  
  oldbulkno+=1;
  return true;
}


//returns the html row of a notice(date,from,subject)
function getNoticeInfo(notice,alt)
{
  var div;
  id=notice.getElementsByTagName("id")[0].childNodes[0].nodeValue;
  if(alt)
      div='<div class="notice-info-alt" onclick=shownotice(\''+id+'\')>';
  else
      div='<div class="notice-info" onclick=shownotice(\''+id+'\')>'; 

  div+='<div class="date">'+notice.getElementsByTagName("date")[0].childNodes[0].nodeValue+'</div>';
  div+='<div class="from">'+notice.getElementsByTagName("from")[0].childNodes[0].nodeValue+'</div>';
  div+='<div class="subject">'+notice.getElementsByTagName("subject")[0].childNodes[0].nodeValue +'</div>';
  div+='</div>'
  return div;
}


//return the header for above noticeInfo(s)
function getNoticeInfoHeader()
{ 
  var div;
  div='<div id="notice_info_header">';
  div+='<div class="date"> Date </div>';
  div+='<div class="from"> Added By </div>';
  div+='<div class="subject"> Subject </div>';
  div+='</div>'
  return div;
}


//shows the content of notice
function shownotice(id)
{ href="#content/"+id;
  document.location.href=href;
  var xhr=getXHRObject()
  xhr.open("get","handle.cgi?action=getnotice&id="+id,false)
  xhr.send()
  xhr.onreadystatechange=function()
  {   if(xhr.readyState!=4)
         document.body.style.cursor="wait";
       if (xhr.readyState==4 && xhr.status==200)
         document.body.style.cursor="default";
  }    

  var j,previd,nextid,prevdiv,nextdiv,backdiv,p;
  for(j=0;j<CurNotices.length;j++)
    if(CurNotices[j].getElementsByTagName("id")[0].childNodes[0].nodeValue==id)
       break;
  p = Math.floor(j/count)+1;
  if(j>0)previd = CurNotices[j-1].getElementsByTagName("id")[0].childNodes[0].nodeValue;
  if(j<CurNotices.length-1)nextid = CurNotices[j+1].getElementsByTagName("id")[0].childNodes[0].nodeValue;
  
  var newerspan="<span><span style=\"font-family:symbols\"> nn </span> Newer </span>";
  var olderspan="<span> Older <span style=\"font-family:symbols\"> mm </span></span>";

  if(j>0)prevdiv = "<div class=\"prev-notice\" onclick=\"shownotice('"+previd+"')\">"+newerspan+"</div>";
  else  prevdiv = "<div class=\"prev-notice-inact\">"+newerspan+"</div>";
  if(j<CurNotices.length-1)nextdiv = "<div class=\"next-notice\" onclick=\"shownotice('"+nextid+"')\">"+olderspan+"</div>";
  else nextdiv = "<div class=\"next-notice-inact\">"+olderspan+"</div>";

  backdiv = "<div id=\"back_to_list\" onclick='clicked(\"page\","+p+")'><span>Back to Notices list</span></div>\n";
 
  place=document.getElementById("notice-place");
  place.innerHTML = "<div id=\"noticeview-links\">"+prevdiv+backdiv+nextdiv+"</div>"
  place.innerHTML += xhr.responseText;
  pglnks=document.getElementById("pagelinks");
  pglnks.innerHTML = "";
  }
  

//prepares html for pagelinks like < 1 2 3 ...  >
function preparepagelinks()
{ var tpages;
  tpages=Math.floor((eval("total"+type)-1)/count)+1;
  
  
  var start=pageno-(pages+1)/2;
  if(start<0)start=0;
  
  var end=start+pages;
  if(end>tpages)
  {end=tpages;
   if(end-pages<0)start=0;
   else start=end-pages;
  }

  //var start=(bulkno-1)*pages;
  //var end=bulkno*pages;
  var total;
 
  if(type=="new")
      total=CurNotices.length;
  if(type=="old")
      total=totalold;
  if(type=="search")
      total=CurNotices.length;
  
  var div=""
  var attr;
  
  if(type!="old"||_cat=="all")
  {  
     attr=" class='pagelink-act' onclick='clicked(\"back\")' ";
     
     if(start==0)attr=" class='pagelink-inact' ";
     
     div+="<span "+attr+"></span>\n";
     
     if(start==0&&(pageno%pages)==1)
         attr=" class='pagelink-inact'";
     else 
         attr=" class='pagelink-act' onclick='clicked(\"prev\")'";
     
     div+="<span "+attr+">&lt;&nbsp;</span>\n";
     
     for(i=start;i<end;i++)
     { 
        attr=" class='pagelink-act' onclick='clicked(\"page\","+(i+1)+")'";
        if((i+1)==pageno)
            attr=" class='pagelink-curr'";
        if ((i*count)<total)
            div+="<span "+attr+">"+(i+1)+"</span>\n";
     }
     
     attr=" class='pagelink-act' onclick='clicked(\"next\")'";
     
     if(end*count>=total&&((pageno*count)>=total))
         attr=" class='pagelink-inact'";
     
     div+="<span "+attr+">&nbsp;&gt;</span>\n";  
     attr=" class='pagelink-act' onclick='clicked(\"more\")'";
     
     if(end*count>=total)
         attr=" class='pagelink-inact'";
     
     div+="<span "+attr+"></span>\n";
  }
  else
  {  
     attr=" class='pagelink-act' onclick='clicked(\"prev\")' ";
     if(start==0&&(pageno%pages)==1)
         attr=" class='pagelink-inact' ";
     div+="<span "+attr+">&lt;</span>\n";
     attr=" class='pagelink-act' onclick='clicked(\"next\")'";
     
     if(end*count>=CurNotices.length&&((pageno*count)>=CurNotices.length)&&nomore)
         attr=" class='pagelink-inact'";
     div+="<span "+attr+">&gt;</span>\n";
  }
  if(total&&(type!="old"||_cat=="all"))
  {  tpages=Math.floor((total-1)/count)+1;
     div+="<div id='pagelinks_text'> Showing "+pageno+" of "+tpages+" page"+(tpages==1?"":"s")+"</div>";
  }   
  return div;
}


//shows the info of notices and pagelinks on the display page 
function shownotices()
{ href="#"+type+"/"+_cat+"/"+_subcat+"/"+pageno;
  document.location.href= href;
  document.getElementById("notice-path").innerHTML=noticepath;
  place=document.getElementById("notice-place");
  place.innerHTML="";
  start=(pageno-1)*count;
  end=pageno*count;
  
  if(end>CurNotices.length)
     end=CurNotices.length;

  if(type == "search" && totalsearch ==0)
  { place.innerHTML = "No Search found.<br>Include expired notices in advanced search options to make search in expired notices.<br>"+
                      "Else switch to Current notices or Expired notices in top links."
  }
  else
  { place.innerHTML+=getNoticeInfoHeader();
  
    for(var i=start;i<end;i++)
    {
      place.innerHTML+=getNoticeInfo(CurNotices[i],i%2);
    }
  }
  pglnks=document.getElementById("pagelinks");
  pglnks.innerHTML=preparepagelinks();
  
  var current_top,expired_top,search_top;
  current_top = document.getElementById("current");
  expired_top = document.getElementById("expired");
  search_top  = document.getElementById("search-show");
  if(type == "new")
  { current_top.className = "active";
    expired_top.className = "";
    search_top.className = "";
  }  
  else if(type == "old")
  { current_top.className = "";
    expired_top.className = "active";
    search_top.className = "";
  } 
  else if(type == "search")
  { current_top.className = "";
    expired_top.className = "";
    search_top.className = "active";
  }

}



//puts the notices to the CurNotices array to be shown on display page
function makeCurNotices()
{ 
  CurNotices=new Array();
  var Notices;
  
  if(type=="new")Notices=NewNotices;
  else if(type=="old")Notices=OldNotices;
  else if(type=="search")Notices=SearchNotices;
 
  if(_cat=="all")
  {for(i=0;i<Notices.length;i++)
    CurNotices.push(Notices[i]);
  }
  else
  {for(var i=0;i<Notices.length;i++)
   { to=Notices[i].getElementsByTagName("to")[0].childNodes[0].nodeValue;
     if(to.search(_cat)!=-1&&(_subcat=="all"||to.search(_subcat)!=-1))
      CurNotices.push(Notices[i]);
   }
  }
  
  if(type=="new")noticepath="<span class=\"noticepath-text\" onclick=\"catclicked('all','all')\">Current Notices</span>";
  else if(type=="old")noticepath="<span class=\"noticepath-text\" onclick=\"catclicked('all','all')\">Expired Notices</span>";
  else if(type=="search")noticepath="<span class=\"noticepath-text\" onclick=\"catclicked('all','all')\">Searched Notices</span>";
 
  noticepath+=" mm ";
  if(_cat=="all")noticepath+="<span class=\"noticepath-text\" onclick=\"catclicked('all','all')\">All</span>";
  else
  { 
    noticepath+="<span class=\"noticepath-text\" onclick=\"catclicked('"+_cat+"','all')\">"+_cat+"</span>"+" mm ";
    if(_subcat=="all")noticepath+="<span class=\"noticepath-text\" onclick=\"catclicked('"+_cat+"','all')\">All</span>";
    else
    {  
       Cat=eval(_cat);
       for(i=0;i<Cat.length;i++)
       {  
          subcat=Cat[i].split(":")[0];
          name=Cat[i].split(":")[1];
          if(_subcat==subcat)
          {  noticepath+="<span class=\"noticepath-text\" onclick=\"catclicked('"+_cat+"','"+_subcat+"')\">"+name+"</span>";
             break;
          }
       }
    }
  }
}



//handles the clicks on new/old Notices(links) and pagelinks
function clicked(str,no)
{
  if(str=='New')
  { 
    if(NewNotices){}
    else{updateNew();}
    pageno=1;
    bulkno=1;
    _cat="all";
    _subcat=null;
    type="new";
    makeCurNotices();
    shownotices();
  }
  else if(str=='Old')
  { 
    if(OldNotices.length==0)updateOld();
    pageno=1;
    bulkno=1;
    _cat="all";
    _subcat=null;
    type="old";
    makeCurNotices();
    shownotices();
  }
  if(str=="back"&&bulkno!=1)
  { 
 bulkno-=1;
    pageno=(bulkno-1)*pages+1;
    shownotices();
  }
  if(str=="prev")
  {
    if(pageno%pages==1&&bulkno!=1)
    {  bulkno-=1;
       pageno=bulkno*pages;
    }
    else pageno-=1;  
       shownotices();
  } 
  if(str=="page")
  { 
    pageno=no;
    bulkno=(pageno-1-(pageno-1)%pages)/pages+1;
    while(type=="old"&&nomore==false&&(pageno*count)>CurNotices.length)
    {
      updateOld();
      makeCurNotices();
    } 
    shownotices();
  }
  if(str=="next")
  {
    if(pageno%pages==0)
    {
      bulkno+=1;
      pageno=(bulkno-1)*pages+1;
    }
    else pageno+=1;
  
    while(type=="old"&&nomore==false&&(pageno*count)>CurNotices.length)
    { updateOld();
      makeCurNotices();
    }   
    if(((pageno-1)*count)>=CurNotices.length)
       pageno-=1;
    shownotices();
  }
  if(str=="more")
  { 
    bulkno+=1;
    pageno=(bulkno-1)*pages+1;
    while(type=="old"&&nomore==false&&(pageno*count)>CurNotices.length)
    { updateOld();
      makeCurNotices();
    } 
    shownotices();
  }
}



//search through ajax and saves result in Search array
function search()
{
  field=document.getElementById("search_field"); 
  if(field.value=="")
     return false;
  advs=document.getElementsByName("adv");
  l=advs.length;
  var a=Array();
  
  for(i=0;i<l;i++)
     if(advs[i].checked)
        a.push(advs[i].value);
 
  xhr=getXHRObject();
  xhr.open("get","handle.cgi?action=search&expr="+field.value+"&adv="+a.join(),false);
  xhr.send();
  xml=parsetoXml(xhr.responseText)
  totalsearch=0;
  SearchNotices=new Array();
  
  if(xml.getElementsByTagName("status")[0].childNodes[0].nodeValue != "failure")
  {   totalsearch=eval(xml.getElementsByTagName("total")[0].childNodes[0].nodeValue);
      SearchNotices=xml.getElementsByTagName("notice");
  }
  type="search";
  catclicked('all','all');
  return false;
}


///////////////////////////////////////////////////////
/////these functions build category pop-down menus

var state_id=null,state=false,f=false,b=false,e=null;


function msover(elm)
{  
   if(state==false)
   {   
       elm.className="pref-act";
       state=true;
       state_id=elm.id;
       ppdshow(elm.id);
   }
   else if(state_id!=elm.id)
   {  
       document.getElementById(state_id).className="pref";
       elm.className="pref-act";
       state_id=elm.id;
       state=true;
       ppdhide();
       ppdshow(elm.id);
   }
   f=true;
   b=false;
   //alert("msover");
}
   

function msout(elm)
{  //alert("msout");
   e=elm;
   f=false; 
   setTimeout('if(b==false&&f==false){e.className="pref";state=false;state_id=null;ppdhide();}',50);
}


function Pmsover()  
{   //alert("pmsover");
    b=true;
    f=false;
}
   
   
function Pmsout()
{   
    b=false;
    setTimeout('if(f==false&&b==false){  elm=document.getElementById(state_id);try{elm.className="pref";}catch(e){}state_id=null;state=false;ppdhide();}',50);
}


function ppdshow(id)
{  
   var height,no;
   Cat=eval(id)
   if(Cat.length==1)
      no=1;
   else 
      no=Cat.length+1;
   rows=no/2;
   table="<table style='float:left;position:relative' width='100%'><colgroup span='2' width='50%'></colgroup><tbody>";
   if(no==1)
   {  
      table+="<tr><td><span class='subcat' onmouseover='this.className=\"subcat-over\"' onmouseout='this.className=\"subcat\"'"+
      "onclick='catclicked(\""+id+"\",\""+Cat[0].split(":")[0]+"\");Pmsout();'>"+Cat[0].split(":")[1]+"</span></td></tr>"
      rows=1;
      
   }
   else
   {
      table+="<tr><td><span  class='subcat' onmouseover='this.className=\"subcat-over\"' onmouseout='this.className=\"subcat\"'"+
             "onclick='catclicked(\""+id+"\",\"all\");Pmsout();'>All</span></td>"+
             "<td><span  class='subcat' onmouseover='this.className=\"subcat-over\"' onmouseout='this.className=\"subcat\"'"+
             "onclick='catclicked(\""+id+"\",\""+Cat[0].split(":")[0]+"\");Pmsout();'>"+Cat[0].split(":")[1]+"</span></td></tr>";
      
      for(i=1;i<rows;i++)
      { 
         table+="<tr><td><span  class='subcat' onmouseover='this.className=\"subcat-over\"' onmouseout='this.className=\"subcat\"'"+
                "onclick='catclicked(\""+id+"\",\""+Cat[2*i-1].split(":")[0]+"\");Pmsout();'>"+Cat[2*i-1].split(":")[1]+"</span></td>";
         if(2*i<Cat.length) 
             table+="<td><span  class='subcat' onmouseover='this.className=\"subcat-over\"' onmouseout='this.className=\"subcat\"'"+
                 "onclick='catclicked(\""+id+"\",\""+Cat[2*i].split(":")[0]+"\");Pmsout();'>"+Cat[2*i].split(":")[1]+"</span></td>";
         table+="</tr>\n";
      }
   } 
   table+="</tbody></table>";
   height=rows*22+14;
   ppd=document.getElementById("pref-pop-down");
   ppd.style.height=""+height+"px";
   ppd.innerHTML=table;
   ppd.onmouseout=Pmsout;
   //ppd.setAttribute("onmouseover","Pmsover();");
   ppd.onmouseover=Pmsover;
   //alert(ppd.getAttribute("onmouseover"));
   //ppd.onclick=Pmsout;
}
   
   
function ppdhide()
{ 
    ppd=document.getElementById("pref-pop-down");
    ppd.setAttribute("style","");
    ppd.innerHTML="";
    ppd.onmouseout = function(){}
    ppd.onmouseover = function(){}
    ppd.style.height=0;  
}
   
   
function prepare_cat()
{
    div=document.getElementById("cat");
    str=div.innerHTML;
    div.innerHTML="";
    div.innerHTML+='<div style="width:'+100/(Categories.length+1)+'%" class="pref" onmouseover="this.className=\'pref-act\'"'+
    'onmouseout="this.className=\'pref\'" onclick="'+(type=='search'?'type=\'new\';':'')+'catclicked(\'all\',\'\')">All</div>\n';
    
    for(i=0;i<Categories.length;i++)
    {  if(eval(Categories[i]).length==1)
         div.innerHTML+='<div style="width:'+100/(Categories.length+1)+'%" id="'+Categories[i]+
	                '" class="pref" onmouseover="this.className=\'pref-act\'"'+
	                'onmouseout="this.className=\'pref\'" onclick="catclicked(\''+Categories[i]+'\',\'all\')">'+Categories[i]+'</div>\n';
       else 
         div.innerHTML+='<div style="width:'+100/(Categories.length+1)+'%" id="'+Categories[i]+'"'+
                        ' class="pref" onmouseover="msover(this)" onmouseout="msout(this)" onclick="catclicked(\''+Categories[i]+'\',\'all\')" >'+
		        Categories[i]+'</div>\n';
    }
}

//////////////////////////////////////////////////////////////


//called when some category:subcategory is clicked
function catclicked(c,s)
{   prepare_cat();
    _cat = c;
    _subcat = s;
    pageno = 1;
    bulkno = 1;
    makeCurNotices();
    shownotices();
}   

//this function is called on index.cgi page at end 
function scriptend()
{
    prepare_cat();
    updateNew();
    pageno=1;
    bulkno=1;
    _cat="all";
    _subcat=null;
    type="new";
    makeCurNotices();    
    if(document.location.hash=="")
    {  clicked('New');
       if(open_notice_id!="")
         shownotice(open_notice_id);
    }
    else
      split_href(); 

    setInterval ("check_href()",100);
}

function check_href(){
    if (href.substr(1) != document.location.href.split('#')[1])
       split_href();
}
    
function split_href() {
  var url = document.location.href;
  var url_hash_parts = document.location.href.split('#');
  var url_parts = url_hash_parts[1].split('/');
  var url_type = url_parts[0];
  var url_cat = url_parts[1];
  var url_subcat = url_parts[2];
  var url_pageno = url_parts[3];
 
  prepare_cat();
  if (url_type == "content")
  { id = url_cat;
    shownotice(id);
  }
  else if (url_type == "new" || url_type =="old") 
  { _cat = url_cat;
    _subcat = url_subcat;
    pageno = parseInt(url_pageno);
    makeCurNotices();
    shownotices();
  }     
}

