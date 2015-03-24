<?php
//error_reporting('E_ALL');
include("../common/functions.php");
include("../../session/django_session.php");

$session = new Session();
if($session->isloggedin()) {
  $user_info = $session->get_user_info();
  $user_id = $user_info['user_id'];
  $username = $session->get_username();
  database::connectToDatabase();
  $choice=database::executeQuery(database::getDesignChoice($username));
  $design=mysql_fetch_row($choice);

  $group = $session->get_group();
  switch($group)
	{
		case "Student":	
      $row=database::executeQuery(database::getStudName($user_id));
      $numrow=mysql_num_rows($row);
			if($numrow==1)
			{
				$_SESSION['lectut_username']=$username;
				$_SESSION['lectut_userid']=$user_id;
				$_SESSION['group']="s";
        $_SESSION['welcome']=0;
				header("Location: ../pages/final_student.php");
			}
			break;
		
		case "Faculty":
      $row=database::executeQuery(database::getFacName($user_id));
			$numrow=mysql_num_rows($row);
			if($numrow==1)
			{
				$_SESSION['lectut_userid']=$user_id;
				$_SESSION['lectut_username']=$username;
				$_SESSION['group']="f";
        $_SESSION['welcome']=0;
				if($design[2]=='t' && $design[1]==$username)
				{
					header("Location: ../pages_old/faculty.php");
				}
				else
				{
					header("Location: ../pages/final_prof.php");
				}
			}
			break;
		
		  default: header("Location: /nucleus/login/?next=".$_SERVER['REQUEST_URI']);
	}
	database::closeDatabase();
}
else
{
	header("Location: /nucleus/login/?next=".$_SERVER['REQUEST_URI']);
}

?>

