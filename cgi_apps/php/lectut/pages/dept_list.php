<div class="ss" id="browse_by_department_goto">
			<div id="bbdl"></div> 	
<?php
if($loggedIn!=0)
{
		echo "<a href=\"javascript:func1('#main_goto');\"><div id=\"bbdr_container\"><div id=\"bbdr\"></div></div></a>";
}
else
{
		echo "<a href=\"javascript:func1('#browse_by_department_goto');\"><div id=\"bbdr_container\"><div id=\"bbdr\"></div></div></a>";
}
?>	
				<div id="browse_by_department" >
<?php
/*
if($loggedIn==0)
{
			echo "<a href=\"\">";
}
else
{
			echo "<a href=\"javascript:func1('#main_goto');\">";
}
*/
if($loggedIn)
{
if($_SESSION['group']=='s')
{
	echo "		<div  id=\"browse_by_department_back\">
				<!--[if !(IE 6)]><!-->
				<a href=\"javascript:func1('#main_goto');\">
				<!--<![endif]-->
				<!--[if IE 6]>
				<a href=\"javascript:ie_func1('#main_goto')\">
				<![endif]-->
			<div  id=\"browse_by_department_main_link\" >
				<div class=\"my_courses_back_link space\" >back&nbsp;to&nbsp;main&nbsp;page</div>
			</div>
			</a>
				<!--[if !(IE 6)]><!-->
					<a href=\"javascript:func1('#my_courses_goto');\">
				<!--<![endif]-->
				<!--[if IE 6]>
						<a href=\"javascript:ie_func1('#my_courses_goto')\">
				<![endif]-->

<!--<a href=\"javascript:func1('#my_courses');\">--> 
			

			<div id=\"browse_by_department_mc_back\">
				<div class=\"my_courses_bbd_back_link space\" >My&nbsp;courses</div>
			</div>
			</a>
			</div>";
}
else
{
	echo "
			<div  id=\"browse_by_department_back\">
				<a href=\"final_prof.php\">
			<div  id=\"browse_by_department_main_link\" >
				<div class=\"my_courses_back_link space\" >back&nbsp;to&nbsp;main&nbsp;page</div>
			</div>
			</a>
			<a href=\"final_prof.php?temp2=b\"> 
			<div id=\"browse_by_department_mc_back\">
				<div class=\"my_courses_bbd_back_link space\" >My&nbsp;courses</div>
			</div>
			</a>
			</div>";
}
	
echo "			";

}
else
{
echo "<a href=\"index.php\">";

echo "			<div  id=\"browse_by_department_back\">
				<a href=\"index.php\">
			<div  id=\"browse_by_department_main_link\" >
				<div class=\"my_courses_back_link space\" >back&nbsp;to&nbsp;main&nbsp;page</div>
			</div>
			</a>
			<a href=\"index.php\"> 
			<div id=\"browse_by_department_mc_back_dummy\">
				<div class=\"my_courses_bbd_back_link space\" ></div>
			</div>
			</a>
			</div>
			<script>
			if($.browser.msie)
			{
				$('#browse_by_department_back').css('width','auto');
				$('#browse_by_department_main_link').css('width',71);
				$('#browse_by_department_mc_back_dummy').css('width',71);
			}
			</script>
			
			";

}

?>
			</a>
			<div id="browse_by_department_page_container">
				<form name="download" action="download.php" method="post" onsubmit="return validate_form();">
				<div id="browse_by_department_topbar">
					<div id="browse_by_department_logout_button" >

<?php
	if($loggedIn==0)
	{
		echo "<a href=\"index.php\">LOGIN</a>";
	}
	else
	{
		echo "<a href=\"/nucleus/logout\">LOGOUT</a>";
	}	
?>	
					</div>
					<div id="browse_by_department_title">
						BROWSE BY DEPARTMENT
					</div>
          <div id="prof_name_bbd"></div>
				</div>
				<div id="browse_by_department_selection">
					<a href="javascript:func22('_lectures','#browse_by_department_files','#browse_by_department_lectures_link');"  id="browse_by_department_lectures_link" class="browse_by_department_selection_link browse_by_department_inactive_link browse_by_department_link">LECTURES</a>
					<a href="javascript:func22('_tutorials','#browse_by_department_files','#browse_by_department_tutorials_link');"  id="browse_by_department_tutorials_link" class="browse_by_department_selection_link browse_by_department_inactive_link browse_by_department_link">TUTORIALS</a>
					<a href="javascript:func22('_exam_papers','#browse_by_department_files','#browse_by_department_exam_papers_link');"  id="browse_by_department_exam_papers_link" class="browse_by_department_selection_link browse_by_department_inactive_link browse_by_department_link">EXAM PAPERS</a>
					<a href="javascript:func22('_solutions','#browse_by_department_files','#browse_by_department_solutions_link');"  id="browse_by_department_solutions_link" class="browse_by_department_selection_link browse_by_department_inactive_link browse_by_department_link">SOLUTIONS</a>
					<a href="javascript:func22('_all','#browse_by_department_files','#browse_by_department_all_link');"  id="browse_by_department_all_link" class="browse_by_department_selection_link browse_by_department_inactive_link browse_by_department_link">ALL</a>
				</div>

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
		{$result2=database::getDeptList($row[0]);
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
		{$result2=database::getDeptList($row[0]);
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

<!-- The go back link put here -->

				<div id="go_back_container" style="font-size:20px"><a id="go_back" href="javascript:go_back();">go back</a></div>
<!-- Content tabs start here.... -->			

				<div id="dept_tab_container" class ="scrolled_tiny">
					<div class="scrollbarer">
					
					<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
<!-- this set and not overview as this is the relatively outermost container div  -->
				<div class="viewport" id="scroll_dept_target">
			 <div class="overview" >




					<div id="dept_tab">
						<div id="dept_list">
<?php

$i=1;
foreach($dep_key as $dept)
{

echo '<script type="text/javascript">';
echo 'var dep'.$i.' = new Array("', join($dep_code[$dept],'","'), '");';
echo '</script>';

?>		
	<a href="javascript:dept_goto('#<? $dept1=str_replace(" ","",secure($dept));  echo $dept1; ?>',dep<? echo $i.",'",$dept1; ?>');"> <div class="dept_name"><? echo $dept; ?></div> </a>	
<?php
$i++;
}

?>



						</div>
						<div id="browse_by_department_course_selection"></div>
					</div>
				</div>
				</div>
				</div>
				</div>
				<div id="details_tab_container">

				<div class="scrollbarer" id="prof_f_t">
					

					
					<div class="scrollbar" ><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
		<div class="viewport" id="scroll_prof_target">




					<div id="details_tab" class="overview" style="">
						<div id="profs_container">
							<div id="profs">
						
<?php
/*
foreach($dep_key as $dept)
{
	foreach($dep_code[$dept] as $fac_id)
	{
		$result=database::executeQuery("facapp",database::getFacName($fac_id));
		if($result)
		{
			$facName=pg_fetch_array($result);
?>	
			<a href="javascript:prof_goto('#browse_by_department_course_selection','<? echo $fac_id; ?>','<? echo $facName[0]; ?>');" class="profs_dept prof_active"><div id="<? $dept1=str_replace(" ","",secure($dept)); echo $dept1; ?>"><? echo $facName[0]; ?></div></a>
<?
		}
	}
}*/
?>			
							</div>
						</div>
					
						<div id="browse_by_department_files" >
							<div id="subjects" class="subjects_bbd"></div>
						</div>

			
					</div>
				</div>
				</div>
				</div>
				<!--	<input type="button" name="CheckAll" value="Check All" onClick="checkAll(<?// echo "$l,$t,$e,$s"; ?>)">
				<input type="button" name="UnCheckAll" value="Uncheck All" onClick="uncheckAll(<?// echo "$l,$t,$e,$s"; ?>)">--><br>
				
				<div style="margin-top:20px;">
				<input type="submit" value="Download" class ="download_button" style="position:relative;top:-1px;">
				<a id="search_box_link_" href="javascript:s();">
				<div id = "search_link_main">Search</div><div id="go_back_check" style="width:0px;height:0px;"></div>
				</a>
				</div>
				
				</form>
				
			</div>
		</div>
		</div>
<?php

database::closeDatabase();

?>
