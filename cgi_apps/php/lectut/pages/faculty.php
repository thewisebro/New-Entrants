<div class="ss" id="browse_by_department_goto">
	<div id="bbdl"></div> 
	<a href="javascript:func1('#main_goto');"><div id="bbdr_container"><div id="bbdr"></div></div></a>
	<div id="browse_by_department" >
		<div  id="upload_back">
			<!--[if !(IE 6)]><!-->
			<a href="javascript:func1('#main_goto');">
			<!--<![endif]-->
			<!--[if IE 6]>
			<a href="javascript:ie_func1('#main_goto');">
			<![endif]-->
			<div  id="browse_by_department_main_link" >
				<div class="my_courses_back_link space" >back&nbsp;to&nbsp;main&nbsp;page</div>
			</div>
			</a>
			<!--[if !(IE 6)]><!-->
			<a href="javascript:func1('#my_courses_goto');"> 
			<!--<![endif]-->
			<!--[if IE 6]>
			<a href="javascript:ie_func1('#my_courses_goto');">
			<![endif]-->
			<div id="browse_by_department_mc_back">
				<div class="my_courses_bbd_back_link space" >My&nbsp;courses</div>
			</div>
			</a>
			</div>
		<div id="browse_by_department_page_container">
			<div id="browse_by_department_topbar">
				<div id="browse_by_department_logout_button" >
<?php
	if($loggedIn==0)
	{
		echo "<a class=\"logout_button\" href=\"index.php\" style=\"top:0px;\">LOGIN</a>";
	}
	else
	{
		echo "<a class=\"logout_button\" href=\"/nucleus/logout\" style=\"top:0px;\">LOGOUT</a>";
	}	
?>	
				</div>
				<div id="browse_by_department_title">
					<span class="u_letter">U</span>PLOAD
				</div>
			</div>
			<div id="resultUpload">
			<?php
				$temp=$_GET['temp1'];
				echo "<div id='warning_upload' style='margin-left:30px; font-size:16px; color:#B00;'>";
				if(isset($temp))
				{
					$logfile=fopen("../lectut_profs_logs.txt",'a');
					$logstring="";
					if($temp=='y'){
						print("<script>$('#warning_upload').css('color','green');</script>File uploaded.");
						$logstring=(string)date("D F d Y",time())." ".(string)$facUsername." temp=y File uploaded\n"; 	
					}
					elseif($temp=='e'){
						print("<script>$('#warning_upload').css('color','red');</script>File already exists.");
						$logstring=date("D F d Y",time())." ".$facUsername." temp=e File already exists\n"; 	
					}
					elseif($temp=='n'){
						print("<script>$('#warning_upload').css('color','red');</script>File not uploaded. Please try after some time.");
						$logstring=date("D F d Y",time())." ".$facUsername." temp=n File  not uploaded. Please try after some time.\n"; 	
					}
					elseif($temp='u'){
						print("<script>$('#warning_upload').css('color','red');</script>Please select the file");
						$logstring=date("D F d Y",time())." ".$facUsername." temp=u Please select the file.\n"; 	
					}
					else{
						print("<script>$('#warning_upload').css('color','red');</script>Please select a choice.");	
						$logstring=date("D F d Y",time())." ".$facUsername." temp=else Please select a choice.\n"; 	
					}
					fwrite($logfile,$logstring);
					fclose($logfile);
				}
				echo "</div>";
			?>
			</div>
			<div id="upload_container">
			<div id="contact_us">In case of any clarifications, contact IMG at 01332-284521</div>
			<form id="upload" method="post" enctype="multipart/form-data" name="upload" action="upload.php" onsubmit="return validate_upload_form();">
			<div id="widthify">Select Type&nbsp;&nbsp;&nbsp;</div>
			<select name="type" onChange="show_form_special(document.upload.type.value)">
			<option value="lec">Lecture</option>
			<option value="tut">Tutorial</option>
			<option value="exam">Exam Paper</option>
			<option value="soln">Solution</option>
			</select><br>		
			<input type="hidden" name="fac_id" value="<?php echo $facUsername; ?>"><br>
			<div id="widthify">Subject Code&nbsp;&nbsp;</div>
      <input type="text" name="subcode" id="subcodeId"> *eg. EC-102 or EC-101A<br>
			<div id="widthify">Select File&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<input type="file" name="file" id="uploadFile"><br>
			<div id="widthify">Topic&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<input type="text" name="topic" id="Topic"><br>
			<!--<div id="widthify">Permissions&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<select name="permission">
				<option value="false">All</option>
				<option value="true">Only Registered</option>
			</select><br>-->
	<div id="show_exam_year">
			<div id="widthify">Year&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<input type="text" name="year" value=""> *only for Exam Papers<br>
	</div>
	<div id="show_soln_link">
			<div id="widthify">Link&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
			<select name="link" onChange="showUploaded(document.upload.link.value,'<?php echo $facUsername; ?>');">
				<option value="" selected>No choice</option>
				<option value="T">Tutorial</option>
				<option value="E">Exam Paper</option>
			</select> *only for Solutions
			

			
			<div class="scrollbarer" id="link_div">
					
			<div class="scrollbar"><div class="track"><div class="thumb"><div class="end"></div></div></div></div>
<!-- this set and not overview as this is the relatively outermost container div  -->
				<div class="viewport">
					<div class="overview" >
			
						<div id="show_uploaded">
						</div>
					</div>
				</div>
			</div>
			
			




			<br>
	</div>
			<input type="submit" value="Upload" id="upload_button">&nbsp;
<!-- onclick="javascript:uploadAjax(this.form)-->
			<input type="reset" value="Reset" id="reset_button">
		</form>		
			</div>
		</div>
	</div><div id="dummy_show_form" style="height:0px;width:0px;"></div>
</div>
        <script type="text/javascript">
        $('body').ready(function(){
            $('#subcodeId').autocomplete({
                  source:'/settings/course_search/',
                        minLength:1
                          });
        }); 
        parent.display_messages([]);

        </script>
