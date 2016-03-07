<?php

//session_start();

include_once("../common/functions.php");
include("../../session/django_session.php");

$session = New Session();

if($_SESSION['group']=='s')	
	$studId=$_SESSION['lectut_userid'];
if($_SESSION['group']=='f')
	$facId=$_SESSION['lectut_userid'];

$id=$_GET['id'];
$name=$_GET['name'];

$facUsername=$_SESSION['lectut_username'];

database::connectToDatabase();
if(isset($studId))
{
	$reg_courses=database::executeQuery(database::studQuery($studId));
}
$result_l=database::executeQuery(database::getDistinctId(COURSE_ID,LEC_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_t=database::executeQuery(database::getDistinctId(COURSE_ID,TUT_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_e=database::executeQuery(database::getDistinctId(COURSE_ID,EXAM_TABLE,"WHERE ".FACULTY_ID."='$id'"));
$result_s=database::executeQuery(database::getDistinctId(COURSE_ID,SOLN_TABLE,"WHERE ".FACULTY_ID."='$id'"));
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

if($_SESSION['group']==0)
{
	disp_fac_design_choice($loggedIn,$facId);
}

if($_SESSION['group']==0)
{
	disp_fac_upload($loggedIn,$facId);
}

?>
		<div class="curve_edge_lt">&nbsp;</div>
		<div class="link"><a href="mailto:img@iitr.ernet.in">Complaints/Suggestions</a></div>
		<div class="curve_edge_rt">&nbsp;</div>
		<div class="curve_edge_lt">&nbsp;</div>
		<div class="link"><a href="/" target="_blank">Channel I</a></div>
		<div class="curve_edge_rt">&nbsp;</div>
<?
if($_SESSION['group']==0)
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
		<b>  </b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<a href="javascript:window.location.reload(false);">Refresh</a> | 
                <a href="dept_list.php"  class="fieldtext">Back</a>

	   </div>

	<div id="left_list_header">
		<?
				echo $name;
		?>
	</div>

<table id="result">

<tr><td>&nbsp;</td><td>&nbsp;</td><td style="width:120px"><div id="expandAll"><a style="text-decoration:underline; cursor:hand; cursor:pointer" onclick=expand()>Expand All</a></div> <div  id="collapseAll" style="display:none"><a style="text-decoration:underline;cursor:hand; cursor:pointer" onclick=collapse()>Collapse All</a></div></td></tr>

<!--Lectures begin-->

	<tr><td style="width:20px">&nbsp;</td><td><b>Lecture List</b></td></tr>	
	
<?php
$l=0; 
while($row=mysql_fetch_row($result_l))
{
	if($row[0]!="")
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);
		if($row1[0]==null)
		{
			$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=mysql_fetch_row($result1);			
		}
?>
							<tr>

							<td id="serial_no" style="width:20px"><? echo $l+1;?> </td>

							<td id="download" width="500px">
							<div class="dept_name" id="list<?echo $l;?>"><a onclick="showhide(<?echo $l;?>)"><?echo $row[0]." - ".$row1[0]; ?></a></div>


							<div id="<?echo $l;?>" style="display:none">
							<ul id="fac_name_list">   


<?php
		$i=0;

		$return_lec=database::getLecObject("COURSE_ID",$row[0],null);

		foreach($return_lec as $result)
		{
			if($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id)
			{

								$i++;
								?>

									<li><a href="<? echo LECDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>" target ="main"><? echo $result->getTopic(); ?></a></li>
									<?
			}
		}
		if($i==0)
		{
			echo "No lectures.";
		}
	?>
							</ul> </div></td>
							</tr>

							<?
							$l++;

	}
}
if($l==0)
{
?>
		<tr><td style="width:20px">&nbsp;</td><td colspan="2">No Lectures.</td></tr>	
<?php
}
?>
				</table>

						<!--Lectures end-->


<!--Tutorials begin-->

	<table id="result">
                  <tr><td>&nbsp;</td></tr> 
	          <tr><td>&nbsp;</td><td><b>Tutorial List</b></td></tr>	
 

<?php
$t=0;
while($row=mysql_fetch_row($result_t))
{
	if($row[0]!="")
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);
		if($row1[0]==null)
		{
			$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=mysql_fetch_row($result1);			
		}
					?>
						<tr>

						<td id="serial_no" style="width:20px"><? echo $l+1;?> </td>

						<td id="download" width="500px">
						<div class="dept_name" id="list<?echo $l;?>"><a onclick="showhide(<?echo $l;?>)"><?echo $row[0]." - ".$row1[0]; ?></a></div>


						<div id="<?echo $l;?>" style="display:none">
						<ul id="fac_name_list">   
						<?php


					$i=0;
		$return_lec=database::getTutObject("COURSE_ID",$row[0],null);
		foreach($return_lec as $result)
		{
			if($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id)
			{
							$i++;
							?>

								<li><a href="<? echo TUTDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>" target ="main"><? echo $result->getTopic(); ?></a></li>
								<?
					
			}
		}
					if($i==0)
					{
						echo "No tutorials.";
					}

					?>
						</ul> </div></td>
						</tr>

						<?
						$l++;
					$t++;


	}

}
if($t==0)
{
?>
		<tr><td style="width:20px">&nbsp;</td><td colspan="2">No Tutorials.</td></tr>	
<?php
}
?>
</table>

<!--Tutorials end-->


<!--Exam Papers begin-->
	<table id="result">
                  <tr><td>&nbsp;</td></tr> 
	          <tr><td>&nbsp;</td><td><b>Exam Paper List</b></td></tr>	



<?php
$e=0;
while($row=mysql_fetch_row($result_e))
{
	if($row[0]!="")
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);
		if($row1[0]==null)
		{
			$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=mysql_fetch_row($result1);			
		}
?>
	<tr>

	<td id="serial_no" style="width:20px"><? echo $l+1;?> </td>

	<td id="download" width="500px">
	<div class="dept_name" id="list<?echo $l;?>"><a onclick="showhide(<?echo $l;?>)"><?echo $row[0]." - ".$row1[0]; ?></a></div>


	<div id="<?echo $l;?>" style="display:none">
	<ul id="fac_name_list">   

<?php
		$return_lec=database::getExamPaperObject("COURSE_ID",$row[0],null);
		$i=0;
		foreach($return_lec as $result)
		{
			if($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id)
			{
						$i++;
						?>

							<li><a href="<? echo EXAMDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>" target ="main"><? echo $result->getTopic(); ?></a></li>
<?php	
     			}
		}
			if($i==0)
				{
					echo "No exam papers.";
				}
?>
</ul> </div></td>
</tr>
<?php
		$e++;
		$l++;

	}	
}
if($e==0)
{
?>
		<tr><td style="width:20px">&nbsp;</td><td colspan="2">No Exam papers.</td></tr>	
<?php
}

?>

	</table>

<!--Exam Papers end-->

<!--Solutions begin-->
	<table id="result">
                  <tr><td>&nbsp;</td></tr> 
	          <tr><td>&nbsp;</td><td><b>Solution List</b></td></tr>	
 
<?php
$s=0;
while($row=mysql_fetch_row($result_s))
{
	if($row[0]!="")
	{
		$result1=database::executeQuery(database::getColumn(COURSE_NAME,COURSE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
		$row1=mysql_fetch_row($result1);
		if($row1[0]==null)
		{
			$result1=database::executeQuery(database::getColumn(COURSE_NAME,ELECTIVE_DETAILS,"WHERE ".COURSE_CODE."='$row[0]'"));
			$row1=mysql_fetch_row($result1);			
		}
?>
<tr>

<td id="serial_no" style="width:20px"><? echo $l+1;?> </td>

	<td id="download" width="500px">
	<div class="dept_name" id="list<?echo $l;?>"><a onclick="showhide(<?echo $l;?>)"><?echo $row[0]." - ".$row1[0]; ?></a></div>
	
       
      <div id="<?echo $l;?>" style="display:none">
     <ul id="fac_name_list">   

<?php
		$return_lec=database::getSolnObject("COURSE_ID",$row[0],null);
		$i=0;
		foreach($return_lec as $result)
		{
			if($result->getPermission()==0 || in_array($result->getCourseId(),$reg_courses) || $facUsername==$id)
			{
				$i++;
?>

			<li><a href="<? echo SOLNDIR; ?>/<? echo $id; ?>/<? echo $result->getFile(); ?>" target ="main"><? echo $result->getTopic(); ?></a></li>
<?

			}
		}
		if($i==0)
		{
			echo "No solutions.";
		}
?>
	     </ul> </div></td>
	</tr>

<?
	$l++;
	$s++;

	}
}
if($s==0)
{
?>
		<tr><td style="width:20px">&nbsp;</td><td colspan="2">No Solutions.</td></tr>	
<?php
}


$total=$l;
?>
	</table>
<!--Solutions end-->

		</div>

		<div id="rght_text">
			<div id="top_rt_text">Please click on a link to get a list of lectures</div>
			<!--<div id="right_shadow">&nbsp;</div>
			<div id="bottom_shadow">&nbsp;</div>-->
			<div id="bottom_block">Once you click on a link you can:<br/><br/>
				<ul id="list_students">
					<li> Download the documents by clicking download link or right-clicking on the 						download link and selecting <b>save target as</b> or <b>save link as</b> depending on 							your browser. 
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
        for($i=0;$i<$total;$i++) { ?>
        	if(document.getElementById("<?echo $i;?>").style.display=="none")
	        {
		        document.getElementById("<?echo $i;?>").style.display="inline";
			document.getElementById("list<?echo $i?>").style.fontWeight="bold";
	        }
<?	} ?>
      
       document.getElementById("expandAll").style.display="none";
       document.getElementById("collapseAll").style.display="inline";


}
function collapse()
{
      <? 
        for($i=0;$i<$total;$i++) { ?>
        	if(document.getElementById("<?echo $i;?>").style.display=="inline")
	        {
		        document.getElementById("<?echo $i;?>").style.display="none";	
                        document.getElementById("list<?echo $i?>").style.fontWeight="normal";

	        }
<?	} ?>
      document.getElementById("collapseAll").style.display="none";
       document.getElementById("expandAll").style.display="inline";

}
function showhide(div_id)
{
	if(document.getElementById(div_id).style.display=="none")
	{
	     <?for($i=0;$i<$total;$i++) { ?>
	        document.getElementById("<?echo $i;?>").style.display="none";
       	        document.getElementById("list<?echo $i?>").style.fontWeight="normal";
	     <?}?>
		document.getElementById(div_id).style.display="inline";	
		document.getElementById("list"+div_id).style.fontWeight="bold";
	}
	else
	{
		document.getElementById(div_id).style.display="none";
        	document.getElementById("list"+div_id).style.fontWeight="normal";
	}

 
}


</script>

<script type="text/javascript" src="/static/js/piwik.js"></script>
</body>
</html>


<?php
database::closeDatabase("intranet");
database::closeDatabase("regol");
?>

