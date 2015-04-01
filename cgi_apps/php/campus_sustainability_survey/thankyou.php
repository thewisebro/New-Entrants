<?php
	require('common.php');
	require('constants.php');
    $highpage=$_SESSION['highpage'];
    if(($highpage=='index.php' or $highpage=='register.php' or $highpage=='survey_partB1.php' or $highpage=='survey_partB2.php' or $highpage=='survey_partC1.php' or $highpage=='survey_partC2.php' or $highpage=='survey_partD1.php' or $highpage=='survey_partD2.php' or $highpage=='survey_partD3.php' or $highpage=='survey_partE1.php' or $highpage=='survey_partE2.php' or $highpage=='survey_partF.php')){
      header('location:'.$_SESSION['current_page']);
    }
    else{
   		$id=$_SESSION['id'];
      $query = "UPDATE members SET last_page='survey_partB1' WHERE id=$id";
	  	mysql_query($query, $con) or die("Error in connection. Please try again.");
      $_SESSION['current_page']='thankyou.php';
    }  
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
    <br/>
      <div>  &nbsp;&nbsp;  
    <?php 
      if($email=='pramod231193@gmail.com' or $email=='shailabunty@gmail.com' or $email=='adpanfeq@iitr.ernet.in'){
        echo '<a href="members_csv.php" style="">Download members Data</a>';
        echo ' &nbsp; &nbsp; <a href="survey_csv.php" style="">Download Survey Answers</a>';
      }
      
      ?>
&nbsp;   &nbsp; <a href="logout.php" style="float:right;">Logout</a>
		<div style="width:50%; margin:0 auto;"><h3>Thank you for your valuable response!</h3></div>
	     <div style="width:50%; margin:0 auto;">
        <span style=''>
  				<input type="button" class="btn-primary" value="Previous" onClick="window.location.href='survey_partF.php'">	
  			</span>
      </div> 
  </div>
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
