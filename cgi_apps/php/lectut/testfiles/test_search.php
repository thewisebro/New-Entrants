<?php
session_start();
if(session_is_registered(username))
{
	if($_SESSION['user']=='s')	
		$studId=$_SESSION['username'];
	if($_SESSION['user']=='f')
		$facId=$_SESSION['username'];
	echo "<a href=logout.php?".session_name()."=".session_id().">Logout</a><br>";
	echo "<a href=dept_list.php?".session_name()."=".session_id().">Back</a><br>";
}
include("../common/database.php");
include("../common/functions.php");
$search=filter_input(INPUT_GET,'search',FILTER_SANITIZE_STRING);
$subcode=secureCode($search);
$search=secure($search);
database::connectToDatabase("intranet");
echo "1. $search";
function search_split_terms($terms)
{
	$terms = preg_replace("/\"(.*?)\"/e", "search_transform_term('\$1')", $terms);
	$terms = preg_split("/\s+|,/", $terms);
	$out = array();
	foreach($terms as $term)
	{
		$term = preg_replace("/\{WHITESPACE-([0-9]+)\}/e", "chr(\$1)", $term);
		$term = preg_replace("/\{COMMA\}/", ",", $term);
		$out[] = $term;
	}
	return $out;
}

function search_transform_term($term)
{
	$term = preg_replace("/(\s)/e", "'{WHITESPACE-'.ord('\$1').'}'", $term);
	$term = preg_replace("/,/", "{COMMA}", $term);
	return $term;
}
/*
function search_escape_rlike($string)
{
	return preg_replace("/([.\[\]*^\$])/", '\\\$1', $string);
}

function search_db_escape_terms($terms)
{
	$out = array();
	foreach($terms as $term)
	{
		$out[] = '[[:<:]]'.AddSlashes(search_escape_rlike($term)).'[[:>:]]';
	}
	return $out;
}*/

function search_perform($terms)
{
	$terms = search_split_terms($terms);
//	$terms_db = search_db_escape_terms($terms);
//	$terms_rx = search_rx_escape_terms($terms);
//	$terms_db = implode(' | ', $terms_db);
	$terms=implode(' | ',$terms);
	print_r($terms);
	$rows = array();
	$result = database::executeQuery("intranet",database::searchLec($terms));
	while($row = pg_fetch_array($result,NULL,PGSQL_ASSOC))
	{
		$row[score] = 0;
		foreach($terms_rx as $term_rx)
		{
			$row[score] += preg_match_all("/$term_rx/i", $row[content_body], $null);
		}
		$rows[] = $row;
	}
	uasort($rows, 'search_sort_results');
	return $rows;
}
/*
function search_rx_escape_terms($terms)
{
	$out = array();
	foreach($terms as $term)
	{
		$out[] = '\b'.preg_quote($term, '/').'\b';
	}
	return $out;
}*/

function search_sort_results($a, $b)
{
	$ax = $a[score];
	$bx = $b[score];
	if ($ax == $bx){ return 0; }
	return ($ax > $bx) ? -1 : 1;
}
/*
function search_html_escape_terms($terms)
{
	$out = array();
	foreach($terms as $term)
	{
		if (preg_match("/\s|,/", $term))
		{
			$out[] = '"'.HtmlSpecialChars($term).'"';
		}
		else
		{
			$out[] = HtmlSpecialChars($term);
		}
	}
	return $out;	
}	*/

/*function search_pretty_terms($terms_html)
{

	if (count($terms_html) == 1)
	{
		return array_pop($terms_html);
	}
	$last = array_pop($terms_html);
	return implode(', ', $terms_html)." and $last";
}
*/
$results = search_perform($search);
//$term_list = search_pretty_terms(search_html_escape_terms(search_split_terms($search)));
$i=0;
foreach($results as $result)
{
	echo $i++.$result[1].$result[2].$result[4];?><br><?php
}
database::closeDatabase("intranet");

?>
