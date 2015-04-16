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

#checked
INSERT INTO nci.placement_placementperson (id, placed_company_category, no_of_companies_placed, status, photo, is_debarred, student_id) SELECT  id, placed_company_category, no_of_companies_placed, status, photo, is_debarred, person_id FROM channeli_dump.placement_placementperson;

#checked
INSERT INTO nci.placement_internshipinformation (id, brief_description, industry, title, period, priority, visible, student_id) SELECT id, brief_description, industry, title, period, priority, visible, person_id FROM channeli_dump.placement_internshipinformation;

#checked
INSERT INTO nci.placement_projectinformation (id, brief_description, industry, title, period, priority, visible, student_id) SELECT id, brief_description, industry, title, period, priority, visible, person_id FROM channeli_dump.placement_projectinformation;

#checked
INSERT INTO nci.placement_extracurriculars (id, name_of_activity, year, achievement, priority, visible, student_id) SELECT id, name_of_activity, year, achievement, priority, visible, person_id from channeli_dump.placement_extracurriculars;

#checked
INSERT INTO nci.placement_jobexperiences (id, organisation, post, date_of_joining, date_of_leaving, brief_description, priority, visible, student_id) SELECT id, organisation, post, date_of_joining, date_of_leaving, brief_description, priority, visible, person_id from channeli_dump.placement_jobexperiences;

#checked
INSERT INTO nci.placement_languagesknown (id, language, proficiency, student_id) SELECT id, language, proficiency, person_id from channeli_dump.placement_languagesknown;

#checked
INSERT INTO nci.placement_researchpublications (id, author, title, publisher, year, priority, visible, student_id) SELECT id, author, title, publisher, year, priority, visible, person_id  from channeli_dump.placement_researchpublications;

#checked
INSERT INTO nci.placement_educationaldetails (id, year, sgpa, cgpa, course, institution, discipline, discipline_provided, student_id) SELECT id, year, sgpa, cgpa, course, institution, discipline, discipline_provided, person_id from channeli_dump.placement_educationaldetails;

#checked
INSERT INTO nci.placement_placementinformation (id, registration_no, area_of_interest, computer_languages, software_packages, achievements, course_taken, reference_1, designation_1, institute_1, email_1, phone_1, reference_2, designation_2, institute_2, email_2, phone_2, student_id) SELECT id, registration_no, area_of_interest, computer_languages, software_packages, achievements, course_taken, reference_1, designation_1, institute_1, email_1, phone_1, reference_2, designation_2, institute_2, email_2, phone_2, person_id from channeli_dump.placement_placementinformation;

#checked
INSERT INTO nci.placement_cptmember (id, name, contact_no, year, email, currently_a_member) SELECT id, name, contact_no, year, email, currently_a_member from channeli_dump.placement_cptmember;

#checked
INSERT INTO nci.placement_company (id, name, year, status, place_of_posting, category, latest_date_of_joining, package_ug, package_pg, package_phd, ctc_remark, cgpa_requirement, company_description, pre_placement_talk, shortlist_from_resumes, group_discussion, online_test, written_test, paper_based_test, interview_1, interview_2, interview_3, last_date_of_applying, name_of_post, description_of_post, other_requirements, total_vacancies_for_iitr, website, brochure, sector, contact_person_id) SELECT id, name, year, status, place_of_posting, category, latest_date_of_joining, package_ug, package_pg, package_phd, ctc_remark, cgpa_requirement, company_description, pre_placement_talk, shortlist_from_resumes, group_discussion, online_test, written_test, paper_based_test, interview_1, interview_2, interview_3, last_date_of_applying, name_of_post, description_of_post, other_requirements, total_vacancies_for_iitr, website, brochure, sector, contact_person_id from channeli_dump.placement_company;

#checked
INSERT INTO  nci.placement_companyapplicationmap (id, status, shortlisted, time_of_application, company_id, plac_person_id) SELECT id, status, shortlisted, time_of_application, company_id, plac_person_id from channeli_dump.placement_companyapplicationmap ;

#checked
INSERT INTO nci.placement_secondround (id, branch_id, year) SELECT id, branch_id, year from channeli_dump.placement_secondround;

#checked
INSERT INTO nci.placement_results (id, company_id, student_id) SELECT id, company_id, person_id from channeli_dump.placement_results;

#checked
INSERT INTO nci.placement_forumpost (id, enrollment_no, person_name, discipline_name, department_name, title, content, date, forum_type) SELECT id, enrollment_no, person_name, discipline_name, department_name, title, content, date, forum_type from channeli_dump.placement_forumpost;

#checked
INSERT INTO nci.placement_forumreply (id, enrollment_no, person_name, content, date, post_id) SELECT id, enrollment_no, person_name, content, date, post_id from channeli_dump.placement_forumreply ;

#checked
INSERT INTO nci.placement_feedback (id, feedback, date, company_id, student_id) SELECT id, feedback, date, company_id, person_id from channeli_dump.placement_feedback ;

#checked
INSERT INTO nci.placement_notices (id, notice, date_of_upload) SELECT id, notice, date_of_upload from channeli_dump.placement_notices;

#checked
INSERT INTO nci.placement_contactperson (id, contact_person, designation, phone_no, email) SELECT id, contact_person, designation, phone_no, email from channeli_dump.placement_contactperson;

#checked
INSERT INTO nci.placement_companycontact (id, company_name, cluster, status, last_contact, person_in_contact, comments, when_to_contact, contactperson_id) SELECT id, company_name, cluster, status, last_contact, person_in_contact, comments, when_to_contact, contactperson_id from channeli_dump.placement_companycontact;

#checked
INSERT INTO nci.placement_placementmgr (id, coordi_id, company_name_id) SELECT id, coordi_id, company_name_id from channeli_dump.placement_placementmgr;

#checked
INSERT INTO nci.placement_companycoordi (id, student_id) SELECT id, person_id from channeli_dump.placement_companycoordi;

#checked
INSERT INTO nci.placement_companyslot (id, visibility, status, start_date, end_date) SELECT id, visibility, status, start_date, end_date from channeli_dump.placement_companyslot;

#checked
INSERT INTO nci.placement_companyplacementpriority (id, priority, date_created, date_updated, company_id, slots_id, student_id) SELECT id, priority, date_created, date_updated, company_id, slots_id, person_id from channeli_dump.placement_companyplacementpriority ;

#checked
INSERT INTO nci.placement_workshoppriority (id, day1_priority, day2_priority, day3_priority, day4_priority, day5_priority, interview_application, student_id) SELECT id, day1_priority, day2_priority, day3_priority, day4_priority, day5_priority, interview_application, person_id from channeli_dump.placement_workshoppriority ;

# Download Softwares
INSERT INTO nci.softwares_software (id,soft_name,category,image,url,version,description,date_added,download_count,added_by,soft_file) SELECT id,soft_name,category,image,url,version,description,date_added,download_count,added_by,soft_file FROM channeli_dump.softwares_software;

#MCM
INSERT INTO nci.mcm_mcmperson (id, air, unfair_means, family_income, other_scholarship, date_time, student_id) SELECT id, air, unfair_means, family_income, other_scholarship, date_time, person_id from channeli_dump.mcm_mcmperson;

INSERT INTO nci.mcm_studentloanaid (id, `check`, cgpa, sgpa, fathers_income, fathers_pan_no, mothers_pan_no, gaurdians_pan_no, guardians_name, guardians_occupation, guardians_income, guardians_address, mothers_occupation, mothers_income, other_scholarship_details, previous_aid_amount, previous_aid_session, work_bhawan_details, date_time, student_id) SELECT id, `check`, cgpa, sgpa, fathers_income, fathers_pan_no, mothers_pan_no, gaurdians_pan_no, guardians_name, guardians_occupation, guardians_income, guardians_address, mothers_occupation, mothers_income, other_scholarship_details, previous_aid_amount, previous_aid_session, work_bhawan_details, date_time, person_id from channeli_dump.mcm_studentloanaid;

INSERT INTO nci.mcm_mcm (id, scholar_type, `check`, air, unfair_means, cgpa, sgpa, family_income, other_scholarship_details, datetime, payment_choice, student_id) SELECT id, scholar_type, `check`, air, unfair_means, cgpa, sgpa, family_income, other_scholarship_details, datetime, payment_choice, person_id from channeli_dump.mcm_mcm;

#INTERNSHIP_ONLINE
#all_checked

INSERT INTO nci.internship_internshipperson (id, status, is_placed, student_id) SELECT id, status, is_placed, person_id from channeli_dump.internship_internshipperson;

INSERT INTO nci.internship_company (id, name_of_company, status, year, address, latest_date_of_joining, stipend, stipend_remark, cgpa_requirements, description, designation_of_contact_person, email, fax, last_date_of_applying, name_of_contact_person, nature_of_duties, name_of_post, no_of_employees, other_requirements, telephone, pre_internship_talk, shortlist_from_resumes, group_discussion, online_test, written_test, paper_based_test, interview_1, interview_2, interview_3, probable_date_of_arrival, total_vacancies, training_period, turnover, website, brochure,sector) SELECT id, name_of_company, status, year, address, latest_date_of_joining, stipend, stipend_remark, cgpa_requirements, description, designation_of_contact_person, email, fax, last_date_of_applying, name_of_contact_person, nature_of_duties, name_of_post, no_of_employees, other_requirements, telephone, pre_internship_talk, shortlist_from_resumes, group_discussion, online_test, written_test, paper_based_test, interview_1, interview_2, interview_3, probable_date_of_arrival, total_vacancies, training_period, turnover, website, brochure,sector from channeli_dump.internship_company;

INSERT INTO nci.internship_companyapplicationmap (id, status, company_id, student_id) SELECT id, status, company_id, person_id from channeli_dump.internship_companyapplicationmap;

INSERT INTO nci.internship_forumpost (id, enrollment_no, person_name, discipline_name, department_name, title, content, date, forum_type) SELECT id, enrollment_no, person_name, discipline_name, department_name, title, content, date, forum_type from channeli_dump.internship_forumpost;

INSERT INTO nci.internship_forumreply (id, enrollment_no, person_name, content, date, post_id) SELECT id, enrollment_no, person_name, content, date, post_id from channeli_dump.internship_forumreply ;

INSERT INTO nci.internship_feedback (id, enrollment_no, person_name, discipline_name, department_name, company_name, feedback, date, year) SELECT id, enrollment_no, person_name, discipline_name, department_name, company_name, feedback, date, year from channeli_dump.internship_feedback;

INSERT INTO nci.internship_results (enrollment_no, person_name, company_name, discipline_name, department_name, year, company_id) SELECT enrollment_no, person_name, company_name, discipline_name, department_name, year, company_id from channeli_dump.internship_results;

INSERT INTO nci.internship_resultsnew (id, company_id, student_id) SELECT id, company_id, person_id from channeli_dump.internship_resultsnew;

INSERT INTO nci.internship_notices (id, notice, date_of_upload) SELECT id, notice, date_of_upload from channeli_dump.internship_notices ;

INSERT INTO nci.internship_companypriority (id, priority, company_id, student_id) SELECT id, priority, company_id, person_id from channeli_dump.internship_companypriority;

#facapp

INSERT INTO nci.facapp_honors(id,faculty_id, year, award, institute, priority, visibility, datetime_created) SELECT *,'2015-04-14 21:42:47' FROM channeli_dump.facapp_honors;

INSERT INTO nci.facapp_participationseminar (id, faculty_id, name, place, sponsored_by, date, priority, visibility, datetime_created) SELECT *, '2015-04-14 21:42:47' FROM channeli_dump.facapp_participationseminar;

INSERT INTO nci.facapp_membership(id, faculty_id, organisation, position, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_membership;

INSERT INTO nci.facapp_administrativebackground(id, faculty_id, from_year, to_year, designation, organisation, at_level, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_administrativebackground;

INSERT INTO nci.facapp_professionalbackground(id, faculty_id, from_year, to_year, designation, organisation, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_professionalbackground;

INSERT INTO nci.facapp_miscellaneous(id, faculty_id, particulars_of_course, innovation_in_teaching, instructional_tasks, process_development, extension_tasks, other_work, self_appraisal, comments, separate_summary, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_miscellaneous;

INSERT INTO nci.facapp_educationaldetails(id, faculty_id, subject, year, university, degree, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_educationaldetails;

INSERT INTO nci.facapp_collaboration(id, faculty_id, topic, organisation, level, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_collaboration;

INSERT INTO nci.facapp_booksauthored(faculty_id, books, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_booksauthored;  

INSERT INTO nci.facapp_refereedjournalpapers(faculty_id, papers, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_refereedjournalpapers;

INSERT INTO nci.facapp_invitations(id, faculty_id, topic, organisation, category, priority, year, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_invitations;

INSERT INTO nci.facapp_multiplepost(id, post, faculty_id, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_multiplepost;

INSERT INTO nci.facapp_teachingengagement(id, faculty_id, priority, class_name, semester, course_code, title, no_of_students, lecture_hours, practical_hours, tutorial_hours, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_teachingengagement;

INSERT INTO nci.facapp_sponsoredresearchprojects(id, faculty_id, financial_outlay, funding_agency, period, other_investigating_officer, status_of_project, type_of_project, year, topic, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_sponsoredresearchprojects;

INSERT INTO nci.facapp_projectandthesissupervision(id, faculty_id, title_of_project, names_of_students, name_of_other_supervisor, description, course, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_projectandthesissupervision;

INSERT INTO nci.facapp_phdsupervised(id, faculty_id, topic, name_of_other_supervisor, registration_year, status_of_phd, phd_type, scholar_name, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_phdsupervised;

INSERT INTO nci.facapp_researchscholargroup(id, faculty_id, scholar_name, interest, home_page, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_researchscholargroup;

INSERT INTO nci.facapp_interests(id, faculty_id, general_topic, research_work_topic, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_interests;

INSERT INTO nci.facapp_visits(id, faculty_id, purpose_of_visit, institute_visited, date, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_visits;

INSERT INTO nci.facapp_participationinshorttermcourses(id, faculty_id, course_name, sponsored_by, date, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_participationinshorttermcourses;

INSERT INTO nci.facapp_organisedconference(id, faculty_id, conference_name, sponsored_by, date, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_organisedconference;

INSERT INTO nci.facapp_speciallecturesdelivered (id, faculty_id, title, place, description, date, priority, visibility, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_speciallecturesdelivered;

INSERT INTO nci.facapp_facspace (user_id, space, datetime_created) SELECT *, NOW() FROM channeli_dump.facapp_facspace;