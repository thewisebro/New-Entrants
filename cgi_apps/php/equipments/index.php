<?php
require 'files/connection.php';
require 'files/map.php';
?>
<div class="header">
<div class= "container">
<div class="app-name">
Institute Instruments Search
</div>

<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
<link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/themes/base/minified/jquery-ui.min.css" type="text/css" />
<script type="text/javascript" src="files/jquery.js"></script>
<script type="text/javascript" src="files/jquery-ui.js"></script>
<!--script type="text/javascript" src="files/auto.js"></script--!>
<?php
$dept = $_GET["value"];
$temp1 = $_GET["val1"];
$values = mysqli_query($var, "SELECT DISTINCT deptname FROM equip_entries");
echo "<select name= 'Departments' id='dropdown' onchange='getdept(this)'>";
echo "<option>Departments</option>";
while($row = mysqli_fetch_array($values))
{
    $temp=$row['deptname'];
    reset($arr);
    while (list($key, $val) = each($arr))
    {
      if($key==$temp)
      {
        echo "<option value='$temp'><a href='files/dept.php?val=$temp'>" .$val. "</a></option>";
      }
    }
    echo "<br>";
}
echo "</select>";
echo "<div class='search'> ";
echo "<form name='search' method='post' action=''> ";
echo "<link href='files/help.css' rel='stylesheet' type='text/css'>
<input type='text' name='abc' id='search-text'>
<img  class ='search-image' src='images/search.jpg'>
</div> ";
echo "</div>";
echo "</div>";

//to check if smethng is entered in the search bar
if(isset($_POST['abc']))
{
  $word=$_POST['abc'];
  $query1= mysqli_query($var, "SELECT * FROM equip_entries WHERE equipname LIKE '%$word%'");
  $temp1= $word;
}
if($temp1!=NULL)
{
  echo "<div class = 'container' wolworine>";
  echo "<table border='1' class='table table-striped results' >";
  echo "<div class ='equip-place'>";
  echo "<br><b>EQUIPMENTS-</b>";
  if(mysqli_num_rows($query1)==0)
  {
     echo "No results found";
  }
  echo "</div>";
  echo "<tr>
  <th>Equipment</th>
  <th>Professor</th>
  <th>Department</th>
  </tr>";
 while($row = mysqli_fetch_array($query1))
 {
       echo "<tr>";
       echo "<td class ='span6'>".$row['equipname']."</td>";
       echo "<td class ='span3'>".str_replace("\n","<br>",$row['profname'])."</td>";
       $temp=$row['deptname'];
       reset($arr);
       while (list($key, $val) = each($arr))
       {
          if($key==$temp)
          {
            echo "<td class ='span3'>".$val."</td>";
          }
       }
       echo "</tr>";
 }
 echo "<br>";
 echo "</div>";
}
else if($temp1==NULL && $dept==NULL)
{
  echo "<br>NO results found";
}
?>
<script>
 function getdept(elem)
 {
    var dept_code = $(elem).val();
    window.location.href = "index.php?value=" + dept_code;
 }
 $(function() {
        //autocomplete
        $("#search-text").autocomplete(
        {
          source: "files/auto.php",
          select: function( event, ui )
          {
               $("#search-text").val(ui.item.value);
               $("form[name=search]").submit();
          },            
          minLength: 2
        });
 });
</script>
<?php
if($temp1==NULL)
{
  reset($arr);
  while (list($key, $val) = each($arr))
  {
    if($dept==$key)
    {
      $dept_name = $val;
    }
  }
  echo "<div class='container'>";
  echo "<div class='dept-name'>";
  echo "<br><b>DEPARTMENT-";
  echo $dept_name;
  echo "</b><br>";
  echo "</div>";
  reset($arr);
  echo "<table border='1' class='table table-striped results'>";
  $values = mysqli_query($var, "SELECT * FROM equip_entries WHERE deptname='$dept'");
  echo "<tr>";
  echo "<th >Equipments</th>";
  echo "<th >Professor</th>";
  echo "</tr>";
  while($row = mysqli_fetch_array($values))
  {
      echo "<tr>";
      echo "<td class = 'span9'>".$row['equipname']."</td>";
      echo "<td class = 'span3'>".str_replace("\n","<br>",$row['profname'])."</td>";
      echo "</tr>";
  }
  echo "</table>";
  echo "</div>";
  echo "</form>";
}
echo "</form>";
echo "<div id='footer'>Copyright ".date('Y')." <a href='http://www.iitr.ac.in/campus_life/pages/Groups_and_Societies+IMG.html'>Information Management Group</a>, IIT Roorkee</div>";
?>
