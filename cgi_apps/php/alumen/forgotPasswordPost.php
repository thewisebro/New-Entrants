<?php
session_start();
error_reporting(0);
include('connection.php');
require('mail.php');

include('static.html');

//Collect Variables

$formInfo=array();


//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory
$formInfo["email"]=$_POST["email"];

$mandatory=array("");



if (!get_magic_quotes_gpc()) 
{
	foreach($formInfo as $param => $info)
	{
		$formInfo[$param]=addslashes($info);

	}
}
/*****************************Functions***************************************************************************************/

require('common.php');

// Generate a random character string
 function rand_str($length = 32, $chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890')
 {
     // Length of character list
     $chars_length = (strlen($chars) - 1);

     // Start our string
     $string = $chars{rand(0, $chars_length)};
                   
     // Generate random string
     for ($i = 1; $i < $length; $i = strlen($string))
    {
        // Grab a random character from our list
        $r = $chars{rand(0, $chars_length)};
                                                     
      // Make sure the same two characters don't appear next to each other
       if ($r != $string{$i - 1}) $string .=  $r;
    }
                                                                
    // Return the string
   return $string;
   }
/**************************************************************************************************************************/


/********************************************Main Executable Part************************************************************************/
//First check if email exists in our db
$validArray=retrieveFromDb($dbcon,"basic_data","count(*) as cnt","email='".$formInfo["email"]."'");
$valid=$validArray[0];

$email=$formInfo["email"];
$formInfo=array();
$passwd=rand_Str(6);
$formInfo["password"]=md5($passwd);

if($valid["cnt"]==1 ) {

/////////////// if email address is valid------> 	
/////////////////////////sending mail///////////////////////////////

$message="Dear Alumnus<br/>Your password has been reset to $passwd. Login with this password and your username and reset your password.<br /><br />Warm Regards,<br />Information Management Group(IMG)<br />IIT Roorkee";
 email_to_user($email,"img@iitr.ernet.in","Alumni Mentorship Programme:Password Reset",$message,$message);

updateDb($dbcon,"basic_data",$formInfo,"email='$email'","ForgotPasswordDone");
}
else

	{

		//Show the error message to the user
		show_message("'Email could not be sent. Carefully check the email address you specified. If the problem persists use \'Report a Bug\' to tell us about the problem.'");
	

	}

/******************************************************************************************************************************/

pg_close($dbcon);
?>
