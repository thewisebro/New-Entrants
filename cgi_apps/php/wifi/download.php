<?php

// output headers so that the file is downloaded rather than displayed
header('Content-Type: application/csv');
header('Content-Disposition: attachment; filename=result.csv');
header('Pragma: no-cache');

echo readfile('./excel/result.csv');

?>
