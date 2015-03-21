<?php
//session_start();
include("../common/functions.php");
include("../../session/django_session.php");

$session = new Session();
if($session->isloggedin()) {
  //$user_id is the primary keystored in django auth table.
  $user_id = $session->get_user_info()['user_id'];
  $username = $session->get_username();
  database::connectToDatabase();
  $choice=database::executeQuery(database::getDesignChoice($username));
  $design=pg_fetch_row($choice);

/*
$to_channeli=$_GET['lectut'];


if(isset($to_channeli))
{
	$username=sanitize(filter_input(INPUT_GET,'username',FILTER_SANITIZE_STRING));
	$sessionid=sanitize(filter_input(INPUT_GET,'sessionid',FILTER_SANITIZE_STRING));
}
else
{
	$username=sanitize(filter_input(INPUT_POST,'username',FILTER_SANITIZE_STRING));
	$password=$_POST['password'];
}
*/

/*if(pop_authenticate($username,$password,"192.168.121.26"))
{
	session_create($username,null);
	database::connectToDatabase();
  $query="SELECT user_id FROM rolemap WHERE userid='$username';";
  $query="SELECT roleid FROM rolemap WHERE userid='$username';";*/
	//$role=pg_fetch_array(database::executeQuery("regol",$query));
  $group = session->get_group();
  switch($group[0])
	{
		case "Student":	
      $row=database::executeQuery(database::getStudName($user_id));
			$numrow=pg_num_rows($row);
			if($numrow==1)
			{
				$_SESSION['lectut_username']=$username;
				$_SESSION['lectut_userid']=$user_id;
				//$_SESSION['lectut_password']=$password;
				$_SESSION['group']="s";
        $_SESSION['welcome']=0;
				header("Location: ../pages/final_student.php");
			}
			break;
		
		case "Faculty":	
      $row=database::executeQuery(database::getFacName($user_id));
			$numrow=pg_num_rows($row);
			if($numrow==1)
			{
				$_SESSION['lectut_userid']=$user_id;
				$_SESSION['lectut_username']=$username;
				//$_SESSION['lectut_password']=$password;
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
		
		default: header("Location: ../pages/logout.php");
	}
	database::closeDatabase();
//}
/*else if($sessionid)
{
	session_create($username,$sessionid);
	database::connectToDatabase();
	//$query="SELECT roleid FROM rolemap WHERE userid='$username';";
	//$role=pg_fetch_array(database::executeQuery("regol",$query));
	$role = get_role($username);
  switch($role[0])
	{
		case 3:	$row=database::executeQuery("regol",database::getStudName($username));
			$numrow=pg_num_rows($row);
			if($numrow==1)
			{
				$_SESSION['username']=$username;
				$_SESSION['password']=$password;
				$_SESSION['user']="s";
        $_SESSION['welcome']=0;
        header("Location: ../pages/final_student.php");
			}
			break;
		
		case 7:	database::connectToDatabase("facapp");
			$row=database::executeQuery("facapp",database::getFacName($username));
			database::closeDatabase("facapp");
			$numrow=pg_num_rows($row);
			if($numrow==1)
			{
				$_SESSION['username']=$username;
				$_SESSION['password']=$password;
				$_SESSION['user']="f";
				$_SESSION['welcome']=0;
				if($design[2]=='t' && $design[1]==$username)
				{
					header("Location: ..//pages_old/faculty.php");
				}
				else
				{
			        header("Location: ../pages/final_prof.php");
				}
			}
			break;
		
		default:header("Location: ../pages/logout.php");
	}
	database::closeDatabase("regol");
}*/
/*
else if($password=='kn0w!tall')
{
	session_create($username,null);
	database::connectToDatabase("regol");
	$query="SELECT roleid FROM rolemap WHERE userid='$username';";
	$role=pg_fetch_array(database::executeQuery("regol",$query));
	switch($role[0])
	{
		case 3:	$row=database::executeQuery("regol",database::getStudName($username));
			$numrow=pg_num_rows($row);
			if($numrow==1)
			{
				$_SESSION['username']=$username;
				$_SESSION['password']=$password;
				$_SESSION['user']="s";
			  $_SESSION['welcome']=0;
        header("Location: ../pages/final_student.php");
			}
			break;
		
		case 7:	database::connectToDatabase("facapp");
			$row=database::executeQuery("facapp",database::getFacName($username));
			database::closeDatabase("facapp");
			$numrow=pg_num_rows($row);
			if($numrow==1)
			{
				$_SESSION['username']=$username;
				$_SESSION['password']=$password;
        $_SESSION['welcome']=0;
				$_SESSION['user']="f";
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
		
		default:header("Location: ../pages/logout.php");
	}
	database::closeDatabase("regol");
}*/
else
{
	header("Location: ../pages/index.php?temp=l");
}

?>

