<?php

include("database.php");

database::connectToDatabase('intranet');

$temp_terms=array();
$terms=array();
$result=database::executeQuery('intranet',database::getDistinctId(TSV,LEC_TABLE,NULL));
while($row=pg_fetch_array($result))
{
	$temp_terms=preg_split("/\b'[^'][^']*'\b/",$row[0]);
	foreach($temp_terms as $term)
	{
		$term=str_ireplace("'","",$term);
		array_push($terms,$term);
	}
}
array_unique($terms);
print_r($terms);
database::closeDatabase('intranet');

?>

