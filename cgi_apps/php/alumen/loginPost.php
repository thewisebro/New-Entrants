<? 
session_start();
require('connection.php');

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
require('common.php');

function chkStudentFilledData($student,$dbcon) // for checking if student_data has been filled
{
        $query ="Select * from student_data where username='$student'";
	$execute =pg_query($dbcon,$query);
	$row=pg_fetch_array($execute);

	if($row)
	      return 0;
	else
	      return 1;
}


/***********************************************************/

if(check_mandatory($formInfo,$mandatory)==1) 
{
	//This function has inbuilt to deal with case of login failure.
	$logincheck=verify_login($dbcon, $formInfo, 'both');
	if($logincheck==1)
	{
		$_SESSION["username"]=$formInfo['username'];
		header("location:loginSuccess.php");	


	}
	else if ($logincheck==2)
	{
		$_SESSION["student"]=$formInfo['username'];
		if(chkStudentFilledData($_SESSION['student'],$dbcon))
		{
			$_SESSION['studentdata']=0;
		}
		else
		{
			$_SESSION['studentdata']=1;
		}

		header("location:student.php");
	}
	else
	{
		include('index.php');
		echo $logincheck;	
		show_message("'<span class=header>Incorrect Username or Password!</span>'");
	}	

}	
else
{
		include("index.html");
		//Show the error message to the user
		show_message("'You did not fill either the username or the password. Click <a href=index.html><b>here</b></a> to go back.'");
}

include("disconnection.php");
?>
