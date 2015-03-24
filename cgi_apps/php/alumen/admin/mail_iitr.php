<?


function email_to_user($to, $from='img@iitr.ernet.in', $subject='', $messagetext='', $messagehtml='', $fromname='', $fname1='', $fname2='', $fname3='')
{
$usetrueaddress=true;
include_once('../phpmailer/class.phpmailer.php');
$mail = new phpmailer;
$mail->PluginDir = '../phpmailer/';
$mail->CharSet = 'UTF-8';
$mail->IsSMTP();
$mail->Host = '192.168.121.26';
$mail->SMTPAuth = false;
$mail->From = $from;
$mail->FromName = $fromname;
$mail->AddReplyTo('noreply@iitr.ernet.in','NO REPLY');
$mail->Subject = substr(stripslashes($subject), 0, 900);
$mail->AddAddress($to); // now, i'll have to check if this works for multiple mails, or do i have to do a for loop, or if calling this multiple times, adds multiple users...

#$mail->AddAttachment('/home/apps/php/groupmailer/temp_loc/'.$fname1,$fname1);
#$mail->AddAttachment('/home/apps/php/groupmailer/temp_loc/'.$fname2,$fname2);
#$mail->AddAttachment('/home/apps/php/groupmailer/temp_loc/'.$fname3,$fname3);
$mail->WordWrap = 79;
$mail->IsHTML(true);
$mail->Encoding = 'quoted-printable';
$mail->Body    =  $messagehtml;
$mail->AltBody =  "\n$messagetext\n";
$mail->Send();
}
function email_to_user_multi($to, $from='noreply@iitr.ernet.in', $subject='No Subject', $messagetext='', $messagehtml='', $fromname) {
$to_field=explode(",",$to);
$total=count($to_field);
$usetrueaddress=true;
include_once('../phpmailer/class.phpmailer.php');
$mail = new phpmailer;
$mail->PluginDir = '../phpmailer/';
$mail->CharSet = 'UTF-8';
$mail->IsSMTP();
$mail->Host = 'people.iitr.ernet.in';
$mail->SMTPAuth = false;
$mail->From = $from;
$mail->FromName = $fromname;
$mail->AddReplyTo('noreply@iitr.ernet.in','NO REPLY');
$mail->Subject = substr(stripslashes($subject), 0, 900);
for($i=0;$i<$total;$i++){
$mail->AddAddress($to_field[$i]); // now, i'll have to check if this works for multiple mails, or do i have to do a for loop, or if calling this multiple times, adds multiple users...
}
$mail->WordWrap = 79;
$mail->IsHTML(true);
$mail->Encoding = 'quoted-printable';
$mail->Body    =  $messagehtml;
$mail->AltBody =  "\n$messagetext\n";
$mail->Send();
return 1;

}
?>
