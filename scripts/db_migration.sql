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

INSERT INTO nci.groups_groupinfo (group_id,mission,founding_year,facebook_url,twitter_url,gplus_url) (SELECT a.user_id as group_id,b.mission,b.founding_year,b.facebook_url,b.twitter_url,b.gplus_url FROM channeli_dump.groups_group a JOIN channeli_dump.groups_groupinfo b ON a.id = b.group_id);

INSERT INTO nci.groups_post (id, post_name) SELECT id, post_name FROM channeli_dump.groups_post;

INSERT INTO nci.groups_membership (id,groupinfo_id,post_id,student_id) (SELECT a.id, c.user_id as groupinfo_id, a.post_id, a.person_id as student_id FROM channeli_dump.groups_membership a JOIN channeli_dump.groups_groupinfo b ON a.groupinfo_id = b.id JOIN channeli_dump.groups_group c ON b.group_id = c.id);

INSERT INTO nci.groups_groupinfo_posts (id,groupinfo_id,post_id) (SELECT a.id, c.user_id as groupinfo_id, a.post_id FROM channeli_dump.groups_groupinfo_posts a JOIN channeli_dump.groups_groupinfo b ON a.groupinfo_id = b.id JOIN channeli_dump.groups_group c ON b.group_id = c.id);

INSERT INTO nci.groups_groupactivity (id,group_id,text,datetime_created) (SELECT a.id, b.user_id as group_id, a.text, a.datetime as datetime_created FROM channeli_dump.groups_groupactivity a JOIN channeli_dump.groups_group b ON a.group_id = b.id);


# events
INSERT INTO nci.events_calendar (id,name,cal_type) SELECT id,name,cal_type FROM channeli_dump.events_calendar;
INSERT INTO nci.events_calendar_users (id,calendar_id,user_id) SELECT id,calendar_id,user_id FROM channeli_dump.events_calendar_users;
INSERT INTO nci.events_event (id,calendar_id,uploader_id,title,date,time,upto_date,upto_time,place,description,event_type,datetime_added,email_sent) SELECT id,calendar_id,uploader_id,title,date,time,upto_date,upto_time,place,description,event_type,datetime_added,email_sent FROM channeli_dump.events_event;

#placement

INSERT INTO nci.placement_placementperson (id, placed_company_category, no_of_companies_placed, status, photo, is_debarred, student_id) SELECT  id, placed_company_created, no_of_companies_created, status, photo, is_debarred, person_id FROM channeli_dump.placement_placementperson;

INSERT INTO nci.placement_internshipinformation (id, brief_description, industry, title, period, priority, visible, student_id) SELECT id, brief_description, industry, title, period, priority, visible, person_id FROM channeli_dump.placement_internshipinformation;

INSERT INTO nci.placement_projectinformation (id, brief_description, industry, title, period, priority, visible, student_id) SELECT id, brief_description, industry, title, period, priority, visible, person_id FROM channeli_dump.placement_projectinformation;

INSERT INTO nci.placement_extracurriculars (id, name_of_activity, year, achievement, priority, visible, student_id) SELECT id, name_of_activity, year, achievement, priority, visible, person_id from channeli_dump.placement_extracurriculars;

INSERT INTO nci.placement_jobexperiences (id, organisation, post, date_of_joining, date_of_leaving, brief_description, priority, visible, student_id) SELECT id, organisation, post, date_of_joining, date_of_leaving, brief_description, priority, visible, person_id from channeli_dump.placement_jobexperiences;

INSERT INTO nci.placement_languagesknown (id, language, proficiency, student_id) SELECT id, language, proficiency, person_id from channeli_dump.placement_languagesknown;

INSERT INTO nci.placement_researchpublications (id, author, title, publisher, year, priority, visible, student_id) SELECT id, author, title, publisher, year, priority, visible, person_id  from channeli_dump.placement_researchpublications;

INSERT INTO nci.placement_educationaldetails (id, year, sgpa, cgpa, course, institution, discipline, discipline_provided, student_id) SELECT id, year, sgpa, cgpa, course, institution, discipline, discipline_provided, person_id from channeli_dump.placement_educationaldetails;

INSERT INTO nci.placement_placementinformation (id, registration_no, area_of_interest, computer_languages, achievements, course_taken, reference_1, designation_1, institute_1, email_1, phone_1, reference_2, designation_2, institute_2, email_2, phone_2, student_id) SELECT id, registration_no, area_of_interest, computer_languages, achievements, course_taken, reference_1, designation_1, institute_1, email_1, phone_1, reference_2, designation_2, institute_2, email_2, phone_2, person_id from channeli_dump.placement_placementinformation;

INSERT INTO nci.placement_cptmember (id, name, contact_no, year, email, currently_a_member) SELECT id, name, contact_no, year, email, currently_a_member from channeli_dump.placement_cptmember;

INSERT INTO nci.placement_company (id, name, year, status, place_of_posting, category, latest_date_of_joining, package_ug, package_pg, package_phd, ctc_remark, cgpa_requirement, company_description, pre_placement_talk, shortlist_from_resumes, group_discussion, online_test, written_test, paper_based_test, interview_1, interview_2, interview_3, last_date_of_applying, name_of_post, description_of_post, other_requirements, total_vacancies_for_iitr, website, brochure, sector, contact_person_id) SELECT id, name, year, status, place_of_posting, category, latest_date_of_joining, package_ug, package_pg, package_phd, ctc_remark, cgpa_requirement, company_description, pre_placement_talk, shortlist_from_resumes, group_discussion, online_test, written_test, paper_based_test, interview_1, interview_2, interview_3, last_date_of_applying, name_of_post, description_of_post, other_requirements, total_vacancies_for_iitr, website, brochure, sector, contact_person_id from channeli_dump.placement_company;

INSERT INTO  nci.placement_companyapplicationmap (id, status, shortlisted, time_of_application, company_id, plac_person_id) SELECT id, status, shortlisted, time_of_application, company_id, plac_person_id from channeli_dump.placement_companyapplicationmap ;

# Download Softwares
INSERT INTO nci.softwares_software (id,soft_name,category,image,url,version,description,date_added,download_count,added_by,soft_file) SELECT id,soft_name,category,image,url,version,description,date_added,download_count,added_by,soft_file FROM channeli_dump.softwares_software;
