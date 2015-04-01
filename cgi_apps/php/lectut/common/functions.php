<?php
//session_start();
include_once("database.php");

/**function pop_authenticate( $username, $password, $auth_host )
{
	$tcp_port = "110";    // POP Server port, usually 110

	$fp = fsockopen( "$auth_host",$tcp_port );  // connect to pop port
	if ( $fp > 0 )  // make sure that you get a response...
	{
		$user_info=fputs( $fp, "USER ".$username. "\r\n" ); //send username
		if ( !$user_info )
		{
			// print  "problem conversing with $auth_host!";


			return false;
		}
		else
		{

			$server_reply = fgets( $fp,128 );
			if ( ord($server_reply) == ord( "+" ))
			{
				// print "$server_reply......<br>";
			}

			$server_reply = fgets( $fp,128 );
			if ( ord( $server_reply ) == ord( "+" ))
			{
				// print "$server_reply.........<br>";
				fputs( $fp, "PASS ".$password. "\r\n" );
				$passwd_attempt = fgets( $fp,128 );
				if ( ord( $passwd_attempt ) == ord( "+" ))
				{
					// print "$passwd_attempt!"; //password accepted
					return true;
				}
				else
				{
					// print "$passwd_attempt!"; //password failed
					return false;
				}
			}
			fputs( $fp, "QUIT". "\r\n" );
			fclose( $fp );
		}
	}
	else //if you don't get a response, complain...
	{
		// print  "<BR>No response from $auth_host! is port $tcp_port open?....";
		return false;
	}
}

function session_create($username,$session_id)
{
	database::connectToDatabase("intranet5");
	if(!$session_id)
	{
		$session_id=time();
		$_SESSION['sessionid']=$session_id;
		$query="Delete from session_id where username='$username';";
		if(!database::executeQuery("intranet5",$query))
			header("Location: logout.php");
		$query="Insert into session_id(username,sessionid) values('$username','$session_id')";
		if(!database::executeQuery("intranet5",$query))
			header("Location: logout.php");
	}
	else
	{
		$_SESSION['sessionid']=$session_id;
	}
	database::closeDatabase("intranet5");
}

function isLogin($username,$sessionid) 
{
	database::connectToDatabase("intranet5");
	$query = "SELECT * FROM session_id WHERE username='$username' and sessionid='$sessionid';";
	$i = mysql_num_rows(database::executeQuery("intranet5",$query));
	if($i == 0)
		{
			session_destroy();
			return false;
		}
	else return ($username && $sessionid);
	database::closeDatabase("intranet5");
}
*/
function sanitize($var) 
{
	return addslashes(htmlspecialchars($var));
}

function secure($input)
{
	$special=array("`","~","!","@","#","$","%","^","&","*","(",")","_","=","+","\\","|","]","}","[","{","'","\"",";",":","/","?",">",",","<",".");
	
	$fileSpecial=array("`","~","!","@","#","$","%","^","*","=","+","\\","|","'","\"",";",":","/","?",">",",","<");

	$input=str_replace($special," ",$input);
	
	$input=htmlspecialchars($input);
	
	if(get_magic_quotes_gpc())
		$input=stripslashes($input);
	
	return $input;
}

function secureCode($code)
{
	if($code!="")
	{
		$code=secure($code);
	
		$code=str_ireplace(" ","",$code);
	
		$code=strtoupper($code);
	
		preg_match_all("/[A-Z]+/",$code,$pattern1);
		preg_match("/[0-9]+/",$code,$pattern2);
		$code=$pattern1[0][0]."-".$pattern2[0].$pattern1[0][1];
	
	}
		
	return $code;
}

function search_split_terms($terms)
{
	$terms = preg_replace("/\"(.*?)\"/e", "search_transform_term('\$1')", $terms);
	$terms = preg_split("/\s+|,/", $terms);
	$out = array();
	foreach($terms as $term)
	{
		$term = preg_replace("/\{WHITESPACE-([0-9]+)\}/e", "chr(\$1)", $term);
		$term = preg_replace("/\{COMMA\}/", ",", $term);
		if(strlen($term)>=2)
		{
			$temp=secureCode($term);
			if($row=mysql_fetch_array(database::executeQuery(database::getDistinctId(COURSE_DETAILS_ID,REGISTERED_COURSES,"WHERE ".COURSE_DETAILS_ID."='$temp'"))))
				$out[]=$row[0];
			else
				$out[]=$term;
		}
	}
	return $out;
}

function search_transform_term($term)
{
	$term = preg_replace("/(\s)/e", "'{WHITESPACE-'.ord('\$1').'}'", $term);
	$term = preg_replace("/,/", "{COMMA}", $term);
	return $term;
}

function search_facname($names)
{
	$facIds=array();
	foreach($names as $name)
	{
		if(strlen($name)>2)
		{
			$result = database::executeQuery(database::searchFac($name));
			while($row = mysql_fetch_array($result))
			{
				array_push($facIds,$row[0]);
			}
		}
	}
	array_unique($facIds);
	return $facIds;
}

function search_perform($terms,$table)
{
	$term = search_split_terms($terms);
	$rows = array();
	$facnames=search_facname($term);
	$term=array_merge($term,$facnames);
	switch($table)
	{
		case 'lec':
			$search="searchLec";
			foreach($term as $terms)
			{
				$len=strlen($terms);
				$terms_c=secureCode($terms);
				if($len==2)
				{
					$result = database::executeQuery(database::$search(null,$terms_c));
				}
				else
				{
					$result = database::executeQuery(database::$search($terms,$terms_c));
				}
				
        while($row = mysql_fetch_array($result))
        {
					$return_lec=database::getLecObject(ID,$row[0]);	
					array_push($rows,$return_lec);
				}
			}
			break;
		case 'tut':
			$search="searchTut";
			foreach($term as $terms)
			{
				$len=strlen($terms);
				$terms_c=secureCode($terms);
				if($len==2)
				{
					$result = database::executeQuery(database::$search(null,$terms_c));
				}
				else
				{
					$result = database::executeQuery(database::$search($terms,$terms_c));
				}
				while($row = mysql_fetch_array($result))
				{
					$return_lec=database::getTutObject(ID,$row[0]);	
					array_push($rows,$return_lec);
				}
			}
			break;
		case 'exam':
			$search="searchExamPaper";
			foreach($term as $terms)
			{	
				$len=strlen($terms);
				$terms_c=secureCode($terms);
				if($len==2)
				{
					$result = database::executeQuery(database::$search(null,$terms_c));
				}
				else
				{
					$result = database::executeQuery(database::$search($terms,$terms_c));
				}
				while($row = mysql_fetch_array($result))
				{
					$return_lec=database::getExamPaperObject(ID,$row[0]);	
					array_push($rows,$return_lec);
				}
			}	
			break;
		case 'soln':
			$search="searchSoln";
			foreach($term as $terms)
			{
				$len=strlen($terms);
				$terms_c=secureCode($terms);
				if($len==2)
				{
					$result = database::executeQuery(database::$search(null,$terms_c));
				}
				else
				{
					$result = database::executeQuery(database::$search($terms,$terms_c));
				}
				while($row = mysql_fetch_array($result))
				{
					$return_lec=database::getSolnObject(ID,$row[0]);	
					array_push($rows,$return_lec);
				}
			}	
			break;
	}
	$rows = array_map('unserialize', array_unique(array_map('serialize', $rows)));
	return $rows;
}

function disp_fac_upload($loggedIn,$facId)
{
     if($loggedIn!=0 && $facId)
     {
                 echo "<div class=\"curve_edge_lt\"></div>
             <div class=\"link\"><a href=\"faculty.php?username=$facId\">Upload files</a></div>
             <div class=\"curve_edge_rt\"></div>";
         }
 
}
 
function disp_fac_logout($loggedIn,$facId)
{
     if($loggedIn!=0 && $facId)
         {
         echo "<div class=\"curve_edge_lt\">&nbsp;</div>
         <div class=\"link\"><a href=\"nucleus/logout\" >Logout</a></div>
         <div class=\"curve_edge_rt\">&nbsp;</div>";
         }
}
 
function disp_fac_design_choice($loggedIn,$facId)
{
     if($loggedIn!=0 && $facId)
     {
                 echo "<div class=\"curve_edge_lt\"></div>
             <div class=\"link\"><a href=\"../pages_old/switch_design.php\">Switch to new LecTut</a></div>
             <div class=\"curve_edge_rt\"></div>";
     }
}
/*
function get_role($username)
{
     $query = "SELECT id from auth_user where username='$username'";
     $id = mysql_fetch_array(database::executeQuery($query));
     $query = "SELECT group_id from auth_user_groups where user_id='$id[0]'";
     $group_id = mysql_fetch_array(database::executeQuery($query));
     $query = "SELECT name from auth_group where id='$group_id[0]'";
     $group = mysql_fetch_array(database::executeQuery($query));
     return $group 
}
*/

function secureType($name)
{
	/*$types=array{};
	$parts=explode(".",$name);
	$type=strtolower($parts[count($parts)-1]);
	if(in_array($type,$types))
		return 1;
	else
		return 0;*/
/*	if($name)
	{
		if(preg_match("/^(doc|)/",$name))
			return 1;
		else
			return 0;	
	}*/
//	$types=array{};
	preg_match("/\.([^\.]+)$/",$name,$matches);
//	if(in_array($matches[0],$types))
//		return 1;
//	else
//		return 0;
}		
?>
