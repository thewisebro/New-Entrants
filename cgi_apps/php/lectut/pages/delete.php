<?php

include("../common/include_in_all.php");

database::connectToDatabase();

$lecdel=$_POST['lec'];
$tutdel=$_POST['tut'];
$examdel=$_POST['exam'];
$solndel=$_POST['soln'];
$countd=0; //count deleted
$countnd=0;//count not deleted
$countne=0;//count do not exist

if($_SESSION['group']=='f')
{
  $facUsername=$_SESSION['lectut_username'];
}
else
{
  header("Location: index.php");
}

if(!empty($lecdel))
{
	foreach($lecdel as $file)
	{
		$name=explode("/",$file);
		$lec=new lecture($name[0],$facUsername,null,null,null,null);
		echo $name[0];	
		$deletefile=ROOT."/uploads/lectures/".$facUsername."/".$name[1];
		if(unlink($deletefile))
		{
			$ret=database::executeQuery($lec->deleteLec());
			if($ret)
			{	
				$countd++;
			//	header("Location: final_prof.php?temp2=d");		
			}
			else
			{
				$countne++;
			//	header("Location: final_prof.php?temp2=n");		
			}
		}
		else
		{
			$countnd++;
		//	header("Location: final_prof.php?temp2=nd");		
		}
	}
}
if(!empty($tutdel))
{
	foreach($tutdel as $file)
	{	
		$name=explode("/",$file);
		$tut=new tutorial($name[0],$facUsername,null,null,null,null);

		$deletefile=ROOT."/uploads/tutorials/".$facUsername."/".$name[1];
	
		if(unlink($deletefile))
		{
			$ret=database::executeQuery($tut->deleteTut());
			if($ret)
			{
				$countd++;
		//		header("Location: final_prof.php?temp2=d");		
			}
			else
			{
				$countne++;
		//		header("Location: final_prof.php?temp2=n");		
			}
		}
		else
		{
			$countnd++;
		//	header("Location: final_prof.php?temp2=nd");		
		}
	}
}
if(!empty($examdel))
{
	foreach($examdel as $file)
	{
		$name=explode("/",$file);
		$exam_paper=new exampaper($name[0],$facUsername,null,null,null,null,null);

		$deletefile=ROOT."/uploads/exampapers/".$facUsername."/".$name[1];

		if(unlink($deletefile))
		{
			$ret=database::executeQuery($exam_paper->deleteExamPaper());
			if($ret)
			{
				$countd++;
		//		header("Location: final_prof.php?temp2=d");	
			}
			else
			{
				$countne++;
		//		header("Location: final_prof.php?temp2=n");	
			}
		}
		else
		{
			$countnd++;
		//	header("Location: final_prof.php?temp2=nd");		
		}
	}
}

if(!empty($solndel))
{
	foreach($solndel as $file)
	{
		$name=explode("/",$file);
		$soln=new solution($name[0],$facUsername,null,null,null,null,null,null);

		$deletefile=ROOT."/uploads/solutions/".$facUsername."/".$name[1];
		if(unlink($deletefile))
		{
			$ret=database::executeQuery($soln->deleteSolution());
			if($ret)
			{
				$countd++;
		//		header("Location: final_prof.php?temp2=d");		
			}
			else
			{
				$countne++;
		//		header("Location: final_prof.php?temp2=n");		
			}
		}
		else
		{
			$countnd++;
		//	header("Location: final_prof.php?temp2=nd");		
		}
	}
}

header("Location: final_prof.php?temp2=y&d=$countd&nd=$countnd&ne=$countne");


database::closeDatabase();

?>
