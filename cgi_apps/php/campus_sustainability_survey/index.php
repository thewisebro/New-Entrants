  <?php
    require('email_verify.php');
  ?>	

<html>
	<head>
  <link href ="bootstrap/css/bootstrap.css" rel="stylesheet" type="text/css" />

  <link href ="main.css" rel="stylesheet" type="text/css" />
  <link href ="bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
		<script type="text/javascript" src="jquery-1.8.min.js">
	</script>
	<script type="text/javascript">
    $(document).ready(function(){
      $('form').submit(function(){
        var email=$('input[id=email]').val();
        var pass=$('input[id=password]').val();
        var str='email='+email+'&password='+pass;
        var flag=0;
        $.ajax({
          url:'ajax_email.php',
          type:'post',
          async:false,
          data:str,
          success:function(data){
            if(data=='false'){
              alert('Enter Valid Email Address');
              flag=1;
              $('#pass').css('display','none');
            }
            else if(data=='admin'){
              alert('If you are an admin enter correct password or please check your email.');
              flag=1;
              $('#pass').css('display','block');
            }
            else{

               $('#pass').css('display','none');           
            }
          } 
        });
        if(flag==1){
          return false;
        }    
      });
    });
  </script>
  </head>
<body>
 <div class="container">
 <div class="header"><img src="iitr_logo.jpg" style="float:right"><div style="clear:both;"></div> </div>
  <div id="middle">
   <div>
    <p>
      <h2>CAMPUS SUSTAINABILITY SURVEY...</h2><br/>
   <b>Sustainability as applicable to campuses is ...</b> efficient use and management of natural resources for the fulfilment of the human needs without compromising the richness of the ecosystem over a prolonged period of time.<br/><br/>
      This survey is being conducted as a part of Doctoral Thesis of Shaila Bantanur on<br/> <b>"Sustainability of Higher Educational campuses"</b> <br/>at the <b>Department of Architecture and Planning of IIT Roorkee,<br/> under the guidance of Dr. Mahua Mukherjee and Prof R.Shankar</b><br/> Response to this survey will help to analyze user awareness and preferences and selection of environmental performance indicators for improving campus sustainability.<br/> Your cooperation is solicited and your contribution will be greatly appreciated.<bt/> (All information obtained from the survey will be treated in complete confidence, and will be used only for academic research).
<br/>
 <br/>
    </p>
  </div>
 <br><br><br>
	<form method="post" action="" enctype="multipart/form-data" style="width:50%; margin:0 auto;">
			<label for="email">Please enter your email to begin: </label>
			<input type="email" name="email" id="email"/><br/>	
			<div id='pass' style="display:none;"><input id='password' name='password' type="password" /></div><br/>
      <input class="btn-primary" style="margin-left:150px;" type="submit" value="Login" name="submit_login"/>
  <br/>
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
