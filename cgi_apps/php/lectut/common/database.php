<?php
//error_reporting(E_ALL);
include("../models/lectures.php");
include("../models/tutorials.php");
include("../models/exampapers.php");
include("../models/solutions.php");

class database
{
  private static $conn;
	
  public static function connectToDatabase()
  {
	  self::$conn=mysql_connect("192.168.121.9", "lectut", "lectuT");
    if (!self::$conn) {
          die('Could not connect: ' . mysql_error());
    }
    mysql_select_db("channeli", self::$conn);
	}
	
	public static function closeDatabase()
	{
	  mysql_close(self::$conn);
	}
	
	public static function executeQuery($query)
  {
    return mysql_query($query,self::$conn);
	}

	public static function getLecObject($column,$value,$cond)
	{
		$query=self::getLec($column,$value,$cond);
		$returnRow=self::executeQuery($query);
		$result=array();
		while($row=mysql_fetch_array($returnRow))
		{
			$lec=new lecture($row[0],$row[1],$row[2],$row[4],$row[3],$row[5]);
			array_push($result,$lec);	
		}
		return $result;
	}

	public static function getTutObject($column,$value,$cond)
	{
		$query=self::getTut($column,$value,$cond);
		$returnRow=self::executeQuery($query);
		$result=array();
		while($row=mysql_fetch_array($returnRow))
		{
			$tut=new tutorial($row[0],$row[1],$row[2],$row[4],$row[3],$row[5]);
			array_push($result,$tut);	
		}
		return $result;
	}

	public static function getExamPaperObject($column,$value,$cond)
	{
		$query=self::getExamPaper($column,$value,$cond);
		$returnRow=self::executeQuery($query);
		$result=array();
		while($row=mysql_fetch_array($returnRow))
		{
			$exampaper=new exampaper($row[0],$row[1],$row[2],$row[4],$row[3],$row[5],$row[6]);
			array_push($result,$exampaper);	
		}
		return $result;
	}

	public static function getSolnObject($column,$value)
	{
		$query=self::getSoln($column,$value);
		$returnRow=self::executeQuery($query);
		$result=array();
		while($row=mysql_fetch_array($returnRow))
		{
			$soln=new solution($row[0],$row[1],$row[2],$row[4],$row[3],$row[5],$row[6]);
			array_push($result,$soln);	
		}
		return $result;
	}

	public static function getDesignChoice($user)
	{
		$query="SELECT ".ID.", ".FACULTY_ID.", ".DESIGN_CHOICE." FROM ".DESIGN_TABLE." WHERE ".FACULTY_ID."='$user';";

		return $query;
	}

	public static function insertDesignChoice($user,$choice)
	{
		$query="INSERT INTO ".DESIGN_TABLE." (".FACULTY_ID.", ".DESIGN_CHOICE.") VALUES('$user','$choice');";

		return $query;
	}

	public static function deleteDesignChoice($user)
	{
		$query="DELETE FROM ".DESIGN_TABLE." WHERE ".FACULTY_ID."='$user';";

		return $query;
	}

/*-----------Student Queries--------------*/

	public static function studQuery($studId)
	{
//		$query="SELECT p.".USER_ID.", r.".COURSE_DETAILS_ID." FROM ".PERSON." p, ".REGISTERED_COURSES." r WHERE p.".USER_ID."=r.".PERSON_ID." AND p.".SEMESTER."=r.".SEMESTER." AND p.".USER_ID."='$studId';";

		$query="SELECT p.".USER_ID.", r.".COURSE_DETAILS_ID." FROM ".PERSON." p, ".REGISTERED_COURSES." r WHERE p.".USER_ID."=r.".PERSON_ID." AND r.".CLEARED_STATUS."='".CUR."' AND p.".USER_ID."='$studId';";

    //		$query="SELECT p.".PERSON_ID.", c.".COURSE_CODE." FROM ".PERSON_VIEW." p, ".CURR_STRUC." c WHERE p.".DISCIPLINE."=c.".DISCIPLINE." AND c.".COURSE."=p.".COURSE." AND p.".PERSON_ID."='$studId'";
    
    return $query;
	}

//Here $studId is get_user_info('user_id')
	public static function getStudName($studId)
	{
		$query="SELECT ".NAME." FROM ".PERSON." WHERE ".USER_ID."='$studId';";
		
    return $query;
	}

/*------------Intranet Queries--------------*/

	public static function getLec($column,$value,$condition)
	{
		$query="SELECT ".ID.", ".FACULTY_ID.", ".COURSE_ID.", ".TOPIC.", ".FILENAME.", ".PERMISSION." from ".LEC_TABLE." where ".$column."='$value' $condition;";		
		return $query;
	}
	
	public static function getTut($column,$value,$condition)
	{
		$query="SELECT ".ID.", ".FACULTY_ID.", ".COURSE_ID.", ".TOPIC.", ".FILENAME.", ".PERMISSION." from ".TUT_TABLE." where ".$column."='$value' $condition;";		
		return $query;
	}

	public static function getExamPaper($column,$value,$condition)
	{
		$query="SELECT ".ID.", ".FACULTY_ID.", ".COURSE_ID.", ".TOPIC.", ".FILENAME.", ".PERMISSION.", ".YEAR." from ".EXAM_TABLE." where ".$column."='$value' $condition;";

		return $query;
	}

	public static function getSoln($column,$value,$condition)
	{
		$query="SELECT ".ID.", ".FACULTY_ID.", ".COURSE_ID.", ".TOPIC.", ".FILENAME.", ".PERMISSION.", ".LINK_TO." from ".SOLN_TABLE." where ".$column."='$value' $condition;";

		return $query;
	}

/*------------------Search Queries-------------------*/

	public static function searchLec($search,$subcode)
	{
//		$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".LEC_TABLE." where ".TSV." @@ to_tsquery('$search') GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";

//		$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID.", ts_rank_cd(".TSV.",query) AS rank from ".LEC_TABLE.", to_tsquery('$search') AS query where ".TSV." @@ query GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID.",".TSV.",query ORDER BY rank DESC,".ID.";";
		
		if($search!=null)
		{
			$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".LEC_TABLE." where ".FACULTY_ID." LIKE '%$search%' OR ".COURSE_ID." LIKE '%$subcode%' OR ".FILENAME." LIKE '%$search%' OR ".TOPIC." LIKE '%$search%' GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
		}
		else
		{
			$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".LEC_TABLE." where ".COURSE_ID." LIKE '%$subcode%' GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
		}
    
    return $query;
	}
	
	public static function searchTut($search,$subcode)
	{
	//	$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".TUT_TABLE." where ".TSV." @@ to_tsquery('$search') GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";

//		$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID.", ts_rank_cd(".TSV.",query) AS rank from ".TUT_TABLE.", to_tsquery('$search') AS query where ".TSV." @@ query GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID.",".TSV.",query ORDER BY rank DESC,".ID.";";

	if($search!=null)
	{
  		$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".TUT_TABLE." where ".FACULTY_ID." LIKE '%$search%' OR ".COURSE_ID." LIKE '%$subcode' OR ".FILENAME." LIKE '%$search%' OR ".TOPIC." LIKE '%$search%' GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
	}
	else
	{
		$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".TUT_TABLE." where ".COURSE_ID." LIKE '%$subcode%' GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
	}
		return $query;
	}
	
	public static function searchExamPaper($search,$subcode)
	{
	//	$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".EXAM_TABLE." where ".TSV." @@ to_tsquery('$search') GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
	
//		$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID.", ts_rank_cd(".TSV.",query) AS rank from ".EXAM_TABLE.", to_tsquery('$search') AS query where ".TSV." @@ query GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID.",".TSV.",query ORDER BY rank DESC,".ID.";";
		
		if($search!=null)
		{
		  $query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".EXAM_TABLE." where ".FACULTY_ID." LIKE '%$search%' OR ".COURSE_ID." LIKE '%$subcode%' OR ".FILENAME." LIKE '%$search%' OR ".TOPIC." LIKE '%$search%' OR  ".YEAR." LIKE '%$search%' GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
		}
		else
		{
			$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".EXAM_TABLE." where ".COURSE_ID." LIKE '%$subcode%' GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
		}

		return $query;
	}
	
	public static function searchSoln($search,$subcode)
	{
		//$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".SOLN_TABLE." where ".TSV." @@ to_tsquery('$search') GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";

//		$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID.", ts_rank_cd(".TSV.",query) AS rank from ".SOLN_TABLE.", to_tsquery('$search') AS query where ".TSV." @@ query GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID.",".TSV.",query ORDER BY rank DESC,".ID.";";
		
		if($search!=null)
		{
		  $query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".SOLN_TABLE." where ".FACULTY_ID." LIKE '%$search%' OR ".COURSE_ID." LIKE '%$subcode%' OR ".FILENAME." LIKE '%$search%' OR ".TOPIC." LIKE '%$search%' GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
		}
		else
		{
			$query="SELECT ".ID.",".COURSE_ID.",".FACULTY_ID." from ".SOLN_TABLE." where ".COURSE_ID." LIKE '%$subcode%' GROUP BY ".COURSE_ID.",".FACULTY_ID.",".ID." ORDER BY ".ID.";";
		}

		return $query;
	}

/*----------Facappn Queries---------*/

	/*public static function getDeptList($facId)
	{
		$query="SELECT d.".DEPT_NAME." from ".FACULTY." g, ".DEPTS." d WHERE g.".FACULTY_ID."='$facId' AND g.".DEPT_CODE."=d.".DEPT_CODE.";";

		return $query;
	}*/

  public static function getDeptList($facId)
  {
    $deptList = array(
        "AHEC" => "Alternate Hydro Energy Centre", 
        "CNT" =>  "Centre for Nanotechnology",
        "ARCD" =>  "Architecture Department",
        "BTD" =>  "Biotechnology Department",
        "CHED" =>  "Chemical Engineering Department",
        "CYD" =>  "Chemistry Department",
        "CSED" => "Computer Science and Engineering Department",
        "CED" => "Civil Engineering Department",
        "EQD" =>  "Earthquake Department",
        "ESD" =>  "Earth Sciences Department",
        "EED" =>  "Electrical Engineering Department",
        "ECED" =>  "Electronics and Communication Department",
        "HSD" => "Humanities and Social Sciences Department",
        "HYD" => "Hydrology Department",
        "MSD" => "Management Studies Department",
        "MAD" => "Mathematics Department",
        "MIED" => "Mechanical and Industrial Engineering Department",
        "MMED" => "Metallurgical and Materials Engineering Department",
        "PTD" => "Paper Technology Department",
        "PHD" => "Physics Department",
        "WRDMD" => "Water Resources Development and Management Department"
          );
    $query = "SELECT ".ID." FROM ".AUTH." WHERE ".USER_NAME."='$facId';";
    $return = self::executeQuery($query);
    $retId = mysql_fetch_array($return);
    $query = "SELECT ".DEPARTMENT." FROM ".FACULTY." WHERE ".USER_ID."='$retId[0]';";
    $return = self::executeQuery($query);
    $retDept = mysql_fetch_array($return);
    return $deptList[$retDept[0]];
  }

//$facId is again the get_user_info('user_id')
	public static function getFacName($facId)
	{
		$query="SELECT ".NAME." FROM ".FACULTY." WHERE ".USER_ID."='$facId';";
	
		return $query;
	}

	public static function getFacUserId($facUsername)
	{
		$query="SELECT ".ID." FROM ".AUTH." WHERE ".USER_NAME."='$facUsername';";
	
		return $query;
	}

	public static function searchFac($name)
  {
		if($name!=null && $name!="")
		{
			$query="SELECT ".USER_NAME." from ".AUTH." where ".ID." IN (SELECT ".USER_ID." from ".FACULTY." where ".NAME." LIKE '%$name%');";
		}
    
    return $query;
	}

/*-------------General Queries----------------*/

	public static function getDistinctId($column,$table,$condition)
	{
		$query="SELECT DISTINCT(".$column.") FROM ".$table." ".$condition.";";
		
    return $query;
	}
	public static function getColumn($column,$table,$condition)
	{
		$query="SELECT $column FROM $table $condition";

		return $query;
	}
}

?>
