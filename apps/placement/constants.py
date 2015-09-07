COMPANY_APPLICATION_STATUS = (
      ('APP','Applied'),
      ('FIN','Finalized'),
      ('SEL', 'Selected'),
    )

WORKSHOP_OPTIONS = (
      ('Smart India', 'Smart India'),
      ('4P Education','4P Education'),
      ('Talerang','Talerang'),
      ('Ethuns Consultancy Service','Ethuns Consultancy Service'),
      ('NOT', 'Not interested')
    )

FORUM_CHOICES = (
      ('T', 'Technical'),
      ('P', 'Placement'),
    )

COMPANY_CATEGORY_CHOICES = (
      ('A', 'A'),
      ('B', 'B'),
      ('C', 'C'),
      ('U', 'University'),
    )

# IMPORTANT : Reflect the changes in resume template directory
# templates/placement/resume/
COMPANY_RESUME_CHOICES = (
      ('FIN','Finance'),
      ('PSU', 'PSU/Government'),
      ('CON', 'Consultancy'),
      ('FMC', 'FMCG'),
      ('PHA', 'Pharmaceuticals'),
      ('RnD', 'R&D'),
      ('IT' , 'IT'),
      ('ACA', 'Academics'),
      ('OIL', 'Oil & Gas' ),
      ('CIN', 'Construction / Infrastructure'),
      ('COR','Core Engineering'),
    )

FEEDBACK_QUESTIONS_OLD = (
  '1. What was the profile offered by the company and for which branches was the company open ?',
  '2. How many rounds were there and what was the time alloted for each round?',
  '3. Briefly explain the preliminary process (Written/Online/Subjective/Objective test) and type of questions asked.',
  '4. Describe the Technical interview process (Duration/No.of rounds - Also discuss the solutions of problems/puzzles/case study asked)',
  '5. Describe the HR interview process (Duration - Also discuss the solutions of problems/case study asked)',
  '6. Other suggestions/advice that you think may be helpful.',
  )

FEEDBACK_QUESTIONS = (
  '1. Your preparations (in general) i.e. all three aspects - Technical, Aptitude and HR. The material you used, the websites you went through, the amount of time you devoted to preparations - anything and everything you would like to share',
  '2. Your Preparations (Specific to the company) - Something you did extra/different for this particular company.',
  '3. Selection Process followed by your company? Initial Screening - Written test/ Group Discussions/ CG based cut-offs; Further Rounds... ',
  '4. Questions asked/ Skills tested (Technical Round). Describe the Technical interview process (Duration/No.of rounds - Also discuss the solutions of problems/puzzles/case study asked and course subjects on which the test/ interview was based.',
  '5. Questions Asked (HR round) ',
  '6. Some tips/advice to your juniors .',
  '7. Anything else.. Something we might have missed to ask but you still want to share...and any feedback to Central Placement Team -Criticism, Appreciation, Suggestions - everything is welcome :)',
  )

LANGUAGE_PROFICIENCY_CHOICES = (
      ('SRW', 'Speak, Read and Write'),
      ('SO' , 'Speak Only'),
      ('RW' , 'Read and Write'),
      ('SR' , 'Speak and Read'),
    )

LANGUAGE_CHOICES = (
  ('AB', 'Arabic'),
  ('AS', 'Assamese'),
  ('BN', 'Bangla'),
  ('EN', 'English'),
  ('FR', 'French'),
  ('GM', 'German'),
  ('GJ', 'Gujarati'),
  ('HB', 'Hebrew'),
  ('HN', 'Hindi'),
  ('JA', 'Japanese'),
  ('KD', 'Kannada'),
  ('MM', 'Malyalam'),
  ('MR', 'Marathi'),
  ('NP', 'Nepali'),
  ('OR', 'Oriya'),
  ('PN', 'Punjabi'),
  ('RU', 'Russian'),
  ('SN', 'Sanskrit'),
  ('SP', 'Spanish'),
  ('SW', 'Swahili'),
  ('TM', 'Tamil'),
  ('TG', 'Telugu'),
  ('UD', 'Urdu'),
)

PLACEMENT_STATUS_CHOICES = (
      ('CLS', 'Closed'),
      ('OPN', 'Opened'),
      ('LCK', 'Locked'),
      ('VRF', 'Verified'),
    )

COMPANY_STATUS_CHOICES = (
      ('OPN', 'Open'),
      ('CLS', 'Closed'),
      ('DEC', 'Declared'),
      ('FIN', 'Finalized'),
    )

CGPA_CHOICES = (
  (5.0, '5.0'),
  (5.25, '5.25'),
  (5.5, '5.5'),
  (5.75, '5.75'),
  (6.0, '6.0'),
  (6.25, '6.25'),
  (6.5, '6.5'),
  (6.75, '6.75'),
  (7.0, '7.0'),
  (7.25, '7.25'),
  (7.5, '7.5'),
  (7.75, '7.75'),
  (8.0, '8.0'),
  (8.25, '8.25'),
  (8.5, '8.5'),
  (8.75, '8.75'),
  (9.0, '9.0')
  )

PAY_PACKAGE_CURRENCY_CHOICES = (
  ('INR', 'INR'),
  ('USD', 'USD'),
  )

#XXX
#Do not change these values
#function get_ctc in utils.py depends on these.
PAY_WHOLE_CHOICES = (
  ('Thousands', 'Thousands'),
  ('Lacs', 'Lacs'),
  )

PAY_PACKAGE_CURRENCY_CONVERSION_RATES = {
  'INR' : 1,
  'USD' : 50,
  }

# Status for placement manager company contact
STATUS_CHOICES = (
        ('JAF Sent', "JAF Sent"),
        ('JAF Received', "JAF Received"),
        ('STF Sent', "STF Sent"),
        ('Not Called', "Not Called"),
        ('JAF + STF sent', 'JAF + STF sent'),
        ('JAF+ STF recieved', 'JAF+ STF recieved'),
        ('Not Picking Up', "Not Picking Up"),
        ('Incorrect contact info', "Incorrect contact info"),
        ('Call Later', "call later"),
        ('Denied', "Denied"),
        ('Process Confirmed', "Process Confirmed"),
        ('Other', "Other"),
    )

# Choices for clusters in company contact
CLUSTER_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )

IMPORT_FILE_TYPES = ['.xls','.xlsx']

COMPANY_COORDI_CHOICES = (
        ('11115072', '11115072 Kunal Punjabi'),
        ('11312018', '11312018 Naman Agrawal'),
        ('11312003', '11312003 Amit Yadav'),
        ('12112021', '12112021 Bhagyashree Das'),
        ('13531006', '13531006 Jitendra Kumar'),
        ('12214012', '12214012 Lilly Kumari'),
        ('10411002', '10411002 Akshit Goel'),
        ('12117017', '12117017 Ayush Kumar Tiwari'),
        ('10110062', '10110062 Sweta Panda'),
        ('10212009', '10212009 Subham Kumar Singh'),
        ('13811014', '13811014 Megha Mittal'),
        ('13611015', '13611015 Sakshi Ganotra'),
    )
