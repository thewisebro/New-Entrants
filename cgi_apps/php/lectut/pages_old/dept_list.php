<?php

//session_start();
include_once("../common/functions.php");
include("../../session/django_session.php");
$session = new Session();
$loggedIn=false;

//if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
//{
if($session->isloggedin()){	
  if($_SESSION['group']=='s')	
		$studId=$_SESSION['lectut_userid'];
	if($_SESSION['group']=='f')
		$facId=$_SESSION['lectut_userid'];
	$loggedIn=true;
}
else
{
	$loggedIn=false;
}

?>

<html>
<head>
<title>Lectures and Tutorials</title>

<link rel=stylesheet href="../styles_old/lectntut.css" type="text/css">
	<script src="../common/jscriptfunc.js"></script>


</head>

<body>
<div id="container">
	<div id="top_links">
<?

if($loggedIn && $_SESSION['group']=='f')
{
	disp_fac_design_choice($loggedIn,$facId);
}

if($loggedIn && $_SESSION['group']=='f')
{
	disp_fac_upload($loggedIn,$facId);
}
?>
	
		<div class="curve_edge_lt">&nbsp;</div>
		<div class="link"><a href="mailto:img@iitr.ernet.in">Complaints/Suggestions</a></div>
		<div class="curve_edge_rt">&nbsp;</div>
		<div class="curve_edge_lt"></div>
		<div class="link"><a href="/" target="_blank">Channel I</a></div>
		<div class="curve_edge_rt"></div>
<?
if($loggedIn && $_SESSION['group']=='f')
{
	disp_fac_logout($loggedIn,$facId);
}
?>

	</div>
	<!---Top Links div end here-->

	<div id="header_search">
		<div id="header">&nbsp;</div>
		<div id="search_bar">
			<div id="search_curve_lt">&nbsp;</div>
			<div id="search">
			<form action="search.php" method="post">
			
			<input type="text" id="search_box" name="search" />
			<input type="image" src="../styles_old/images/search.gif" id="search_button">
			</form></div>

			<div id="search_curve_rt">&nbsp;</div>
			
		</div>
	</div>
		

	<!--Header ends here-->
	<br />
	<div id="main_body">
		<div id="left_list">
		

	  <div id="left_list_top">
		<b>  </b>&nbsp;&nbsp;&nbsp; 
		<a href="javascript:window.location.reload(false);">Refresh</a> | 
		<a href="index.php" class="fieldtext">Home</a>
	
	</div>

	<div id="left_list_header">
		Department List	
	</div>
	
			<table id="result">
	
<?php
$dep_code=array();
database::connectToDatabase();
$result_l=database::executeQuery(database::getDistinctId(FACULTY_ID,LEC_TABLE,NULL));
$result_t=database::executeQuery(database::getDistinctId(FACULTY_ID,TUT_TABLE,NULL));
$result_e=database::executeQuery(database::getDistinctId(FACULTY_ID,EXAM_TABLE,NULL));
$result_s=database::executeQuery(database::getDistinctId(FACULTY_ID,SOLN_TABLE,NULL));

if($result_l)
{
	while($row=mysql_fetch_array($result_l))
	{
		if($row[0]!="")
		{
			$result2=database::getDeptList($row[0]);
      if($result2)
			{
				if(!array_key_exists($result2,$dep_code))
				{
					$dep_code[$result2]=array();
				}
				array_push($dep_code[$result2],$row[0]);
			}
		}
	}
}

if($result_t)
{
	while($row=mysql_fetch_row($result_t))
	{
		if($row[0]!="")
		{
			$result2=database::getDeptList($row[0]);
			if($result2)
			{
				if(!array_key_exists($result2,$dep_code))
				{
					$dep_code[$result2]=array();
				}
				array_push($dep_code[$result2],$row[0]);
			}
		}
	}
}

if($result_e)
{
	while($row=mysql_fetch_row($result_e))
	{
		if($row[0]!="")
		{
			$result2=database::getDeptList($row[0]);
			if($result2)
			{
				if(!array_key_exists($result2,$dep_code))
				{
					$dep_code[$result2]=array();
				}
				array_push($dep_code[$result2],$row[0]);
			}
		}
	}
}

if($result_s)
{
	while($row=mysql_fetch_row($result_s))
	{
		if($row[0]!="")
		{
			$result2=database::getDeptList($row[0]);
			if($result2)
			{
				if(!array_key_exists($result2,$dep_code))
				{
					$dep_code[$result2]=array();
				}
				array_push($dep_code[$result2],$row[0]);
			}
		}
	}
}

$dep_key=array_keys($dep_code);
foreach($dep_key as $dept)
{
	$dep_code[$dept]=array_unique($dep_code[$dept]);
	asort($dep_code[$dept]);
}
asort($dep_key);
?>

<tr><td>&nbsp;</td><td>&nbsp;</td><td width="100px"><div id="expandAll"><a style="text-decoration:underline; cursor:hand; cursor:pointer" onclick=expand()>Expand All</a></div> <div  id="collapseAll" style="display:none"><a style="text-decoration:underline;cursor:hand; cursor:pointer" onclick=collapse()>Collapse All</a></div></td></tr>

<?php

$i=1;
foreach($dep_key as $dept)
{
	$dept1=str_replace(" ","",secure($dept)); 
?>

<tr>


<td id="serial_no"><? echo $i; ?></td>

	<td id="download">
<div id="<?echo $dept1; ?>" class="dept_name" > 
	<a onclick="showhide('expand<?echo $i-1;?>')"><?echo $dept; ?></a>
</div>

    <div id="expand<? echo $i-1; ?>" style="display:none" >

<ul id="fac_name_list" >

<?php
	foreach($dep_code[$dept] as $facUsername)
	{
    $fac_id=mysql_fetch_array(database::executeQuery(database::getFacUserId($facUsername)));
		$result=database::executeQuery(database::getFacName($fac_id[0]));
		if($result)
		{
			$facName=mysql_fetch_array($result);
?>
<li><a href="courses_prof.php?id=<?echo $facUsername;?>&name=<?echo $facName[0];?>" ><?echo $facName[0];?></a></li>
<?php
		}
	}

?>
</ul></div>
</td>

</tr>

<?php
$i++;
}

database::closeDatabase();
?>

</table>

		</div>

		<div id="rght_text">
			<div id="top_rt_text">Please click on the department name to get the list of professors</div>
			<!--<div id="right_shadow">&nbsp;</div>
			<div id="bottom_shadow">&nbsp;</div>-->
			<div id="bottom_block">Once you click on a link you can:<br/><br/>
				<ul id="list_students">
						<li> Download the documents by selecting the course and clicking download link or right-clicking on the 						download link and selecting <b>save target as</b> or <b>save link as</b> depending on 							your browser. 
				</ul>
			</div>
		</div>
		
	</div>


	
</div>

	<div id="footer">
			<div id="footer_text">
			<div id="bottom_curve_lt">&nbsp;</div>
			<div id="img">Credits: <a href="http://www.iitr.ernet.in/campus_life/pages/Groups_and_Societies+IMG.html" target="_blank">Information Management Group</a></div>
			
			<div id="bottom_curve_rt">&nbsp;&nbsp;</div>
			</div>
		</div>

<!--Footer ends here-->	
<script>
function expand()
{
      <? 
        for($i=0;$i<count($dep_code);$i++) { ?>
        	if(document.getElementById("expand<?echo $i;?>").style.display=="none")
	        {
		        document.getElementById("expand<?echo $i;?>").style.display="inline";		
	        }
<?	} ?>
       document.getElementById("expandAll").style.display="none";
       document.getElementById("collapseAll").style.display="inline";

}
function collapse()
{
      <? 
        for($i=0;$i<count($dep_code);$i++) { ?>
        	if(document.getElementById("expand<?echo $i;?>").style.display=="inline")
	        {
		        document.getElementById("expand<?echo $i;?>").style.display="none";		
	        }
<?	} ?>
      
      document.getElementById("collapseAll").style.display="none";
       document.getElementById("expandAll").style.display="inline";
}
function showhide(div_id)
{
	if(document.getElementById(div_id).style.display=="none")
	{
	     <?for($i=0;$i<count($dep_code);$i++) { ?>
	        document.getElementById("expand<?echo $i;?>").style.display="none";
	     <?}?>
		document.getElementById(div_id).style.display="inline";		
	}
	else
	{
		document.getElementById(div_id).style.display="none";
	}

 
}

</script>
<script type="text/javascript" src="/static/js/piwik.js"><script>
</body>
</html>

