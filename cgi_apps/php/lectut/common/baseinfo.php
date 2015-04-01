<?php

class baseinfo
{
	protected $id;
	protected $faculty_id;
	protected $course_id;
	protected $file;
	protected $topic;
	protected $permission;
	protected $timestamp;

/*----------Constructor Functions------------*/
	function __construct($id,$facId,$courseId,$file,$topic,$permit)
	{
		$this->id=$id;
		$this->faculty_id=$facId;
		$this->course_id=$courseId;
		$this->file=$file;
		$this->topic=$topic;
		$this->permission=$permit;
	}

/*--------Set Functions---------*/

	public function setId($id)
	{
		$this->id=$id;
	}

	public function setFile($name)
	{
		$this->file=$name;
	}

	public function setTopic($topic)
	{
		$this->topic=$topic;
	}

	public function setPermission($permit)
	{
		$this->permission=$permit;
	}
	
	public function setCourseId($courseId)
	{
		$this->course_id=$courseId;
	}

	public function setFacultyId($facId)
	{
		$this->faculty_id=$facId;
	}

/*--------Get Functions---------*/
	public function getId()
	{
		return $this->id;
	}
	
	public function getFacultyId()
	{
		return $this->faculty_id;
	}
	
	public function getCourseId()
	{
		return $this->course_id;
	}
	
	public function getFile()
	{
		return $this->file;
	}
	
	public function getTopic()
	{
		return $this->topic;
	}
	
	public function getPermission()
	{
		return $this->permission;
	}
	
	public function getTimestamp()
	{
		return $this->timestamp;
	}
}
?>
