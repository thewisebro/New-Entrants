<?
$current_path = dirname(__FILE__);
include $current_path.'/../importpy.php';
importpy($current_path.'/pyfiles/source.py',array('d','l','s'));
/*  These too works without using $current_path .
    
    include '../importpy.php';
    importpy('pyfiles/source.py',array('d','l','s'));   // imports only given variables.
    
    importpy('pyfiles/source.py')     //imports all variable of that python module. 
    
    importpy() can only import those variable having primary data-type like int,float,str
    or having secondry data-type one of these - list,dict,tuple. These secondry data-type variables 
    may be nested of the same secondry data-type or of primary data-type.
*/
var_dump($d);
?>
