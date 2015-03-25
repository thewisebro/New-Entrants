<?php
//session_start();

include("../common/constants.php");
include("../common/functions.php");
include("../../session/django_session.php");

$session = New Session();

$lecdown=$_POST['lec'];
$tutdown=$_POST['tut'];
$examdown=$_POST['exam'];
$solndown=$_POST['soln'];

$zip=new ZipArchive();
$time=time();

//if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
//{
if($session->isloggedin()){  
  $dir=tempnam(sys_get_temp_dir(), $_SESSION['lectut_username']);
}
else
{
  $dir=tempnam(sys_get_temp_dir(), "NA");
}

if($zip->open($dir,ZIPARCHIVE::CREATE)===TRUE)
{
	if(!empty($lecdown))
	{
		foreach($lecdown as $file)
		{
			$name=explode("/",$file);
			$zip->addFile(LECDIR."/$file","Lectures/".$name[1]);
		}
	}
	if(!empty($tutdown))
	{
		foreach($tutdown as $file)
		{
			$name=explode("/",$file);
			$zip->addFile(TUTDIR."/$file","Tutorials/".$name[1]);
		}
	}
	if(!empty($examdown))
	{
		foreach($examdown as $file)
		{
			$name=explode("/",$file);
			$zip->addFile(EXAMDIR."/$file","Exam Papers/".$name[1]);
		}
	}
	if(!empty($solndown))
	{
		foreach($solndown as $file)
		{
			$name=explode("/",$file);
			$zip->addFile(SOLNDIR."/$file","Solutions/".$name[1]);
		}
	}
	$zip->close();
}
else
{
	echo "Error : Cannot create the archive";
}

header("Content-type: application/zip");
header("Content-Disposition: attachment; filename=lecntut.zip");
header("Pragma: no-cache");
header("Expires: 0");
readfile($dir);

if(file_exists($dir))
{
	unlink($dir);
}

exit;
?>
