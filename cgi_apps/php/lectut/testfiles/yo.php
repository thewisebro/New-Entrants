<?php

header("Content-type:application/xml");
$xmlDoc = new DOMDocument();
$xmlDoc->load("yo.xml");

print $xmlDoc->saveXML();
?> 
