<?php
	require('common.php');
	require('constants.php');
	require('partD_verify2.php');
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
    <br/>     <div>  &nbsp;&nbsp;  
    <?php 
      if($email=='pramod231193@gmail.com' or $email=='shailabunty@gmail.com' or $email=='adpanfeq@iitr.ernet.in'){
        echo '<a href="members_csv.php" style="">Download members Data</a>';
        echo ' &nbsp; &nbsp; <a href="survey_csv.php" style="">Download Survey Answers</a>';
      }
      
      ?>
&nbsp; &nbsp; <a href="logout.php" style="float:right;">Logout</a>
		<form method="post" enctype="multipart/form-data" action="">
		<?php
			$email = $_SESSION['email'];	
			$count=0;
			$count_alphabet=1;
			echo "<div class='partD_options'>";
      foreach($partD_options['ENERGY'] as $key=>$value){
				echo " <span class='partD_option'> &nbsp; <i>$key.$value</i> &nbsp; </span>";	
			}
			echo "</div><br/><br/>";
  		$id=$_SESSION['id'];
  		$query = "SELECT * FROM questions WHERE id>=65 and id<=109";
			$rlt = mysql_query($query, $con) or die("Error in connection. Please try again.");
			echo "<table>";
		  echo "<tr><th colspan='2'></th><th colspan='5'>ENERGY</th><th colspan='5' class='waste_td'>WASTE</th><th colspan='5'>WATER</th></tr>";
			echo "<tr><td></td><td></td><td>&nbsp; 1.</td> <td>&nbsp; 2.</td> <td>&nbsp; 3.</td> <td>&nbsp; 4.</td><td></td> ";
      echo "<td class='waste_td'>&nbsp; 1.</td> <td class='waste_td'>&nbsp; 2.</td> <td class='waste_td'>&nbsp; 3.</td> <td class='waste_td'>&nbsp; 4.</td><td class='waste_td'></td>";
      echo " <td>&nbsp; 1.</td> <td>&nbsp; 2.</td> <td>&nbsp; 3.</td> <td>&nbsp; 4.</td><td></td></tr> ";
      $count=0;
			while($row = mysql_fetch_assoc($rlt)){
        $count++;
        if((($count)%3)!=1){
          continue;
        }
				$name=$row['number'];
				$section=$row['section'];
				$str=explode('_',$row['number']);
				if(($str[1] != $prev[1]) or $count==1){
					$count_alphabet++;
					$count_roman=-1;
					echo "<tr><td><b>$alphabet[$count_alphabet].$section</b></td>";
					  echo "<td></td><td></td> <td></td> <td></td> <td></td><td></td> ";
          echo "<td class='waste_td'></td> <td class='waste_td'></td> <td class='waste_td'></td> <td class='waste_td'></td><td class='waste_td'></td>";
          echo " <td></td> <td></td> <td></td> <td></td><td></td></tr> ";
				}
				$count_roman++;
				echo "<tr><td width='600px' height='40px' id='$name'>($roman[$count_roman]) $row[question]</td><td></td>";
				$prev=explode('_',$row['number']);
				foreach($partD_options as $category=>$options){
          $name='';
          if($category == 'ENERGY'){
            $name=$str[0]."_".$str[1]."_".$str[2]."_ENERGY";
            //$name='pramod';
          } 
	        elseif($category == 'WASTE'){
            $name=$str[0]."_".$str[1]."_".$str[2]."_WASTE";
          } 
	        elseif($category == 'WATER'){
            $name=$str[0]."_".$str[1]."_".$str[2]."_WATER";
          } 
	        $query="SELECT * FROM survey WHERE person_id='$id' and question='$name'";
          $result=mysql_query($query, $con) or die("Error in connection. Please try again.");
          $result=mysql_fetch_assoc($result);
          $answer=$result['answer'];
          $class='';
          if($category=='WASTE'){
            $class='waste_td';
          }  
					foreach($options as $key=>$option){
						if($option == $answer){
  						 echo '<td width="75px" class="'.$name.' '.$class.'" > &nbsp; <input type="radio" name="'.$name.'" value="'.$option.'" checked="checked"/>&nbsp; </td>';	
						}
						else{
  						echo '<td width="75px" class="'.$name.' '.$class.'" > &nbsp; <input type="radio" name="'.$name.'" value="'.$option.'"/>&nbsp; </td>';	
						}
						if($key==4){
							echo "<td width='40px' class='$class'></td>";
						}
					}
				}
				echo "</tr>";
			}
			?>
      </table>
			<br/>
      <div style="width:50%; margin:0 auto;">	
	        <span> <input class="btn-primary" type="button" value="Previous" onClick="window.location.href='survey_partD1.php'">	</span>
			  &nbsp; &nbsp; &nbsp; 
			  <span> <td><input class="btn-primary" type='submit' name='partD_submit' value='Next'></td></tr></span>
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
