<?
	function EmailValidation($email)
	{ 
		$email = htmlspecialchars(stripslashes(strip_tags($email))); //parse unnecessary characters to prevent exploits
		if ( eregi ( '[a-z||0-9]@[a-z||0-9].[a-z]', $email ) ) { //checks to make sure the email address is in a valid format
			$domain = explode( "@", $email ); //get the domain name
			if ( @fsockopen ($domain[1],80,$errno,$errstr,3)){
				return true; //if the connection can be established, the email address is probably valid
			} 
			else{
				return false; //if a connection cannot be established return false
			}
			return false; //if email address is an invalid format return false
		}
	}
	if(isset($_POST['submit_login']) and $_POST['submit_login']=="Login"){
		if(!isset($_POST['email'])){
			die("Please fill in you email correctly");	
		}
		$email = $_POST['email'];
		$con = mysql_connect("192.168.121.9","survey","surv3y!") or die("Connection could not be setup <br/>"."Error in connection. Please try again."); 
		$db = mysql_select_db("campus_survey", $con) or die("Error in connection. Please try again.");	
		
    $email = mysql_real_escape_string($email);					
  	/* SQL QUERY STARTS */
		$query = "SELECT * FROM members WHERE `email`='$email'";
		$result = mysql_query($query, $con) or die("Error in connection. Please try again.");
		$num_rows = mysql_num_rows($result);
		
		if($num_rows){
			$query = "SELECT id,last_page, completed FROM members WHERE `email`='$email'";
			$result = mysql_query($query, $con) or die("Error in connection. Please try again.");
			$row = mysql_fetch_assoc($result);
			$last_page=$row['last_page'];
      $completed=$row['completed'];
		  $id=$row['id'];
      if($last_page!=''){
				$last_page = $last_page.".php";
				session_start();
				$_SESSION['email']=$email;
	      $_SESSION['highpage']=$last_page;
        $_SESSION['id']=$id;
	  	  if($last_page=='register.php'){
          $_SESSION['register']=1;
        } 
        if($completed==1){
          $_SESSION['highpage']='thankyou.php';
        }
				header("location:$last_page");	
				exit();
  		}
			else{
				$query = "UPDATE members SET `last_page`='register' WHERE `email`= '$email'";	
				mysql_query($query, $con) or die("Error in connection. Please try again.");
				session_start();
				$_SESSION['email']=$email;
				$_SESSION['highpage']='register.php';
        $_SESSION['id']=$id;
        header('location:register.php');
				exit();	
      }
   	}
		else{
      $query = "INSERT INTO members (`email`,`last_page`,`completed`) VALUES ('$email','register',0)";
			$result = mysql_query($query, $con) or die("Error in connection. Please try again.");
			$query = "SELECT id from members WHERE email='$email'";
			$result = mysql_query($query, $con) or die("Error in connection. Please try again.");
      $row=mysql_fetch_assoc($result);
			$id=$row['id'];
      session_start();
			$_SESSION['email']=$email;
			$_SESSION['highpage']='register.php';
			$_SESSION['register']=1;
      $_SESSION['id']=$id;
      header('location:register.php');
			exit();  
		}
	}
  else{
    
    session_start();
    if(isset($_SESSION['email'])){
      header('location:'.$_SESSION['current_page']);
    }
    //echo 'pramod';
  }
?>

