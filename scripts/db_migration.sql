# nucleus

insert into nci.auth_group select * from ci.auth_group;

insert into nci.nucleus_user (id,username,password,last_login,date_joined,is_active,is_staff,email) select id,username,password,last_login,date_joined,is_active,is_staff,email from ci.auth_user;

insert into nci.nucleus_user_groups (id,user_id,group_id) select id,user_id,group_id from ci.auth_user_groups;

update nci.nucleus_user inner join ci.nucleus_person on (nci.nucleus_user.id = ci.nucleus_person.user_id) set nci.nucleus_user.name=ci.nucleus_person.name, nci.nucleus_user.photo=ci.nucleus_person.photo, nci.nucleus_user.gender=ci.nucleus_person.gender, nci.nucleus_user.contact_no=ci.nucleus_person.personal_contact_no;

update nci.nucleus_user inner join ci.facapp_faculty on (nci.nucleus_user.id = ci.facapp_faculty.user_id) set nci.nucleus_user.name=ci.facapp_faculty.name, nci.nucleus_user.photo=ci.facapp_faculty.photo, nci.nucleus_user.email=ci.facapp_faculty.alternate_mail_id, nci.nucleus_user.contact_no=ci.facapp_faculty.phone;

insert into nci.nucleus_branch (code,name,degree,department,graduation,no_of_semesters) select code,name,degree,department,graduation,duration from ci.nucleus_branch;

insert into nci.nucleus_student (user_id,branch_id,admission_year,cgpa,bhawan,room_no) select user_id,branch_id,admission_year,cgpa,bhawan,room_no from ci.nucleus_person;

insert into nci.nucleus_faculty (user_id,department,resume,designation,address,employee_code,date_of_joining,home_page) select user_id,department,resume,designation,address,employee_code,date_of_joining,home_page from ci.facapp_faculty;





# regol
insert into nci.regol_coursedetails select * from ci.regol_coursedetails;

insert into nci.regol_registeredcourses (student_id,course_details_id,credits,registered_date,semester,subject_area,cleared_status,grade,group_code) select person_id as student_id,course_details_id,credits,registered_date,semester,subject_area,cleared_status,grade,group_code from ci.regol_registeredcourses;


# groups
insert into nci.groups_group (user_id,name,nickname,website,description,admin_id,is_active) select user_id,name,nickname,website,description,admin_id,is_active from ci.groups_group;

# events
insert into nci.events_calendar (id,name,cal_type) select id,name,cal_type from ci.events_calendar;
insert into nci.events_calendar_users (id,calendar_id,user_id) select id,calendar_id,user_id from ci.events_calendar_users;
insert into nci.events_event (id,calendar_id,uploader_id,title,date,time,upto_date,upto_time,place,description,event_type,datetime_added,email_sent) select id,calendar_id,uploader_id,title,date,time,upto_date,upto_time,place,description,event_type,datetime_added,email_sent from ci.events_event;
