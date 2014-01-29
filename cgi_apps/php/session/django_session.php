<?php
error_reporting('E_ALL');
include("connection.php");
class Session {
  private $db_conn;
  private $table;
  private $session_id;
  private $redirect_url;
  private $user;

  public function __construct() {
    $this->db_conn = db();
    $this->table = "nucleus_php_session";
    $this->next_url = $_SERVER['REQUEST_URI'];
    $this->redirect_url = "/nucleus/login/?next=".$this->next_url;
    $this->user = NULL;

    /*
      Set session handlers
    */

    session_set_save_handler(
			     array(&$this, 'open'),
			     array(&$this, 'close'),
			     array(&$this, 'read'),
			     array(&$this, 'write'),
			     array(&$this, 'destroy'),
			     array(&$this, 'gc'));

    session_start();
  }

  public function open($path, $session_name) {
    /*
      Check if the connection to database is established or not.
    */

    $session_id = session_id();
    $query = "select * from nucleus_php_session where session_key = '".$session_id."'";
    $result = mysql_query($query, $this->db_conn);

    /*
       Check if the query returned non zero row, if not
       sessoin doesn't exist and redirect to login page
    */

    $num_rows = mysql_num_rows($result);
    if($num_rows == 0)
      header("Location: ".$this->redirect_url);

    if($this->db_conn)
      return TRUE;
    else
      return FALSE;
  }

  public function close() {
    /*
      Close mysql connection
    */

    mysql_close($this->db_conn);
  }

  public function gc($time) {
    /*
      TODO:

      Complete this function with proper expire date
    */

    return TRUE;
  }

  public function read($session_id)
  {
    $query = "select * from nucleus_php_session where session_key = '".$session_id."'";
    $result = mysql_query($query, $this->db_conn);

    /*
       Check if the query returned non zero row, if not
       sessoin doesn't exist and redirect to login page
    */

    $num_rows = mysql_num_rows($result);
    if($num_rows == 0)
      header("Location: ".$this->redirect_url);

    /*
      Get sessoin data
    */

    $row = mysql_fetch_assoc($result);
    $session_data = unserialize($row['session_data']);
    return $session_data;

  }

  public function write($session_id, $session_data) {

    /*
      Sanity checks
    */

    $query = "select * from nucleus_php_session where session_key = '".$session_id."'";
    $result = mysql_query($query, $this->db_conn);

    /*
       Check if the query returned non zero row, if not
       sessoin doesn't exist and redirect to login page
    */

    $num_rows = mysql_num_rows($result);
    if($num_rows == 0)
      header("Location: ".$this->redirect_url);

    /*
       Everything looks fine, now change session data
    */

    $session_data = serialize($session_data);
    $query = "update nucleus_php_session set session_data =
             '".$session_data."' where session_key = '".$session_id."'";
    $result = mysql_query($query, $this->db_conn);

    if($result) {
      return TRUE;
    }
    else {
      return FALSE;
    }
  }

  public function destroy($session_id) {
    /*
      Do nothing here, session is destroyed by django
    */
  }

  public function isloggedin() {
    $session_id = session_id();
    $query = "select * from nucleus_php_session where session_key = '".$session_id."'";
    $result = mysql_query($query, $this->db_conn);
    $num_rows = mysql_num_rows($result);
    if($num_rows == 0) {
      return FALSE;
    }

    $row = mysql_fetch_assoc($result);
    if($row['username'])
      return TRUE;
    else
      return FALSE;
  }

  public function get_userid() {

    $session_id = session_id();
    $query = "select * from nucleus_php_session where session_key = '".$session_id."'";
    $result = mysql_query($query, $this->db_conn);
    $num_rows = mysql_num_rows($result);
    if($num_rows == 0)
      return NULL;
    $row = mysql_fetch_assoc($result);
    if(!$row)
      return NULL;
    $username = $row['username'];
    $query = "select * from nucleus_personidenrollmentnomap where enrollment_no = '".$username."'";
    $result = mysql_query($query, $this->db_conn);
    $num_rows = mysql_num_rows($result);
    if($num_rows == 0)
      return NULL;
    $row = mysql_fetch_assoc($result);
    if(!$row)
      return NULL;
    return $row['person_id'];
  }

  public function get_username() {

    $session_id = session_id();
    $query = "select * from nucleus_php_session where session_key = '".$session_id."'";
    $result = mysql_query($query, $this->db_conn);
    $num_rows = mysql_num_rows($result);
    if($num_rows == 0)
      return NULL;

    $row = mysql_fetch_assoc($result);
    if(!$row)
      return NULL;

    return $row['username'];
  }

/*  public function get_nucleus_user_id($username) {
    $query = "select * from nucleus_user where username = '".$username."'";
    $result = mysql_query($query, $this->db_conn);
    $num_rows = mysql_num_rows($result);
    if($num_rows == 0)
      return NULL;
    $row = mysql_fetch_assoc($result);

    if(!$row)
      return NULL;
    return $row['id'];
  }
*/
  public function get_group() {

    if(!$this->isloggedin())
      return NULL;

    $username = $this->get_username();
    if(!$username)
      return NULL;

    $query_group = "select name from auth_group where id in (select group_id from nucleus_user_groups where user_id=(select id from auth_user where username='".$username."'))";
    $result = mysql_query($query_group, $this->db_conn);
    $num_rows = mysql_num_rows($result);
    if($num_rows == 0)
      return NULL;

    $group=array();

    while($row = mysql_fetch_assoc($result))
    {
      if($row['name']!="")
      {
        array_push($group,$row['name']);
      }
    }

    return $group;
  }

  public function get_user_info() {
    if(!$this->isloggedin())
      return NULL;

    $username = $this->get_username();
    if(!$username)
      return NULL;

    $group = $this->get_group();
    if(empty($group))
      return NULL;

    $query_userinfo = "select * from nucleus_user where username='".$username."'";
    $result = mysql_query($query_userinfo, $this->db_conn);
    if(!$result)
      return NULL;

    $rows_assoc = mysql_fetch_assoc($result);
    return $rows_assoc;
  }
}
?>
