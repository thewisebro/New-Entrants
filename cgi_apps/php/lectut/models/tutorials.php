<?php

class tutorial extends baseinfo
{
	
/*-----------Constructor functions-----------*/
	function __construct($id,$fId,$cId,$fil,$top,$perm)
	{
		parent::__construct($id,$fId,$cId,$fil,$top,$perm);
	}	

/*---------Upload-------------*/

	public function uploadTut()
	{
		$query="INSERT INTO ".TUT_TABLE." (".FACULTY_ID.", ".COURSE_ID.", ".FILENAME.", ".TOPIC.", ".PERMISSION.") VALUES('$this->faculty_id', '$this->course_id', '$this->file', '$this->topic', $this->permission);";
	
		return $query;
	}

/*--------------Delete---------------*/

	public function deleteTut()
	{
		$query="DELETE FROM ".TUT_TABLE." WHERE ".ID."='$this->id';";	
		return $query;
	}
}	

?>
