<?php

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
  $email=$_POST['email'];
  $password=$_POST['password'];
  if($email=='pramod231193@gmail.com' or $email=='shailabunty@gmail.com' or $email=='adpanfeq@iitr.ernet.in'){
    if($password=='campussurvey2013'){
      echo true;
    }  
    else{  
      echo "admin";   
  
   }
  }
  elseif(EmailValidation($email) == false){
		echo "false";
	}
  else{
    echo "true";
  }
	
?>
