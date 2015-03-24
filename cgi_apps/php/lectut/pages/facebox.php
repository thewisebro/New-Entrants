
<div id="backy_fb" onclick="facebox_close();"></div>
<?php
/*
if($loggedIn!=0 && $_SESSION['welcome']!=1)
{

?>
<!-- faceboxes for first time users -->
<div id="login_fresh_show" style="display:none;">
<span class="cross" onclick="facebox_close();">X</span>
Welcome back !<br/>
Lectures &amp; Tutorials has been made easier to access with everything on one page. Now you get -
<ul>
<li>Sleek Design</li>
<?php
if($_SESSION['user']=='s')
{
   echo '<li>Provision for Registered Courses</li>';
}
if($_SESSION['user']=='f')
{
   echo '<li>Multiple Delete</li>
     <li>Upload Exam Papers and Solutions</li>';
}
?>
<li>Multiple Download</li>
<li>Keyboard Shortcuts : ? ( or Shift + / )</li>
Browsers : IE 8,9 and others
</ul>

</div>

<?php

$_SESSION['welcome']=1;
}
*/
?>
<div id="keyboard_shortcuts_facebox" style="display:none;">
<span class="cross" onclick="facebox_close();">X</span>

<b>Keyboard Shortcuts</b>

<ul>

<li> s : toggle search </li>
<li> Esc : close search box</li>
<li> ? or Shift + / : open this dialog box.</li>
<li> Less than ( &lt; ) : go back to last view</li>
<li> Use direction keys for navigation ( &larr; &amp; &rarr; ).</li>

</ul>

</div>


