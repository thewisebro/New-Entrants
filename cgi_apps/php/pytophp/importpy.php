<?
function importpy($modulepath,$var_array=array()){ 
$command = dirname(__FILE__).'/pytophp.py '.$modulepath.' '.join($var_array,' ');
exec($command,$read);
foreach($read as $line)
{ eval($line);
}
}
?>
