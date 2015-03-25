<?php
	require('common.php');
	require('constants.php');
	require('partF_verify.php');
  $email=$_SESSION['email'];
?>
<html>
	<head>
  <link href ="bootstrap/css/bootstrap.css" rel="stylesheet" type="text/css" />
  <link href ="main.css" rel="stylesheet" type="text/css" />
  <link href ="bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
	<script type="text/javascript">
	</script>
	<script type="text/javascript" src="jquery-1.8.min.js">
	</script>
	<script type="text/javascript" src="validation.js">
	</script>
	</head>
	<body>
  <div class="container">
    <div class="header"><img src="iitr_logo.jpg" style="float:right"><div style="clear:both;"></div> </div>
    <div id="middle">
    <br/> &nbsp; 
      <div>  &nbsp;&nbsp;  
    <?php 
      if($email=='pramod231193@gmail.com' or $email=='shailabunty@gmail.com' or $email=='adpanfeq@iitr.ernet.in'){
        echo '<a href="members_csv.php" style="">Download members Data</a>';
        echo ' &nbsp; &nbsp; <a href="survey_csv.php" style="">Download Survey Answers</a>';
      }
      
      ?>
&nbsp;   <a href="logout.php" style="float:right;">Logout</a>
		<h2>Part F. </h2>
		<form method="post" enctype="multipart/form-data" action="">
		<?php
			$email = $_SESSION['email'];	
			$count_group=0;
			$count_alphabet=-1;
			echo "<br/>";
  		$id=$_SESSION['id'];
			$query = "SELECT * FROM questions WHERE id>=178 and id<=179";
			$rlt = mysql_query($query, $con) or die("Error in connection. Please try again.");
			$count=0;
			echo "<table>";
      while($row = mysql_fetch_assoc($rlt)){
				$name=$row['number'];
        $query="SELECT * FROM survey WHERE person_id='$id' and question='$name'";
  			$result=mysql_query($query, $con) or die("Error in connection. Please try again.");
	  		$result=mysql_fetch_assoc($result);
				$answer=$result['answer'];
				$section=$row['section'];
				$count++;
				$str=explode('_',$row['number']);
				if(($str[1] != $prev[1]) or $count==1){
					$count_alphabet++;
					$count_roman=-1;
					echo "<tr><td><b>Q1.$section</b></td></tr>";
				}
				$count_roman++;
				echo "<tr><td width='400px' height='40px' id='$name'>($roman[$count_roman]) $row[question]</td>";
				$prev=explode('_',$row['number']);
				if($name=='F_2_1'){
					echo "<td><textarea name='F_2_1'>$answer</textarea></td></td>";
					continue;
				}
				foreach($partF_options as $key=>$option){
					if($option == $answer){
						echo '<td width="75px" class="'.$name.'" > &nbsp; <input type="radio" name="'.$name.'" value="'.$option.'" checked="checked"/> '.$option.' &nbsp; </td>';	
					}
					else{
						echo '<td width="75px" class="'.$name.'" > &nbsp; <input type="radio" name="'.$name.'" value="'.$option.'"/> '.$option.' &nbsp; </td>';	
					}
				}
				echo "</tr>";
			}
      echo "</table><br/>";
	    $query="SELECT * FROM questions WHERE number='F_others'";
      $result=mysql_query($query, $con);
      $result=mysql_fetch_assoc($result);
      $name=$result['question'];
      $query="SELECT * FROM survey WHERE person_id='$id' and question='F_others'";
      $rslt=mysql_query($query, $con) or die("Error in connection. Please try again.");
      $rslt=mysql_fetch_assoc($rslt);
      $answer=$rslt['answer'];
      echo "<span width='' height='40px'><b>Q.2.$result[question]</b></span> &nbsp; &nbsp; &nbsp;";
      if($answer==''){
        echo "<span><textarea name='F_others'></textarea></span><br/>";
			}
      else{
         echo "<span><textarea name='F_others'>$answer</textarea></span><br/>";	     
      }
      ?>
      <br/>
      <div style="width:50%; margin:0px auto;">
      <span style='margin:auto;'>
				<input class="btn-primary" type="button" value="Previous" onClick="window.location.href='survey_partE2.php'">	
			</span>
       &nbsp; &nbsp; &nbsp;     
			<span style='margin:auto;'><input class="btn-primary" type='submit' name='partF_submit' value='Next'></span>
		  </div>
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
