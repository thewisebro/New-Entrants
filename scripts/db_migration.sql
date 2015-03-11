# nucleus

INSERT INTO nci.auth_group SELECT * FROM channeli_dump.auth_group;

INSERT INTO nci.nucleus_user (id,username,password,last_login,date_joined,is_active,is_staff,email) SELECT id,username,password,last_login,date_joined,is_active,is_staff,email FROM channeli_dump.auth_user;

UPDATE nci.nucleus_user SET is_superuser=1, is_staff=1 WHERE nci.nucleus_user.username='admin';

INSERT INTO nci.nucleus_user_groups (id,user_id,group_id) SELECT id,user_id,group_id FROM channeli_dump.auth_user_groups;

UPDATE nci.nucleus_user INNER JOIN channeli_dump.nucleus_person ON (nci.nucleus_user.id = channeli_dump.nucleus_person.user_id) SET nci.nucleus_user.name=channeli_dump.nucleus_person.name, nci.nucleus_user.photo=channeli_dump.nucleus_person.photo, nci.nucleus_user.gender=channeli_dump.nucleus_person.gender, nci.nucleus_user.contact_no=channeli_dump.nucleus_person.personal_contact_no;

UPDATE nci.nucleus_user INNER JOIN channeli_dump.nucleus_personinfo ON (nci.nucleus_user.id = channeli_dump.nucleus_personinfo.person_id) SET nci.nucleus_user.birth_date=channeli_dump.nucleus_personinfo.birth_date;

UPDATE nci.nucleus_user INNER JOIN channeli_dump.facapp_faculty ON (nci.nucleus_user.id = channeli_dump.facapp_faculty.user_id) SET nci.nucleus_user.name=channeli_dump.facapp_faculty.name, nci.nucleus_user.photo=channeli_dump.facapp_faculty.photo, nci.nucleus_user.email=channeli_dump.facapp_faculty.alternate_mail_id, nci.nucleus_user.birth_date=channeli_dump.facapp_faculty.date_of_birth, nci.nucleus_user.contact_no=channeli_dump.facapp_faculty.phone;

UPDATE nci.nucleus_user INNER JOIN channeli_dump.groups_group ON (nci.nucleus_user.id = channeli_dump.groups_group.user_id) SET nci.nucleus_user.name=channeli_dump.groups_group.name;

UPDATE nci.nucleus_user c INNER JOIN (SELECT a.user_id,b.email,b.photo,b.phone_no FROM channeli_dump.groups_group a JOIN channeli_dump.groups_groupinfo b ON a.id = b.group_id) d ON (c.id = d.user_id) SET c.photo=d.photo,c.email=d.email,c.contact_no=d.phone_no;

INSERT INTO nci.nucleus_branch (code,name,degree,department,graduation,no_of_semesters) SELECT code,name,degree,department,graduation,duration FROM channeli_dump.nucleus_branch;

INSERT INTO nci.nucleus_student (user_id,semester,branch_id,admission_year,cgpa,bhawan,room_no,passout_year) SELECT user_id,semester,branch_id,admission_year,cgpa,bhawan,room_no,passout_year FROM channeli_dump.nucleus_person;

INSERT INTO nci.nucleus_studentinfo (student_id,fathers_name,fathers_occupation,fathers_office_address,fathers_office_phone_no,mothers_name,permanent_address,home_contact_no,state,city,pincode,bank_account_no,passport_no,nearest_station,local_guardian_name,local_guardian_address,local_guardian_contact_no,category,nationality,marital_status,blood_group,physically_disabled,fulltime,resident,license_no) SELECT person_id,fathers_name,fathers_occupation,fathers_office_address,fathers_office_phone_no,mothers_name,permanent_address,home_contact_no,state,city,pincode,bank_account_no,passport_no,nearest_station,local_guardian_name,local_guardian_address,local_guardian_contact_no,category,nationality,marital_status,blood_group,physically_handicapped,fulltime,resident,license_no FROM channeli_dump.nucleus_personinfo;

INSERT INTO nci.nucleus_faculty (user_id,department,resume,designation,address,employee_code,date_of_joining,home_page) SELECT user_id,department,resume,designation,address,employee_code,date_of_joining,home_page FROM channeli_dump.facapp_faculty;





# regol
INSERT INTO nci.regol_coursedetails SELECT * FROM channeli_dump.regol_coursedetails;

INSERT INTO nci.regol_registeredcourses (student_id,course_details_id,credits,registered_date,semester,subject_area,cleared_status,grade,group_code) SELECT person_id as student_id,course_details_id,credits,registered_date,semester,subject_area,cleared_status,grade,group_code FROM channeli_dump.regol_registeredcourses;


# groups
INSERT INTO nci.groups_group (user_id,nickname,website,description,admin_id,is_active) SELECT user_id,nickname,website,description,admin_id,is_active FROM channeli_dump.groups_group;


# events
INSERT INTO nci.events_calendar (id,name,cal_type) SELECT id,name,cal_type FROM channeli_dump.events_calendar;
INSERT INTO nci.events_calendar_users (id,calendar_id,user_id) SELECT id,calendar_id,user_id FROM channeli_dump.events_calendar_users;
INSERT INTO nci.events_event (id,calendar_id,uploader_id,title,date,time,upto_date,upto_time,place,description,event_type,datetime_added,email_sent) SELECT id,calendar_id,uploader_id,title,date,time,upto_date,upto_time,place,description,event_type,datetime_added,email_sent FROM channeli_dump.events_event;
