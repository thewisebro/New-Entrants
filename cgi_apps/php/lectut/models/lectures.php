<?php
include_once('../common/constants.php');
include_once('../common/baseinfo.php');

class lecture extends baseinfo
{

/*-----------Constructor functions-----------*/
	function __construct($id,$fId,$cId,$fil,$top,$perm)
	{
		parent::__construct($id,$fId,$cId,$fil,$top,$perm);
	}		

/*---------Upload---------*/

	public function uploadLec()
	{
		$query="INSERT INTO ".LEC_TABLE." (".FACULTY_ID.", ".COURSE_ID.", ".FILENAME.", ".TOPIC.", ".PERMISSION.") VALUES('$this->faculty_id', '$this->course_id', '$this->file', '$this->topic', $this->permission);";
    
    return $query;
	}

/*---------Delete---------*/

	public function deleteLec()
	{
		$query="DELETE FROM ".LEC_TABLE." WHERE ".ID."=$this->id;";	
		return $query;
	}
}
?>
