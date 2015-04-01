<?php

class solution extends baseinfo
{
	protected $link_type;
	protected $link_id;

/*-----------Constructor functions-----------*/
	function __construct($id,$fId,$cId,$fil,$top,$perm,$linkType,$linkId)
	{
		parent::__construct($id,$fId,$cId,$fil,$top,$perm);
		$this->link_type=$linkType;
		$this->link_id=$linkId;
	}	

/*-----------Set Functions-----------*/
	public function setLink($linkType,$linkId)
	{
		$this->link_type=$linkType;
		$this->link_id=$linkId;
	}

/*----------Get Functions--------*/

	public function getLink()
	{
		return $this->link_type.$this->link_id;
	}

/*---------Delete----------*/

	public function deleteSolution()
	{
		$query="DELETE FROM ".SOLN_TABLE." WHERE ".ID."='$this->id';";	
		return $query;
	}
	
/*---------Upload---------------*/

	public function uploadSolution()
	{
		$query="INSERT INTO ".SOLN_TABLE." (".FACULTY_ID.", ".COURSE_ID.", ".FILENAME.", ".TOPIC.", ".PERMISSION.", ".LINK_TO.", ".LINK_TYPE.") VALUES('$this->faculty_id', '$this->course_id', '$this->file', '$this->topic', $this->permission, $this->link_id, '$this->link_type');";

		return $query;	
	}


}
?>
