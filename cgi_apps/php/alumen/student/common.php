<?php

require("../pop-authenticate.php");

  function upload2Db($dbcon,$table,$formInfo,$destination)
{
	//Basic Query Structure
	$submit_query="insert into $table ([fields]) values ([values])";

	$fields="";
	$values="";
	//Now we will dynamically build the query
	foreach($formInfo as $param=>$info)
	{
		$fields.=$param.",";
		$values.="'$info',";

	}

	$fields=substr($fields,0,-1);
	$values=substr($values,0,-1);

	$submit_query=str_replace("[fields]",$fields,$submit_query);
	$submit_query=str_replace("[values]",$values,$submit_query);	

	//$_SESSION["student"]=$formInfo["username"];
	
	if(pg_query($dbcon,$submit_query)!=FALSE && $destination!="null")
	{
		$_SESSION['studentdata']=1;
		$_SESSION['message']="Profile Saved"; 
		echo "<script language='javascript'>";
		echo "document.location='../student.php#$destination';";
		echo "updateInfo('$destination')";
		echo "</script>";

	}
	
}

function upload_application($dbcon,$table,$formInfo)
{
	//Basic Query Structure
	$submit_query="insert into $table ([fields]) values ([values])";
	$fields="";
	$values="";

	//Now we will dynamically build the query

 	foreach($formInfo as $param=>$info)
	{
		$fields.=$param.",";
		$values.="'$info',";
	}

	$fields=substr($fields,0,-1);
	$values=substr($values,0,-1);

	$submit_query=str_replace("[fields]",$fields,$submit_query);
	$submit_query=str_replace("[values]",$values,$submit_query);

	$execute=pg_query($dbcon,$submit_query);
}

/*
 *  getStudentDetails : gets the required fields of student from channel-i db
 *  
 * Input : $fields, required columns of the student, from mulitple tables.
           use, auth.<column>  for auth_user table
                nperson.<col> for nucleus_person table
                nmap.<col> for nucleus_personidenrollmentnomap
                nbranch.<col> for nucleus_branch
 *
 * 
 */
function getStudentDetails($dbconchanneli, $fields, $student_id)
{
  $tables = "nucleus_person nperson, auth_user auth,
             nucleus_personidenrollmentnomap nmap, nucleus_branch nbranch";
  $condition = "nperson.user_id = auth.id and nmap.enrollment_no = auth.username and nperson.branch_id = nbranch.code and nmap.person_id = '$student_id'";
  $select_query = "select $fields from $tables where $condition";
  $result = mysqli_query($dbconchanneli, $select_query);

  if( $result != FALSE)
  {
    $main_array = array();
    while( $row = mysqli_fetch_array($result) )
      $main_array[] = $row ;

    return $main_array;
  }
}

function retrieveFromDb($dbcon,$table,$fields,$where_condition)
{
	//Basic Query Structure
	$select_query="select $fields from $table where $where_condition";
	$select_result=pg_query($dbcon,$select_query);
	$main_array=array();
	if($select_result!=FALSE)
	{
		while($select_array=pg_fetch_array($select_result))
			$main_array[]=$select_array;
		return $main_array;	
	}
	else
	{
		$main_array[0][0]=0;
		return $main_array;
	}
}

function updateDb($dbcon, $table, $formInfo,$where_condition, $destination)
{	

	$code=md5($formInfo['code']);
	
	//Now we will dynamically build the query
	
	foreach($formInfo as $param=>$info)
	{
		$fields.=$param.",";
		$values.="'$info',";

	}

	$fields=substr($fields,0,-1);
	$values=substr($values,0,-1);

	$submit_query=str_replace("[fields]",$fields,$submit_query);
	$submit_query=str_replace("[values]",$values,$submit_query);	
	 
	$_SESSION["username"]=$formInfo["username"];
	$username=$formInfo["username"];
	$check_query="select * from $table where username='$username'";	

	$check_result=pg_query($dbcon,$check_query);
	$query_result=array();

	while($row = pg_fetch_array($check_result))
	{
	$query_result[0]=$row["username"];
	}	
	if(!empty($query_result))
	{
	$update_query="update $table set ([fields])=([values])	where [where_condition]";
	$update_query=str_replace("[where_condition]",$where_condition,$update_query);
	}
	else
	{
	$update_query="insert into $table ([fields]) values ([values])";
	}			
	$update_query=str_replace("[fields]",$fields,$update_query);
	$update_query=str_replace("[values]",$values,$update_query);
//update_query=str_replace("[where_condition]",$where_condition,$update_query);
	
	if(pg_query($dbcon,$update_query)!=FALSE && $destination!="null")
	{
		$_SESSION['message']="Your profile has been updated.";
		$_SESSION['studentdata']=1;

		echo "<script language='javascript'>";
		echo "document.location='../student.php#$destination';";
		echo "updateInfo('$destination')";
		echo "</script>";

	}
	else if($destination!="null")
	{
		echo $check_query;
		echo $query_result[0];
		echo $update_query;
		echo "An error occured";

	}
	
}



function check_mandatory($formInfo,$fields)
{
	foreach($fields as $f)
		if($formInfo[$f]=="")
		{
		
			return 0;
		}		
	return 1;

}

function show_message($message)
{
	echo "<script language='javascript'>";
	echo "document.getElementById('middle_left_top').innerHTML=$message";
	echo "</script>";	

}
function alter_HTML($div,$content)
{
	echo "<script language='javascript'>";
	echo "document.getElementById('$div').innerHTML=$content";
	echo "</script>";	

}
/*Can be used in two cases : to check before new registration & when a user goes for "Forgot Password" Option to see if he exists or not*/
function user_already_exists($dbcon,$username,$email)
{
	$check_user_query="select count(*) as cnt from basic_data where username='$username' or email='$email'";

	$user_count=pg_query($dbcon,$check_user_query);
	
	$user_count_row=pg_fetch_row($user_count);

	$user_count_value=$user_count_row[0];
	if($user_count_value>0)
		return 1;
	else
		return 0;
}



/*$mode means: 'both'=both username & passwd are passed as arguements(at time of login); 'username'=just to check in b/w if user is logged in or not*/
function verify_login($dbcon,$formInfo,$mode)
{


	switch($mode)
	{
		case 'both':
		/*********************************************************/
		$login_query="select count(*) as cnt from basic_data where username='".$formInfo['username']."' and password='".md5($formInfo['password'])."'";

		$result=pg_query($dbcon,$login_query);
		$result_row=pg_fetch_row($result);
		$valid_count=$result_row[0];
		
		if($valid_count==1)
		{
		
			return 1;

		}
		else if (pop_authenticate($formInfo['username'],$formInfo['password'],"192.168.121.26"))
		{
			return 2;
		}
		else
			show_message("'Invalid username or password!'");

		/*********************************************************/
		break;		
	
		case "username":
			if(isset($_SESSION["username"]) && $formInfo==$_SESSION["username"])
				return 1;
			else
			{	session_unset();
				show_message("'You are not logged in.'");

			}

		break;
		
		case "student":
			if (isset($_SESSION["student"]) && $formInfo==$_SESSION["student"])
				return 2;
			else
			{
				session_unset();
				show_message("'You are not logged in.'");
			}

		break;
	}

}


function getMNS($alumni,$dbcon)// to get the no of students to be taken for mentorship
{
	$table="mentor_data";
	$fields="num_students";
	$where_condition="username = '$alumni'";
	$num=retrieveFromDb($dbcon,$table,$fields,$where_condition);

	return $num;
}

function getMaxStudents($alumni,$dbcon)// to get the max no of allowed applications to be viewed
{
	$num =getMNS($alumni,$dbcon);

	if($num)
	{
		$num_students=$num[0][0];
		$max_students= 3 * $num_students;
	}
	else
		$max_students=15;

	return $max_students;
}

function getAlumniStatus($alumni,$dbcon)// for finding the current atatus of application queue
{
	$table="mentorship";
	$fields="count(*)";
	$where_condition="alumni = '$alumni' and status!='A-'";
	$count=retrieveFromDb($dbcon,$table,$fields,$where_condition);
	$c =$count[0][0];

	$max = getMaxStudents($alumni,$dbcon);
	
	if($c<$max)
		return "O";
	else if($c<($max+5))
		return "WL";
	else
		return "C";
}

function getMentorshipStatus($alumni,$dbcon)// for finding if all the mentorship slots of an alumni have been filled
{
	$max = getMNS($alumni,$dbcon);
	$current_no = retrieveFromDb($dbcon,"mentorship","count(*)","alumni = '$alumni' and status='F'");

	if($current_no==$max)
		return 1;
	else
		return 0;
}

function getCodeValue($code,$dbcon)
{
        $code_value=retrieveFromDb($dbcon,"codes_used","value","code='$code'");
        $value=$code_value[0][0];
	return $value;
}

function getStudentStatus_Al($alumni,$student,$dbcon) // for finding student status with respect to a particular alumni
{
	$table="mentorship";
	$fields="status";
	$where_condition="alumni = '$alumni' and student = '$student'";
	$status=retrieveFromDb($dbcon,$table,$fields,$where_condition);
	if($status)
	{
		$sts = $status[0][0];	
		$value=getCodeValue($sts,$dbcon);
		return $value;
	}
	else
		return "Not Defined"; 
}

function getStudentStatus($student,$dbcon)               //for finding how may alumni has student applied to.
{
	$query ="Select count(*) from mentorship where student='$student' and status!='A-'";
	$execute =pg_query($dbcon,$query);
	$row =pg_fetch_array($execute);
	$c = $row[0];
	return $c;
}

function updateStudentStatus($student,$alumni,$sts,$dbcon)// for changing the student status wrt an alumni
{
	$query="Update mentorship set status='$sts' where student = '$student' and alumni = '$alumni'";
	$execute_query = pg_query($dbcon,$query);
}

function updateAl_sts($alumni,$dbcon) // for updating student from wl to O on a student being rejected
{
	$query1="Select student from mentorship where alumni=$alumni and al_sts='WL' order by timst limit 1";
	$execute_query_1 = pg_query($dbcon,$query1);
	$row=pg_fetch_row($execute);
	$student=$row[0];

	$query2="Update mentorship set al_sts = 'O' where student = '$student' and alumni = '$alumni'";
	$execute_query_2 = pg_query($dbcon,$query2);

	$query3="Update student_data set wl=0 where username='$student'";
	$execute_query_3 = pg_query($dbcon,$query3);
}

function deleteOtherAppsOfStudent($student,$dbcon)// for deleting other apps of student when he gets finalized
{
	$check=retrieveFromDb($dbcon,"mentorship","count(*)","student='$student' and status='F'");
	$sts=$check[0][0];
	if($sts==1)
	{
		$delete_query="Delete from mentorship where student='$student' and (status='A' or status='A-')";
		$execute_query=pg_query($dbcon,$delete_query);
		
		$update_query="Update mentorship set status ='X' where student='$student'and status ='A+'";
		$execute_query=pg_query($dbcon,$update_query);
	}
}

function chkStudentFilledData($student,$dbcon) // for checking if student_data has been filled
{
	$query ="Select * from student_data where username='$student'";
	$execute =pg_query($dbcon,$query);
	$row=pg_fetch_array($execute);

	if(empty($row))
		return 0;
	else 
		return 1;
}

function notifyOtherStudentApplicants($alumni,$dbcon) // for notifying those whose applications got rejected as alumni finalised his quota
{
	$update_query="Update mentorship set status ='A-' where alumni='$alumni' and (status ='A' or status='A+')";
	$execute_query=pg_query($dbcon,$update_query);

	$query ="Select * from mentorship where alumni='$alumni' and al_sts='WL' and status='A-'";
	$execute=pg_query($dbcon,$query);

	while($row=pg_fetch_array($execute))
	{
		$update = "Update student_data set wl=0 where username='".$row['student']."'";
		$execute_update($dbcon,$update);
	}
}

function MentorshipAscess($student,$dbconchanneli)
{

  $fields = "nperson.semester as course" ;
  $student_id = $student ;
  $getInfo = getStudentDetails($dbconchanneli, $fields, $student_id);
	$course = $getInfo[0][0];
	$year=substr($course,2,1);
	$degree = substr($student,5,1);

	if($degree=='u')
	{
		if(($year=='3')||($year=='4')||($year=='5'))
			return 1;
		else 
			return 0;
	}
	else 
		return 0;
}

function returnName($student,$dbconchanneli)
{

  $fields = 'nperson.name';
  $student_id = $student ;
  $name = getStudentDetails($dbconchanneli , $fields, $student_id);
	$fullname=$name[0][0];

	return $fullname;
}

function ImageResize($location)
{
        $identify =shell_exec("identify $location");
	$size = explode(" ",$identify);
	$k = explode("x",$size[2]);
	$width =  $k[0];
        $height = $k[1];

	if($height>$width)
	{
		$ratio = $width/$height;
		$height=150;
		$width= $ratio*$height;
	}
	else
	{
		$ratio = $height/$width;
		$width=150;
		$height= $ratio*$width;
	}

	shell_exec("convert $location -resize ".$width."x".$height." $location");
}

function MentorshipAscessOfAlumni($alumni,$dbcon)
{
	$query="Select status from basic_data where username='$alumni'";
	$execute=pg_query($dbcon,$query);

	$row=pg_fetch_array($execute);
	$sts=$row['status'];

	if($sts=='A')
		return 1;
	else 
		return 0;
}

?>
