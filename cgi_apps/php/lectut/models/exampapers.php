<?php

class exampaper extends baseinfo
{
	protected $year;

/*-----------Constructor functions-----------*/
	function __construct($id,$fId,$cId,$fil,$top,$perm,$year)
	{
		parent::__construct($id,$fId,$cId,$fil,$top,$perm);
		$this->year=$year;
	}	

/*-----------Set Functions-----------*/
	public function setYear($year)
	{
		$this->year=$year;
	}

/*-----------Get Functions-------------*/

	public function getYear()
	{
		return $this->year;
	}

/*------------Upload------------*/

	public function uploadExamPaper()
	{
		$query="INSERT INTO ".EXAM_TABLE." (".FACULTY_ID.", ".COURSE_ID.", ".FILENAME.", ".TOPIC.", ".PERMISSION.", ".YEAR.") VALUES('$this->faculty_id', '$this->course_id', '$this->file', '$this->topic', $this->permission,'$this->year');";

		return $query;
	}

/*-----------Delete---------------*/

	public function deleteExamPaper()
	{
		$query="DELETE FROM ".EXAM_TABLE." WHERE ".ID."='$this->id';";	
		return $query;
	}


}
?>
