<?php

/*definitions for django auth table*/
define("AUTH","auth_user");
define("USER_NAME","username");

/*definitions for tsvector column*/
//define("TSV","tsv" );

/*definitions for class baseinfo */
define("ID","id");
define("FACULTY_ID","faculty_id");
define("COURSE_ID","course_id");
define("FILENAME","file");
define("TOPIC","topic");
define("PERMISSION","permission");
define("TIMESTAMP","timestamp");

/*definitions for table course_details and elective_details*/
define("COURSE_DETAILS","regol_coursedetails");
define("COURSE_NAME","course_name");
define("COURSE_CODE","course_code");
//define("ELECTIVE_DETAILS","elective_details");

/*definitions for table departments*/
define("DEPTS","departments");
define("DEPT_NAME","department_name");
define("DEPT_CODE","department_code");

/*definitions for table facapp_faculty*/
define("FACULTY","facapp_faculty");
define("NAME","name");
define("DEPARTMENT","department");

/*definitions for table lectures*/
define("LEC_TABLE","lectut_lectures");

/*definitions for table tutorials*/
define("TUT_TABLE","lectut_tutorials");

/*definitions for table exam_papers*/
define("EXAM_TABLE","lectut_exam_papers");
define("YEAR","year");

/*definitions for table solutions*/
define("SOLN_TABLE","lectut_solutions");
define("LINK_TO","link_id");
define("LINK_TYPE","link_type");

/*definitions for table nucleus_person*/
//define("PERSON_VIEW","person_view");
define("PERSON","nucleus_person");
//define("PERSON_ID","person_id");
define("USER_ID","user_id");
define("SEMESTER","semester");

/*definitions for table regol_registeredcourses*/
define("REGISTERED_COURSES","regol_registeredcourses");
define("PERSON_ID","person_id");
define("COURSE_DETAILS_ID","course_details_id");
define("CLEARED_STATUS","cleared_status");
define("CUR","CUR");

/*definitions for curricular_structure*/
define("CURR_STRUC","regol_coursestructuremap");
define("DISCIPLINE","discipline");

/*directories*/
define("LECDIR","../uploads/lectures");
define("TUTDIR","../uploads/tutorials");
define("EXAMDIR","../uploads/exampapers");
define("SOLNDIR","../uploads/solutions");
/*define("ROOT","/home/virendra/channel-i-php/lectut");*/
define("ROOT",dirname(__FILE__)."/..");

/*definitions for design_choice*/
define("DESIGN_TABLE","lectut_design_choice");
define("DESIGN_CHOICE","choice");

?>
