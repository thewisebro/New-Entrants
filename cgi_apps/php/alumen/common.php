<?php
require("pop-authenticate.php");

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

	$_SESSION["username"]=$formInfo["username"];
	
	if(pg_query($dbcon,$submit_query)!=FALSE && $destination!="null")
	{
		echo "<script language='javascript'>";
		echo "document.location+='#$destination';";
		echo "updateInfo('$destination')";
		echo "</script>";

	}
	

}

function retrieveFromDb($dbcon,$table,$fields,$where_condition)
{
	//Basic Query Structure
	$select_query="select $fields from $table where $where_condition";
	$select_result=pg_query($dbcon,$select_query);
	$main_result=array();
	if($select_result!=FALSE)
	{
		while($select_array=pg_fetch_array($select_result))
			$main_array[]=$select_array;
		return $main_array;	
	}
	else
		echo "An error occurred. Please report this error in 'Report a Bug' section";
}

function verifyOldPassword($dbcon,$table,$old_password,$username){
	$check_query="Select password from ".$table." where username='".$username."'";
	$result=pg_fetch_row(pg_query($check_query));
	if($result[0]==$old_password){
		return true;
	}else{
		return false;
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
	$check_query="select * from mentor_data where username='$username'";	

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
	$update_query="insert into mentor_data ([fields]) values ([values])";
	}			
	$update_query=str_replace("[fields]",$fields,$update_query);
	$update_query=str_replace("[values]",$values,$update_query);
//update_query=str_replace("[where_condition]",$where_condition,$update_query);
	
	if(pg_query($dbcon,$update_query)!=FALSE && $destination!="null")
	{
		echo "<script language='javascript'>";
		echo "document.location+='#$destination';";
		echo "updateInfo('$destination')";
		echo "</script>";

	}
	else if($destination!="null")
	{
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
?>
