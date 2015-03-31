<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<?php
//session_start();

include_once("../common/functions.php");
include("../../session/django_session.php");
$session = new Session();

//if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
//{
if($session->isloggedin()){	
  if($_SESSION['group']=='s')	
		$studId=$_SESSION['lectut_userid'];
	if($_SESSION['group']==0)
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

	<div class="curve_edge_lt">&nbsp;</div>
	<div class="link"><a href="mailto:img@iitr.ernet.in" target="_blank">Complaints/Suggestions</a></div>
	<div class="curve_edge_rt">&nbsp;</div>
	<div class="curve_edge_lt"></div>
	<div class="link"><a href="/" target="_blank">Channel I</a></div>
	<div class="curve_edge_rt"></div>
</div>
<!---Top Links div end here-->

<div id="header_search">
   <div id="header">&nbsp;</div>
	<div id="search_bar">
		<div id="search_curve_lt">&nbsp;</div>
		<div id="search">
		<form action="search.php" method="post">
			
			<input type="text" id="search_box"  name="search"/>
			<input type="image" src="../styles_old/images/search.gif" id="search_button">
			</form></div>

			<div id="search_curve_rt">&nbsp;</div>
			
		</div>
	</div>
		

	<!--Header ends here-->
	<br />
	<div id="main_body">

	<div id="leftbox" style="margin-top:30px;">
           <div id="left_list_top">
		<a href="index.php" class="fieldtext">Home</a>
	   </div>
<?php
$search=filter_input(INPUT_POST,'search',FILTER_SANITIZE_STRING);
$search=secure($search);

$len=strlen($search);

if($len<2)
{
	echo "Search string should be atleast 3 characters long or department code.";
}
else
{

database::connectToDatabase();

if(isset($studId))
{
	$reg_courses=database::executeQuery(database::studQuery($studId));
}
$time1=microtime(true);
$results_lec = search_perform($search,"lec");
$results_tut = search_perform($search,"tut");
$results_exam = search_perform($search,"exam");
$results_soln = search_perform($search,"soln");
$time2=microtime(true);
$time=$time2-$time1;
$time=round($time,3);

}
?>

			<div id="left_list_header">
			<?php echo "$search ($time seconds)"; ?>
				</div>
				<table id="result">

	<tr><td style="width:20px">&nbsp;</td><td colspan="2"><b>Lectures</b></td></tr>	

<?php
$i=count($results_lec);
$count=0;
foreach($results_lec as $result)
{       
	if($result[0]->getPermission()==0 || in_array($result[0]->getCourseId(),$reg_courses) || $facId==$result[0]->getFacultyId())
	{
		$count++;
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result[0]->getFacultyId())));

?>

<tr>
					<td><?echo $count;?></td>
					<td><?echo $facName[0];//faculty name?></td>
					<td class="subject"><?echo $result[0]->getCourseId();//subject_code?></td>
					<td id="download"><a href="<? echo LECDIR."/".$result[0]->getFacultyId()."/".$result[0]->getFile(); ?>"><? echo $result[0]->getTopic(); ?></a></td>
					</tr>


<?php   
	}
}       
if($count==0)
{
echo "<tr><td>&nbsp;</td><td colspan=\"2\">No lectures found.</td></tr>";
}       
?>
                  <tr><td>&nbsp;</td></tr> 

	<tr><td style="width:20px">&nbsp;</td><td colspan="2"><b>Tutorials</b></td></tr>	

<?php
$i=count($results_tut);
$count=0;
foreach($results_tut as $result)
{       
	if($result[0]->getPermission()==0 || in_array($result[0]->getCourseId(),$reg_courses) || $facId==$result[0]->getFacultyId())
	{
		$count++;
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result[0]->getFacultyId())));

?>

<tr>
					<td><?echo $count;?></td>
					<td><?echo $facName[0];//faculty name?></td>
					<td class="subject"><?echo $result[0]->getCourseId();//subject_code?></td>
					<td id="download"><a href="<? echo TUTDIR."/".$result[0]->getFacultyId()."/".$result[0]->getFile(); ?>"><? echo $result[0]->getTopic(); ?></a></td>
					</tr>


<?php   
	}       
}       
if($count==0)
{
echo "<tr><td>&nbsp;</td><td colspan=\"2\">No tutorials found.</td></tr>";
}       
?>
	                  <tr><td>&nbsp;</td></tr> 
<tr><td style="width:20px">&nbsp;</td><td colspan="2"><b>Exam Papers</b></td></tr>	

<?php
$i=count($results_exam);
$count=0;
foreach($results_exam as $result)
{       
	if($result[0]->getPermission()==0 || in_array($result[0]->getCourseId(),$reg_courses) || $facId==$result[0]->getFacultyId())
	{
		$count++;
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result[0]->getFacultyId())));

?>

<tr>
					<td><?echo $count;?></td>
					<td><?echo $facName[0];//faculty name?></td>
					<td class="subject"><?echo $result[0]->getCourseId();//subject_code?></td>
					<td id="download"><a href="<? echo EXAMDIR."/".$result[0]->getFacultyId()."/".$result[0]->getFile(); ?>"><? echo $result[0]->getTopic(); ?></a></td>
					</tr>


<?php   
	}       
}       
if($count==0)
{
echo "<tr><td>&nbsp;</td><td colspan=\"2\">No exam papers found.</td></tr>";
}       
?>
                  <tr><td>&nbsp;</td></tr> 

	<tr><td style="width:20px">&nbsp;</td><td colspan="2"><b>Solutions</b></td></tr>	

<?php
$i=count($results_soln);
$count=0;
foreach($results_soln as $result)
{       
	if($result[0]->getPermission()==0 || in_array($result[0]->getCourseId(),$reg_courses) || $facId==$result[0]->getFacultyId())
	{
		$count++;
		$facName=mysql_fetch_array(database::executeQuery(database::getFacName($result[0]->getFacultyId())));

?>

<tr>
					<td><?echo $count;?></td>
					<td><?echo $facName[0];//faculty name?></td>
					<td class="subject"><?echo $result[0]->getCourseId();//subject_code?></td>
					<td id="download"><a href="<? echo SOLNDIR."/".$result[0]->getFacultyId()."/".$result[0]->getFile(); ?>"><? echo $result[0]->getTopic(); ?></a></td>
					</tr>


<?php   
	}       
}       
if($count==0)
{
echo "<tr><td>&nbsp;</td><td colspan=\"2\">No solutions found.</td></tr>";
}      
?>
	</table>

	</div> <!--// leftbox ends.-->
	<div id="rght_text">
		<div id="top_rt_text">The following lectures and tutorials matched your query.</div>
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

<script type="text/javascript" src="/static/js/piwik.js"></script>
</body>
</html>

<?php

database::closeDatabase();

?>
