<?php
//include('db_connection.php');

function pop_authenticate( $username, $password )
{
   $auth_host = "192.168.121.26";
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

?>
