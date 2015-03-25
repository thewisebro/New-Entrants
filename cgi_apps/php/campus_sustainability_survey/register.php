<?php
	require_once('common.php');
	require_once('register_verify.php');
	require_once('constants.php');
	$email = $_SESSION['email'];	
	$count_group=0;
	$count_alphabet=-1;
	$query="SELECT * FROM members WHERE `email`='$email'";
	$result=mysql_query($query, $con) or die("Error in connection. Please try again.");
	$result=mysql_fetch_assoc($result);	
	function date_picker($name, $year_flag=0, $startyear=NULL, $endyear=NULL)	{
			if($startyear==NULL) $startyear = date("Y")-50;
			if($endyear==NULL) $endyear=date("Y"); 

			$months=array('','January','February','March','April','May',
			'June','July','August', 'September','October','November','December');

			// Month dropdown
			$html="<select  id=\"".$name."month\" name=\"".$name."month\">";

			for($i=1;$i<=12;$i++)
			{
				 $html.="<option value='$i'>$months[$i]</option>";
			}
			$html.="</select> ";
		 
			// Day dropdown
			$html.="<select name=\"".$name."day\"  name=\"".$name."day\">";
			for($i=1;$i<=31;$i++)
			{
				 $html.="<option $selected value='$i'>$i</option>";
			}
			$html.="</select> ";

			// Year dropdown
			$year="<select  id=\"".$name."year\" name=\"".$name."year\">";

			for($i=$startyear;$i<=$endyear;$i++)
			{      
				$year.="<option value='$i' >$i</option>";
			}
			$year.="</select> ";

			$html = $html.$year;
			if($year_flag==1){
				return $year;
			}
			return $html;
	}
?>		
<html>
	<head>
    <link href ="bootstrap/css/bootstrap.css" rel="stylesheet" type="text/css" />
    <link href ="main.css" rel="stylesheet" type="text/css" />                   
    <link href ="bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
		<script type="text/javascript" src="jquery-1.8.min.js">
		</script>
		<script type="text/javascript">
			var prevval='.student';
			var prevval_student='#ug_year';
			$(document).ready(function(){
				/* Form Validation */
        $("#details_submit").click(function(){
          var unfilled=new Array();
          var a=0;
          $('form').find('input').each(function(){
            var name=$(this).attr('name');
            if(name=='nonacademic_designation' &&  $('#category').val()!=='nonacademic'){ 
              return;
            }
            if($(this).attr('type')=='radio'){  
              var str="input[name="+name+"]:checked";
              var value=$(str).val();
              if(value=='' || typeof(value)=='undefined'){
                unfilled.push(name);
                a=1;
                return;
              }
            }
            else{
              value=$(this).val();  
              if(value=='' || typeof(value)=='undefined'){
                unfilled.push(name);
                a=1;
                return;
              }
            }
          });
          if(a==1){
            var len=unfilled.length;
            $('td').css("background-color","#f9f9f9");
            
            for(var i=0;i<len;i++){
              var string=unfilled[i];
              if(string[0]=='D'){
                var str='.'+unfilled[i];
                $(str).css("background-color","#F2DEDE");
                str='#'+string.slice(0,5)+'_ENERGY';
                $(str).css("background-color","#F2DEDE");
              }
              else{  
                var str='#'+unfilled[i];
                $(str).css("background-color","#F2DEDE");
              }
            }
            alert('Please fill the form completely');
            return false;
          }
        });				
        $('#details_submit').click(function(){
          var age = $('.age_input').val();
					var from = $('#assoc_fromyear').val();
					var till = $('#assoc_toyear').val();
					if((age<=0 || age>100 || (isNaN(age))) ){
						if(age=='' || typeof(age)=="undefined"){
              return;
            }
            $('#age').css("background-color","#F2DEDE");
            alert("Enter valid age");
						return false;
					}
					if(from>till){
						alert("Please enter proper years of your association.");
						return false;
					}
       });
        /* Ajax Call before the page is closed */
        window.onbeforeunload=window.onunload=function(){
          $.ajax({
              url:'ajax_register.php',
              type:'post',
              async:'false',
              data:$('form').serialize(),
              success:function(data){
                //alert(data);
              } 
            });   
            return null;
          };
        /* jQuery for selected category */
        $("#category").change(function(){
					var value = $('#category option:selected').text();
					$(prevval).css("display","none");
					if(value=='Student'){
						$(".student").css("display","block");	
						prevval='.student';
						$(prevval_student).css("display","block");	
					
					}
					else if(value=='Non-Academic'){
						$(".nonacademic").css("display","block");	
						prevval='.nonacademic';
						$(prevval_student).css("display","none");	
					}
					else{	
						$(prevval_student).css("display","none");	
					}
				})
				$("#student_category").change(function(){				
					var value = $('#student_category option:selected').text();
					$(prevval_student).css("display","none");
					if(value=='UG'){
						$("#ug_year").css("display","block");	
						prevval_student='#ug_year';
					}
					else if(value=='PG'){
						$("#pg_year").css("display","block");	
						prevval_student='#pg_year';
					}
					else{
						$("#phd_year").css("display","block");	
						prevval_student='#phd_year';
					}
				})	
			});
		</script>
	</head>
	<body> 
  <div class="container">
 <div class="header"><img src="iitr_logo.jpg" style="float:right"><div style="clear:both;"></div> </div>
<div id="middle">

  <a href="logout.php" style="float:right;">Logout</a>
		<h2>GENERAL INFORMATION</h2><br/>
		<br/>
		<form action="" enctype="multipart/form-data" method="post">
			<table>
				<tr>	
					<td>
						<label for="category">Category: </label>
					</td>
					<td>
						<select id="category" name="category">
							<option value="student" selected="selected" >Student</option>
							<option value="Faculty" >Faculty</option>
							<option value="nonacademic" >Non-Academic</option>
						</select>
					</td>
				</tr>
				<tr>
					<td class="student">
						<label for="student_category">Category: </label>
					</td>
					<td class="student">
						<select name="student_category" id="student_category">
							<option value="UG" >UG</option>
							<option value="PG" >PG</option>
							<option value="Ph.D" >Ph.D</option>
						</select>
					</td>
					<td class="student">
						<label for="ug_year">Year: </label>
					</td>
					<td id="ug_year">
						<select name="acad_year">
							<option value="1" >1</option>
							<option value="2" >2</option>
							<option value="3" >3</option>
							<option value="4" >4</option>
						</select>
					</td>
					<td id="pg_year" style="display:none;">
						<select name="acad_year">
							<option value="1" >1</option>
							<option value="2" >2</option>
						</select>
					</td>
					<td id="phd_year" style="display:none;">
						<select name="acad_year">
							<option value="1" >1</option>
							<option value="2" ></option>
							<option value="3" >3</option>
						</select>
					</td>
				</tr>
				<tr>
					<td class="nonacademic" style="display:none;">
						<label for="nonacademic_designation">Designation</label>
					</td>
					<td class="nonacademic" style="display:none;">
						<input type="text" name="nonacademic_designation" id="nonacademic_designation" />
					</td>
					<td class="nonacademic" style="display:none;">
						<label for="nonacademic_category">Category: </label>
					</td>
					<td class="nonacademic" style="display:none;">
						<select name="nonacademic_category" id="nonacademic_category">
							<option value="A">Category A </option>
							<option value="B">Category B </option>
							<option value="C">Category C </option>
							<option value="D">Category D </option>
						</select>
					</td>	
				</tr>
				<tr>
					<td id="sex">Sex:</td>
					<td class="sex">
						<label for="male" style="display:inline">Male &nbsp;</label>
						<input type="radio" name="sex" id="sex" value="male"/>
						<label for="female" style="display:inline">Female</label>
						<input type="radio" name="sex" id="sex" value="female" />
					</td>
				</tr>
				<tr>
					<td id="age">
						<label for="age">Age:</label>
					</td>
					<td class="age">
						<input type="text" name="age" class="age_input">
					</td>
				</tr>
				<tr>
					<td id="institute">
						<label for="institute">Name of the Institute</label>
					</td>
					<td class="institute">
						<input type="text" name="institute"/>
					</td>
				</tr>
				<tr>
					<td id="department">
						<label for="department">Department</label>
					</td>
					<td class="department">
						<input type="text" name="department"/>
					</td>
				</tr>
				<br/>
				<tr>
					<td>Years of Association:</td>
					<td>
						<label for="year_from">From:</label>
							<?php
								echo date_picker("assoc_from",1);
							?>
						<label for="year_to">&nbsp; To:</label>
							<?php
								echo date_picker("assoc_to",1);
							?>
					</td>
				</tr>
			</table>	
			<input type="Submit" class="btn-primary" id="details_submit" name="details_submit" value="Submit" />	
		</form>
	  </div>
    </div>
    <div id="footer">
      <div id="footer_content">  
        <div class="footer_text">
            <a href="http://www.iitr.ac.in/campus_life/pages/Groups_and_Societies+IMG.html">
            Information Management Group
            </a>, IIT Roorkee &copy; <?php echo date('Y') ?>
            <br/>
            Contact us : <a href="mailto:img.iitr.img@gmail.com">img.iitr.img@gmail.com</a>
              
                             <iframe id="like_footer" src="//www.facebook.com/plugins/like.php?href=http%3A%2F%2Fwww.facebook.com%2FIMGIITRoorkee&amp;send=false&amp;layout=button_count&amp;width=450&amp;show_faces=false&amp;action=like&amp;colorscheme=dark&amp;font&amp;height=21" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:150px; height:21px; vertical-align:middle; margin-left:5px;" allowTransparency="true" style="margin-left:10px; background-color:#444" class="fb_like"></iframe>
        </div>
      </div>
    </div>

<!-- endfooter -->

  </body>
</html>
