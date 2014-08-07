# TODO: Fill with real data.
REGISTERED_COURSES_CLEARED_STATUS = (
    ('CUR', 'Current'),
    ('CLR','Cleared'),
    ('NXT','Next'),
    ('DRP','Dropped'),
    ('BCK','Back'),
)

SUBJECT_AREA_CHOICES = (
    ('DCC', 'Departmental Core Course'),
    ('IEC', 'Institute Elective Course'),
    ('DEC', 'Departmental Elective Course'),
    ('PEC', 'Programme Elective Course'),
    ('OEC', 'Open Elective Course'),
    ('ICC', 'Institute Core Course'),
    ('RP',  'Project'),
    ('SEM', 'Seminar'),
    ('PHDNPRE', 'PHD Non Prescribed Course'),
    ('PRO', 'Proficiency'),
)

REGISTRATION_TYPE_CHOICES = (
    ('IER', 'Institute Elective Registration'),
    ('DER', 'Departmental Elective Registration'),
    ('SBR', 'Subject Registration'),
    ('SMR', 'Semester Registration'),
    ('RFN', 'Registration Finalized'),
)

PHD_REGISTRATION_TYPE_CHOICES = (
    ('RWR', 'Research Work Registration'),
    ('CWR', 'Course Work Registration'),
)

PHD_COURSEWORK_TYPE_CHOICES = (
    ('PHDPRE', 'PHD Prescribed Courses'),
    ('PHDNPRE', 'PHD Non Prescribed Courses'),
    ('PHDSELF','PHD Self Courses'),
)

ADMIN_MESSAGES = {
    'USL':'Please make sure the file contains the fields Enrollment No, Name, Semester, Branch, Admission year, Gender in the same order',
    'UCS':'Please make sure the file contains the fields Course code, Semester, Branch, Subject Area in the same order',
    'UES':'Please make sure the file contains the fields Group code, Semester, Branch, Subject Area in the same order',
    'UCD':'Please make sure the file contains the fields Course code, Course name, Credits, Pre requisite, No of seats in the same order',
    'UED':'Please make sure the file contains the fields Course code, Course name, Credits, Pre requisite, Group code, No of seats in the same order',
    'IRC':'Please enter a valid Enrollment number.',
    'ECD':'Please enter a valid Course code.',
    'UBL':'Please make sure the file contains the fields Enrollment No, Course code, semester and cleared status in the same order',

}

UPLOAD_FILE_NO_COLS = {
  'USL':6,
  'UCS':4,
  'UES':4,
  'UCD':5,
  'UED':6,
  'UBL':4,
}

ATTRIBUTE_MODEL_MAPPING = {
  'ARC':'RegisteredCourses',
  'ECD':'CourseDetails',
  'ACD':'CourseDetails',
  'ACS':'CourseStructureMap',
  'ANEE':'InstituteElectivesNotEligibleMap'
}

ATTRIBUTE_FORM_MAPPING = {
  'CSM':'ViewCourseStructureForm',

}


ATTRIBUTE_ACTION_MAPPING = {
  'CSM':'/regol/admin/redirect/CSM/',}

SEMREG_CARD_COPIES = ['STUDENT COPY',
                      'INSTITUTE COPY',
                      'FINANCE & A/C COPY',
                      'DOSW COPY',
                      'CCB COPY',
                      'BHAWAN COPY'
]
