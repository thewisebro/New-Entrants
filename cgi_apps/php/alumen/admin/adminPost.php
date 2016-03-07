<? 
session_start();

require('../connection.php');

$formInfo=array();
//In case new fields are added to this form, just need to specify here. If the field is mandatory add it to the array $mandatory
$formInfo["username"]=$_POST["username"];
$formInfo["password"]=$_POST["password"];

$mandatory=array("username","password");

if (!get_magic_quotes_gpc()) 
{
	foreach($formInfo as $param => $info)
	{
		$formInfo[$param]=addslashes($info);

	}
}


/**************************functions**************************/
require('../common.php');
/***********************************************************/


if(check_mandatory($formInfo,$mandatory)==1) 
{
	//This function has inbuilt to deal with case of login failure.

	if($formInfo["username"]=="admin_mentor" && md5($formInfo["password"])=="c4a8cfad308db70453e2a675f8e0ba68")
	{
		$_SESSION["admin_user"]=$formInfo['username'];

		header("location:adminSuccess.php");	


	}
	else
	{
		include('index.php');
		show_message("'<span class=header>Incorrect Username or Password!</span>'");



	}	

}	
else
{
		include('index.php');
		//Show the error message to the user
		show_message("'You did not fill either the username or the password. Click <a href=index.html><b>here</b></a> to go back.'");
	

}
pg_close($dbcon);
?>
