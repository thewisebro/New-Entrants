<?php
session_start();

include_once("../common/functions.php");

if(isLogin($_SESSION['username'],$_SESSION['sessionid']))
{
if($_SESSION['user']=='s')	
$studId=$_SESSION['username'];
if($_SESSION['user']=='f')
$facId=$_SESSION['username'];
echo "<a href=\"logout.php\">Logout</a><br>";
								echo "<a href=\"dept_list.php\">Browse All</a><br>";
								}
								else
								{
									echo "<a href=\"index.php\">Login</a><br>";
									}

									$search=filter_input(INPUT_GET,'search',FILTER_SANITIZE_STRING);
									$search=secure($search);

									$len=strlen($search);

									if($len<2)
									{
										echo "Search string should be atleast 3 characters long or department code.";
										}
										else
										{

										database::connectToDatabase("intranet");
										database::connectToDatabase("regol");

										if(isset($studId))
										{
											$reg_courses=database::executeQuery('regol',database::studQuery($studId));
											}
											$time1=microtime(true);
											$results_lec = search_perform($search,"lec");
											$results_tut = search_perform($search,"tut");
											$results_exam = search_perform($search,"exam");
											$results_soln = search_perform($search,"soln");
											$time2=microtime(true);
											$time=$time2-$time1;
											$time=round($time,3);
											echo "$search ($time seconds)";
											?>

<form name="download" action="download.php" method="post">
<h3>Lectures</h3>
<table>
<?php
$i=count($results_lec);
$count=0;
foreach($results_lec[count] as $result)
{
if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$result->getFacultyId())
{
$count++;
?>			<tr>
<td><? echo $count;  ?></td>
<td><? echo $result->getFacultyId(); ?></td>
<td><? echo $result->getCourseId(); ?></td>
<td>
<a href=<? echo LECDIR."/".$result->getFacultyId()."/".$result->getFile(); ?>><? echo $result->getTopic(); ?></a>
</td>
<td>
<input type="checkbox" name="lec[]" value="<? echo $result->getFacultyId()."/".$result->getFile(); ?>">
</td>
</tr><br>
<?php
}
}
if($count==0)
{
echo "No lectures found.";
}
?>
</table>

<h3>Tutorials</h3>
																																																																			<table>
																																																																			<?php
																																																																				$i=count($results_tut);
																																																																					$count=0;
																																																																							foreach($results_tut[$count] as $result)
																																																																									{
																																																																												if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$result->getFacultyId())
																																																																															{
																																																																																			$count++;
																																																																																			?>			<tr>
																																																																																						<td><? echo $count;  ?></td>
																																																																																									<td><? echo $result->getFacultyId(); ?></td>
																																																																																												<td><? echo $result->getCourseId(); ?></td>
																																																																																															<td>
																																																																																																		<a href=<? echo TUTDIR."/".$result->getFacultyId()."/".$result->getFile(); ?>><? echo $result->getTopic(); ?></a>
																																																																																																					</td>
																																																																																																								<td>
																																																																																																											<input type="checkbox" name="tut[]" value="<? echo $result->getFacultyId()."/".$result->getFile(); ?>">
																																																																																																														</td>

																																																																																																																	</tr><br>
																																																																																																																	<?php
																																																																																																																				}
																																																																																																																						}
																																																																																																																							if($count==0)
																																																																																																																								{
																																																																																																																										echo "No tutorials found.";
																																																																																																																											}
																																																																																																																											?>
																																																																																																																											</table>

																																																																																																																											<h3>Exam Papers</h3>
																																																																																																																											<table>
																																																																																																																											<?php
																																																																																																																												$i=count($results_exam);
																																																																																																																													$count=0;
																																																																																																																															foreach($results_exam[$count] as $result)
																																																																																																																																	{
																																																																																																																																				if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$result->getFacultyId())
																																																																																																																																							{
																																																																																																																																											$count++;
																																																																																																																																											?>			<tr>
																																																																																																																																														<td><? echo $count;  ?></td>
																																																																																																																																																	<td><? echo $result->getFacultyId(); ?></td>
																																																																																																																																																				<td><? echo $result->getCourseId(); ?></td>
																																																																																																																																																							<td>
																																																																																																																																																										<a href=<? echo EXAMDIR."/".$result->getFacultyId()."/".$result->getFile(); ?>><? echo $result->getTopic(); ?></a>
																																																																																																																																																													</td>
																																																																																																																																																																<td>
																																																																																																																																																																			<input type="checkbox" name="exam[]" value="<? echo $result->getFacultyId()."/".$result->getFile(); ?>">
																																																																																																																																																																						</td>
																																																																																																																																																																									</tr><br>
																																																																																																																																																																									<?php
																																																																																																																																																																												}
																																																																																																																																																																														}
																																																																																																																																																																															if($count==0)
																																																																																																																																																																																{
																																																																																																																																																																																		echo "No Exam Papers found.";
																																																																																																																																																																																			}
																																																																																																																																																																																			?>
																																																																																																																																																																																			</table>

																																																																																																																																																																																			<h3>Solutions</h3>
																																																																																																																																																																																			<table>
																																																																																																																																																																																			<?php
																																																																																																																																																																																				$i=count($results_soln);
																																																																																																																																																																																					$count=0;
																																																																																																																																																																																							foreach($results_soln[$count] as $result)
																																																																																																																																																																																									{
																																																																																																																																																																																												if($result->getPermission()=='f' || in_array($result->getCourseId(),$reg_courses) || $facId==$result->getFacultyId())
																																																																																																																																																																																															{
																																																																																																																																																																																																			$count++;
																																																																																																																																																																																																			?>			<tr>
																																																																																																																																																																																																						<td><? echo $count;  ?></td>
																																																																																																																																																																																																									<td><? echo $result->getFacultyId(); ?></td>
																																																																																																																																																																																																												<td><? echo $result->getCourseId(); ?></td>
																																																																																																																																																																																																															<td>
																																																																																																																																																																																																																		<a href=<? echo SOLNDIR."/".$result->getFacultyId()."/".$result->getFile(); ?>><? echo $result->getTopic(); ?></a>
																																																																																																																																																																																																																					</td>
																																																																																																																																																																																																																								<td>
																																																																																																																																																																																																																											<input type="checkbox" name="soln[]" value="<? echo $result->getFacultyId()."/".$result->getFile(); ?>">
																																																																																																																																																																																																																														</td>
																																																																																																																																																																																																																																	</tr><br>
																																																																																																																																																																																																																																	<?php
																																																																																																																																																																																																																																				}
																																																																																																																																																																																																																																						}
																																																																																																																																																																																																																																							if($count==0)
																																																																																																																																																																																																																																								{
																																																																																																																																																																																																																																										echo "No Solutions found.";
																																																																																																																																																																																																																																											}
																																																																																																																																																																																																																																											?>
																																																																																																																																																																																																																																											</table>
																																																																																																																																																																																																																																											<br>
																																																																																																																																																																																																																																											<input type="submit" value="Download">
																																																																																																																																																																																																																																											</form>

																																																																																																																																																																																																																																											<?php

																																																																																																																																																																																																																																											database::closeDatabase("regol");
																																																																																																																																																																																																																																											database::closeDatabase("intranet");
																																																																																																																																																																																																																																											}

																																																																																																																																																																																																																																											?>
