<?php
//session_start();
include_once("../common/functions.php");
include("../../session/django_session.php");
$session = new Session();
$loggedIn=false;

//if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
//{
if($session->isloggedin()){	
	if($_SESSION['group']=='f')
		$facId=$_SESSION['lectut_userid'];
	$loggedIn=true;
}
else
{
	$loggedIn=false;
}

if($loggedIn && $_SESSION['group']=='s')
{
	header("Location: ../pages/final_student.php");
}

database::connectToDatabase();	

$fileSpecial=array("`","~","!","@","#","$","%","^","*","=","+","\\","|","'","\"",";",":","/","?",">",",","<");
$facUsername=$_SESSION['lectut_username'];
$type=$_POST['type'];
$courseId=secureCode(filter_input(INPUT_POST,'subcode',FILTER_SANITIZE_STRING));
$name=$courseId." ".str_replace($fileSpecial,"",$_FILES['file']['name']);
$topic=secure(filter_input(INPUT_POST,'topic',FILTER_SANITIZE_STRING));
//$permit=$_POST['permission'];
$permit='false';
$year=secure(filter_input(INPUT_POST,'year',FILTER_SANITIZE_STRING));
$link=$_POST['link'];
$tmpname=$_FILES['file']['tmp_name'];
$size=$_FILES['file']['size'];

/*echo $_FILES['file']['error'];
echo $_FILES['file']['type'];*/

/*if(secureType($name))
{
	echo "File type not supported.";
	die();
}
else */if($size>10485760)
{
	echo "File exceeds size limit.";
	die();
}
else
{
/*	switch($type)
	{
		case 'lec':
			uploadLecture($tmpname,$facUsername,$courseId,$name,$topic,$permit);
			break;
		case 'tut':
			uploadTutorial($tmpname,$facUsername,$courseId,$name,$topic,$permit);
			break;
		case 'exam':
			uploadExam($tmpname,$facUsername,$courseId,$name,$topic,$permit,$year);
			break;
		case 'soln':
			uploadSoln($tmpname,$facUsername,$courseId,$name,$topic,$permit,$link);
			break;
		default:
			echo "Please select a choice.";
	}*/

	//to avoid file being uploading with empty faculty string (bug to be resolved, occurs rarely)
	if($facUsername!=""){
	switch($type)
	{
		case 'lec':
	if($name)
	{
		$dir1=LECDIR."/$facUsername";
		if(!file_exists($dir1))
		{
			mkdir($dir1,0777);
		}

/*		else
		{
			chmod($dir1,0777);
		}
*/		$temp=$name;
		$dir="$dir1/$temp";
	        $i=0;
		while(file_exists($dir))
		{
			$parts=explode('.',$name,2);
			$temp=$parts[0]."(".++$i.").".$parts[1];
			$dir="$dir1/$temp";
		}

		$lec=new lecture(1,$facUsername,$courseId,$temp,$topic,$permit);
	
		if (move_uploaded_file($tmpname,$dir))
		{
			$return_value = database::executeQuery($lec->uploadLec());
			if($return_value)
			{
				header("Location: faculty.php?temp1=y");	
			}
			else
			{
				header("Location: faculty.php?temp1=e");	
			}
/*			chmod($dir,0667);
			chmod($dir1,0667);*/
		} 
		else 
		{
			header("Location: faculty.php?temp1=n");	
		}
	}
	else
	{
		header("Location: faculty.php?temp1=u");	
	}

			break;
		case 'tut':
	if($name)
	{
		$dir1=TUTDIR."/$facUsername";
		if(!file_exists($dir1))
		{
			mkdir($dir1,0777);
		}
/*		else
		{
			chmod($dir1,0777);
		}

*/		$temp=$name;
		$dir="$dir1/$temp";
	       	$i=0;
		while(file_exists($dir))
		{
			$parts=explode('.',$name,2);
			$temp=$parts[0]."(".++$i.").".$parts[1];
			$dir="$dir1/$temp";
		}

		$tut=new tutorial(1,$facUsername,$courseId,$temp,$topic,$permit);

		if (move_uploaded_file($tmpname,$dir))
		{
			if(database::executeQuery($tut->uploadTut()))
			{
				header("Location: faculty.php?temp1=y");		
			}
			else
			{
				header("Location: faculty.php?temp1=e");
			}
/*			chmod($dir,0667);
			chmod($dir1,0667);*/
		} 
		else 
		{
			header("Location: faculty.php?temp1=n");
		}
	}
	else
	{
		header("Location: faculty.php?temp1=u");
	}
	
			break;
		case 'exam':
	if($name)
	{
		$dir1=EXAMDIR."/$facUsername";
		if(!file_exists($dir1))
		{
			mkdir($dir1,0777);
		}
/*		else
		{
			chmod($dir1,0777);
		}*/
	
		$temp=$name;
		$dir="$dir1/$temp";
	       	$i=0;
		while(file_exists($dir))
		{
			$parts=explode('.',$name,2);
			$temp=$parts[0]."(".++$i.").".$parts[1];
			$dir="$dir1/$temp";
		}

		$exam=new exampaper(1,$facUsername,$courseId,$temp,$topic,$permit,$year);
		
		if (move_uploaded_file($tmpname,$dir))
		{
			if(database::executeQuery($exam->uploadExamPaper()))
			{
				header("Location: faculty.php?temp1=y");
			}
			else
			{
				header("Location: faculty.php?temp1=e");		
			}
		/*	chmod($dir,0667);
			chmod($dir1,0667);*/
		} 
		else 
		{
			header("Location: faculty.php?temp1=n");
		}
	}
	else
	{
		header("Location: faculty.php?temp1=u");
	}

			break;
		case 'soln':
	if($name)
	{
		$dir1=SOLNDIR."/$facUsername";
		if(!file_exists($dir1))
		{
			mkdir($dir1,0777);
		}
/*		else
		{
			chmod($dir1,0777);
		}
		
*/		$temp=$name;
		$dir="$dir1/$temp";
	       	$i=0;
		while(file_exists($dir))
		{
			$parts=explode('.',$name,2);
			$temp=$parts[0]."(".++$i.").".$parts[1];
			$dir="$dir1/$temp";
		}
	
		$link_type="";
		$linkid="NULL";
	
		switch($link)
		{
			case 'T':$link_type='T';
				$linkid=$_POST['link_tut'];
				break;

			case 'E':$link_type='E';
				$linkid=$_POST['link_exam'];
			         break;

			default:break;
		}

		$soln=new solution(1,$facUsername,$courseId,$temp,$topic,$permit,$link_type,$linkid);

		if (move_uploaded_file($tmpname,$dir))
		{
      if(database::executeQuery($soln->uploadSolution()))
			{
				header("Location: faculty.php?temp1=y");
			}
			else
			{
				header("Location: faculty.php?temp1=e");			
			}
/*			chmod($dir,0667);
			chmod($dir1,0667);*/
		} 
		else 
		{
			header("Location: faculty.php?temp1=n");
		}
	}
	else
	{
		header("Location: faculty.php?temp1=u");
	}

			break;
		default:
			header("Location: faculty.php?temp1=x");	
	}
	}

	database::closeDatabase();
}

?>
