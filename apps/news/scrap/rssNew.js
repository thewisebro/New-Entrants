var i=0;
var j=0;
var arr=new Array(3);
	 arr[0]="International";
	 arr[1]="National";
	 arr[2]="Sports";
var ch_arr=new Array(4);
	 ch_arr[0]="google_int";
	 ch_arr[1]="hindu_int";
	 ch_arr[2]="bbc_int";
	 ch_arr[3]="nyt_int";	 
var sports_arr=new Array(6);


function ajax_send(GP,URL,PARAMETERS,RESPONSEFUNCTION)
{
	var xmlhttp
	try{xmlhttp=new ActiveXObject("Msxml2.XMLHTTP")}
	catch(e){
	try{xmlhttp=new ActiveXObject("Microsoft.XMLHTTP")}
	catch(e){
	try{xmlhttp=new XMLHttpRequest()}
	catch(e){
		alert("Your Browser Does Not Support AJAX")}}} err=""
	if (GP==undefined) err="GP "
	if (URL==undefined) err +="URL "
	if (PARAMETERS==undefined) err+="PARAMETERS"
	if (err!=""){alert("Missing Identifier(s)\n\n"+err);return false;}

	xmlhttp.onreadystatechange=function(){
		if (xmlhttp.readyState == 4){
			if (RESPONSEFUNCTION=="") return false;
			eval(RESPONSEFUNCTION(xmlhttp.responseText));
			}
		}

	if (GP=="GET"){
		URL+="?"+PARAMETERS
		xmlhttp.open("GET",URL,true)
		xmlhttp.send(null)
	}

	if (GP="POST"){
		PARAMETERS=encodeURI(PARAMETERS)
		xmlhttp.open("POST",URL,true)
		xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
		xmlhttp.setRequestHeader("Content-length",PARAMETERS.length)
		xmlhttp.setRequestHeader("Connection", "close")
		xmlhttp.send(PARAMETERS)
	}
}

function left_arrow_click_row1()
{
	
	 //array size=3
	arr[0]="International";
	arr[1]="National";
	arr[2]="Sports";	
	
		i--;
		
		if(i<0)
		{
			i=2;
		}
			document.getElementById("types").innerHTML="<h3>"+arr[i]+"</h3>";

			if(arr[i]=="International")
				{
					document.getElementById("channels").innerHTML="<h3>google_int</h3>";
					document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
					var data="p="+arr[i]+"&q=google_int";
					ajax_send("GET","rss2.php",data,test);
				}
			if(arr[i]=="National")
				{
					document.getElementById("channels").innerHTML="<h3>google_nat</h3>";
					document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
					var data="p="+arr[i]+"&q=google_nat";
					ajax_send("GET","rss2.php",data,test);
				}
			if(arr[i]=="Sports")
				{
					document.getElementById("channels").innerHTML="<h3>cricket</h3>";
					document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
					var data="p="+arr[i]+"&q=cricket";
					ajax_send("GET","rss2.php",data,test);
				}
			
	
}
function right_arrow_click_row1()
{
	
	 //array size=3
	arr[0]="International";
	arr[1]="National";
	arr[2]="Sports";	
	
		i++;
		
		if(i>2)
		{
			i=0;
		}
			document.getElementById("types").innerHTML="<h3>"+arr[i]+"</h3>";
		

		if(arr[i]=="International")
			{
   				document.getElementById("channels").innerHTML="<h3>google_int</h3>";
				document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
				var data="p="+arr[i]+"&q=google_int";
				ajax_send("GET","rss2.php",data,test);
			}
		if(arr[i]=="National")
			{
				 document.getElementById("channels").innerHTML="<h3>google_nat</h3>";
				 document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
				 var data="p="+arr[i]+"&q=google_nat";
				 ajax_send("GET","rss2.php",data,test);
			}
		if(arr[i]=="Sports")
			{
				document.getElementById("channels").innerHTML="<h3>cricket</h3>";
				document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
				var data="p="+arr[i]+"&q=cricket";
				ajax_send("GET","rss2.php",data,test);
			}
}

function left_arrow_click_row2()
{	
		
	//var arr=new Array(4); //array size=3
	if(arr[i]=="International")
	{ch_arr[0]="google_int";
	 ch_arr[1]="hindu_int";
	 ch_arr[2]="bbc_int";
	 ch_arr[3]="nyt_int";
	 document.getElementById("channels").innerHTML="<h3>google_int</h3>";
	 }
	if(arr[i]=="National")
	{ch_arr[0]="google_nat";
	 ch_arr[1]="hindu_nat";
	 ch_arr[2]="toi_nat";
	 ch_arr[3]="ie_nat";}
	if(arr[i]=="Sports")
	{sports_arr[0]="cricket";
	 sports_arr[1]="hockey";
	 sports_arr[2]="football";
	 sports_arr[3]="tennis";
	 sports_arr[4]="badminton";
	 sports_arr[5]="chess";
	 }


	if(arr[i]!="Sports")	
	{
		j--;
		
		if(j<0)
		{
			j=3;
		}
				
			document.getElementById("channels").innerHTML="<h3>"+ch_arr[j]+"</h3>";
			document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
			var data="p="+arr[i]+"&q="+ch_arr[j];
			ajax_send("GET","rss2.php",data,test);
 	}	
	else
	{
		j--;
		
		if(j<0)
		{j=5;}
		
		document.getElementById("channels").innerHTML="<h3>"+sports_arr[j]+"</h3>";
		document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
		var data="p="+arr[i]+"&q="+sports_arr[j];
		ajax_send("GET","rss2.php",data,test);
	}
	
}

function right_arrow_click_row2()
{	
		
	//var arr=new Array(4); //array size=3
	if(arr[i]=="International")
	{ch_arr[0]="google_int";
	 ch_arr[1]="hindu_int";
	 ch_arr[2]="bbc_int";
	 ch_arr[3]="nyt_int";
	 document.getElementById("channels").innerHTML="<h3>google_int</h3>";
	 }
	if(arr[i]=="National")
	{ch_arr[0]="google_nat";
	 ch_arr[1]="hindu_nat";
	 ch_arr[2]="toi_nat";
	 ch_arr[3]="ie_nat";}
	if(arr[i]=="Sports")
	{sports_arr[0]="cricket";
	 sports_arr[1]="hockey";
	 sports_arr[2]="football";
	 sports_arr[3]="tennis";
	 sports_arr[4]="badminton";
	 sports_arr[5]="chess";
	 }


	if(arr[i]!="Sports")	
	{
		j++;
		
		if(j>3)
		{
			j=0;
		}
				
			document.getElementById("channels").innerHTML="<h3>"+ch_arr[j]+"</h3>";
			document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
			var data="p="+arr[i]+"&q="+ch_arr[j];
			ajax_send("GET","rss2.php",data,test);
 	}		
	else
	{
		j++;

		if(j>5)
		{j=0;}

		document.getElementById("channels").innerHTML="<h3>"+sports_arr[j]+"</h3>";
		document.getElementById("data").innerHTML="<img src='loading.gif' style='width:350px;height:350px;'>";
		var data="p="+arr[i]+"&q="+sports_arr[j];
		ajax_send("GET","rss2.php",data,test);
	}
}

function test(str)
{
	document.getElementById("data").innerHTML=str;	
}
