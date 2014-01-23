CODE_LENGTH=10
TEXT_LENGTH=100
PHONE_NO_LENGTH=15

YES_NO_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

# MAKE SURE ALL APPLICATIONS USE THIS TO SHOW departments.
# It should not contain any number
DEPARTMENT_CHOICES = (
    # End all department names with 'D'
    ('AHEC', 'Alternate Hydro Energy Centre'),
    ('ASED', 'Applied Science and Engineering Department'),
    ('CNT', 'Centre for Nanotechnology'),
    ('ARCD', 'Architecture and Planning Department'),
    ('BTD', 'Biotechnology Department'),
    ('CHED', 'Chemical Engineering Department'),
    ('CDM', 'Centre of Excellence in Disaster Mitigation and Management'),
    ('CYD', 'Chemistry Department'),
    ('CED','Civil Engineering Department'),
    ('CSED','Computer Science and Engineering Department'),
    ('CT', 'Centre for Transportation Systems'),
    ('EQD', 'Earthquake Department'),
    ('ESD', 'Earth Sciences Department'),
    ('EED', 'Electrical Engineering Department'),
    ('ECED', 'Electronics and Communication Engineering Department'),
    ('HSD','Humanities and Social Sciences Department'),
    ('HYD','Hydrology Department'),
    ('MSD','Management Studies Department'),
    ('MAD','Mathematics Department'),
    ('MIED','Mechanical and Industrial Engineering Department'),
    ('MMED','Metallurgical and Materials Engineering Department'),
    ('PTD','Paper Technology Department'),
    ('PPED','Polymer and Process Engineering Department'),
    ('PHD','Physics Department'),
    ('WRDMD','Water Resources Development and Management Department'),
    ('CDM','Centre for Disaster Mitigation'),
    ('ICC', 'Institute Computer Centre'),
    ('IIC', 'Institute Instrumentation Centre'),
    ('QIP', 'Quality Improvement Programme'),
)

STATE_CHOICES = (
    ('ADP', 'Andhra Pradesh'),
    ('ARP', 'Arunachal Pradesh'),
    ('ASM', 'Assam'),
    ('BHR', 'Bihar'),
    ('CHG', 'Chhattisgarh'),
    ('DEL', 'Delhi'),
    ('GOA', 'Goa'),
    ('GUJ', 'Gujarat'),
    ('HAR', 'Haryana'),
    ('HMP', 'Himachal Pradesh'),
    ('JNK', 'Jammu and Kashmir'),
    ('JHK', 'Jharkhand'),
    ('KAR', 'Karnataka'),
    ('KRL', 'Kerala'),
    ('MDP', 'Madya Pradesh'),
    ('MAH', 'Maharashtra'),
    ('MNP', 'Manipur'),
    ('MGY', 'Meghalaya'),
    ('MIZ', 'Mizoram'),
    ('NGL', 'Nagaland'),
    ('ORS', 'Orissa'),
    ('PJB', 'Punjab'),
    ('RAJ', 'Rajasthan'),
    ('SIK', 'Sikkim'),
    ('TAN', 'Tamil Nadu'),
    ('TRP', 'Tripura'),
    ('UTA', 'Uttaranchal'),
    ('UTP', 'Uttar Pradesh'),
    ('WSB', 'West Bengal')
)

GRADE_CHOICES = (
    ('A+', '10'),
    ('A', '9'),
    ('B+', '8'),
    ('B', '7'),
    ('C+', '6'),
    ('C', '5'),
    ('D', '4'),
    ('F', 'Back'),
    ('-', 'NA'),
)

# TODO: Fill with real data.
PHD_INFO_SCHEME_CHOICES = (
    ('MHRD', 'MHRD'),
)

# These courses must be in order in which courses can be taken by a student.
# Do not change the order or insert data as the order is used to separate the entries available to UG, PG and PhD.
# If you want to change the order, change the corresponding lines of view placment.views.educational_details also.
SEMESTER_CHOICES = (
  ('UG0' , 'UG Overall'),
  ('DPLM', 'Diploma'),
  ('PG0' , 'PG Overall'),
  ('10TH', 'Tenth'  ),
  ('12TH', 'Twelfth'),
  ('UG10', 'UG(I Year I Semester)'),
  ('UG11', 'UG(I Year II Semester)'),
  ('UG20', 'UG(II Year I Semester)'),
  ('UG21', 'UG(II Year II Semester)'),
  ('UG30', 'UG(III Year I Semester)'),
  ('UG31', 'UG(III Year II Semester)'),
  ('UG40', 'UG(IV Year I Semester)'),
  ('UG41', 'UG(IV Year II Semester)'),
  ('UG50', 'UG(V Year I Semester)'),
  ('UG51', 'UG(V Year II Semester)'),
  ('ST1' , 'Summer Term(I Year)'),
  ('ST2' , 'Summer Term(II Year)'),
  ('ST3' , 'Summer Term(III Year)'),
  ('ST4' , 'Summer Term(IV Year)'),
  ('PG10', 'PG(I Year I Semester)'),
  ('PG11', 'PG(I Year II Semester)'),
  ('PG20', 'PG(II Year I Semester)'),
  ('PG21', 'PG(II Year II Semester)'),
  ('PG30', 'PG(III Year I Semester)'),
  ('PG31', 'PG(III Year II Semester)'),
  ('PHD10', 'PHD(I Year I Semester)'),
  ('PHD11', 'PHD(I Year II Semester)'),
  ('PHD20', 'PHD(II Year I Semester)'),
  ('PHD21', 'PHD(II Year II Semester)'),
  ('PHD30', 'PHD(III Year I Semester)'),
  ('PHD31', 'PHD(III Year II Semester)'),
  ('PHD40', 'PHD(IV Year I Semester)'),
  ('PHD41', 'PHD(IV Year II Semester)'),
  ('PHD50', 'PHD(V Year I Semester)'),
  ('PHD51', 'PHD(V Year II Semester)'),
  ('PHD60', 'PHD(VI Year I Semester)'),
  ('PHD61', 'PHD(VI Year II Semester)'),
  ('PHD70', 'PHD(VII Year I Semester)'),
  ('PHD71', 'PHD(VII Year II Semester)'),
  ('PHD80', 'PHD(VIII Year I Semester)'),
  ('PHD81', 'PHD(VIII Year II Semester)'),
  ('PHD90', 'PHD(IX Year I Semester)'),
  ('PHD91', 'PHD(IX Year II Semester)'),
  ('PHD0' , 'PHD Overall'),
  ('UG00', 'UG(New Entrants)')
  )

# Can consist of : alphabets (small and capital) + digits + dot character(.)
# Important : Corressponding changes in DEGREES below for any change here.
DEGREE_CHOICES = (
    ('B.Tech.','Bachelor of Technology'),
    ('B.Arch.','Bachelor of Architecture'),
    ('IDD', 'Integrated Dual Degree'),
    ('M.Tech.', 'Master of Technology'),
    ('IMT', 'Integrated Master of Technology'),
    ('IMSc', 'Integrated Master of Science'),
    ('M.Arch.', 'Master of Architecture'),
    ('MURP', 'Master of Urban and Regional Planning'),
    ('PGDip', 'Postgraduate Diploma Course'),
    ('MBA', 'Master of Business Administration'),
    ('MCA', 'Master of Computer Applications'),
    ('MSc', 'Master of Sciences'),
    ('PHD', 'Doctor of Philosophy'),
)

SIMPLIFIED_DEGREE = {
  'B.Tech.':'B.Tech.',
  'B.Arch.':'B.Arch.',
  'IDD': 'Int. Dual Degree',
  'M.Tech.': 'M.Tech.',
  'IMT': 'Int. M.Tech.',
  'IMSc': 'Int. M.Sc.',
  'M.Arch.': 'M.Arch.',
  'MURP': 'M.U.R.P.',
  'PGDip': 'P.G. Dip.',
  'MBA': 'MBA',
  'MCA': 'MCA',
  'MSc': 'M.Sc.',
  'PHD': 'Ph.D.',
}

BANK_NAME= (
    ('PNB','Punjab National Bank'),
    ('SBI', 'State Bank Of India'),
)

DEGREES= {
  'UG':['B.Tech.','B.Arch.','IDD','IMT','IMSc'],
  'PG':['M.Tech.','M.Arch.','MURP','PGDip','MBA','MCA','MSc'],
  'PHD':['PHD']
}    

GRADUATION_CHOICES = (
    ('UG','Under Graduate'),
    ('PG','Post Graduate'),
    ('PHD','PhD')
)

COURSE_CHANGE_CHOICES = (
  ('ADD', 'Course Added'),
  ('DRP', 'Course Dropped'),
)

BHAWAN_CHOICES = (
    ('AZB','Azad Bhawan'),
    ('CTB','Cautley Bhawan'),
    ('GNB','Ganga Bhawan'),
    ('GVB','Govind Bhawan'),
    ('JWB','Jawahar Bhawan'),
    ('RKB','Radhakrishnan Bhawan'),
    ('RJB','Rajendra Bhawan'),
    ('RGB','Rajiv Bhawan'),
    ('RVB','Ravindra Bhawan'),
    ('MVB','Malviya Bhawan'),
    ('SB','Sarojini Bhawan'),
    ('KB','Kasturba Bhawan'),
    ('IB',' Indra Bhawan'),
)

RESIDENTIAL_CHOICES = BHAWAN_CHOICES + (
    ('GPH','GP Hostel'),
    ('MRH','MR Chopra Hostel'),
    ('AZW','Azad Wing Hostel'),
    ('DBH','DS Barrack Hostel'),
    ('AKH','AN Khosla House'),
    ('KIH','Khosla International House'),
    ('NA','Not Applicable'),
)

PHD_INFO_TIME_TYPE_CHOICES = (
    ('FULL', 'Fulltime'),
    ('PART', "Parttime"),
)

SEMESTER_TYPE_CHOICES = (
    ('S', 'Spring'),
    ('A', 'Autumn'),
)

CATEGORY_CHOICES = (
    ('GEN', 'General'),
    ('SC', 'Scheduled Caste'),
    ('ST', 'Scheduled Tribe'),
    ('OBC', 'Other Backward Classes'),
)

MARITAL_STATUS_CHOICES = (
    ('SIN', 'Single'),
    ('MAR', 'Married'),
)

BLOOD_GROUP_CHOICES = (
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
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


def get_integer_tuple(lower_bound, upper_bound):
  """Can use it to generate a drop down list of integers.
     The model field should be of type IntegerField and NOT CharField."""
  l = []
  for x in range(lower_bound, upper_bound):
    l.append((x,x))
  return tuple(l)

def get_value_from_key(choices, key):
  """Use this function to get the value of a choices tuple, given the key."""
  for tup in choices:
    if tup[0] == key:
      return tup[1]
  return None

PRIORITY_CHOICES = get_integer_tuple(1, 25)
import datetime
year = datetime.datetime.now().year
HISTORY_YEAR_CHOICES = get_integer_tuple(year - 100, year + 1)
FUTURE_YEAR_CHOICES = get_integer_tuple(year, year + 10)

# Bug Tracker Constats

BUG_TYPES = (
  ('bug', 'Bug'),
  ('doc', 'Doc'),
  ('feedback', 'Feedback'),
  ('imporvement', 'Improvement'),
  ('newfeat', 'New Feature'),
  )

BUG_STATUS = (
  ('new', 'New'),
  ('assigned', 'Assigned'),
  ('resolved', 'Resolved'),
  ('closed', 'Closed'),
  )

RAILWAY_CHOICES = (
    ('ABR', 'ABU ROAD - ABR'),
    ('AGC', 'AGRA CANTT - AGC'),
    ('AF', 'AGRA FORT - AF'),
    ('AGA', 'AGRA CITY - AGA'),
    ('ADI', 'AHMEDABAD JN - ADI'),
    ('AII', 'AJMER - AII'),
    ('AK', 'AKOLA - AK'),
    ('ALJN', 'ALIGARH JN - ALJN'),
    ('ALD', 'ALLAHABAD - ALD'),
    ('ALLP', 'ALLEPPEY - ALLP'),
    ('AWR', 'ALWAR - AWR'),
    ('AWY', 'ALWAYE - AWY'),
    ('UMB', 'AMBALA - UMB'),
    ('AME', 'AMETHI - AME'),
    ('AMI', 'AMRAVATI - AMI'),
    ('ASR', 'AMRITSAR - ASR'),
    ('ASN', 'ASANSOL JN - ASN'),
    ('AWB', 'AURANGABAD - AWB'),
    ('AMH', 'AZAMGARH - AMH'),
    ('BRK', 'BAHRAICH - BRK'),
    ('SBC', 'BANGALORE - SBC'),
    ('BUI', 'BALLIA - BUI'),
    ('BWT', 'BANGARAPET - BWT'),
    ('BP', 'BARRACKPORE - BP'),
    ('BJU', 'BARAUNI JN - BJU'),
    ('BE', 'BAREILLY - BE'),
    ('BST', 'BASTI - BST'),
    ('BSL', 'BHUSAVAL - BSL'),
    ('BGS', 'BEGU SARAI - BGS'),
    ('BGM', 'BELGAUM - BGM'),
    ('BAY', 'BELLARY - BAY'),
    ('BGP', 'BHAGALPUR - BGP'),
    ('BKN', 'BIKANER JN - BKN'),
    ('BSP', 'BILASPUR - BSP'),
    ('BINA', 'BINA - BINA'),
    ('BPL', 'BHOPAL - BPL'),
    ('BTI', 'BHATINDA - BTI'),
    ('BKSC', 'BOKARO STL CITY - BKSC'),
    ('BBS', 'BHUBANESHWAR - BBS'),
    ('BWN', 'BURDWAN - BWN'),
    ('BXR', 'BUXAR - BXR'),
    ('CLT', 'CALICUT - CLT'),
    ('CDG', 'CHANDIGARH - CDG'),
    ('MAS', 'CHENNAI - MAS'),
    ('CHTS', 'COCHIN - CHTS'),
    ('CRJ', 'CHITTARANJAN - CRJ'),
    ('CBE', 'COIMBATORE JN - CBE'),
    ('DBG', 'DARBHANGA JN - DBG'),
    ('DJ', 'DARJEELING - DJ'),
    ('DDN', 'DEHRADUN - DDN'),
    ('DHN', 'DHANBAD JN - DHN'),
    ('DWR', 'DHARWAR - DWR'),
    ('DURG', 'DURG - DURG'),
    ('DBRT', 'DIBRUGARH TOWN - DBRT'),
    ('ERS', 'ERNAKULAM - ERS'),
    ('ED', 'ERODE - ED'),
    ('FD', 'FAIZABAD JN - FD'),
    ('FDB', 'FARIDABAD - FDB'),
    ('FBD', 'FARUKHABAD - FBD'),
    ('GAYA', 'GAYA JN - GAYA'),
    ('G', 'GONDIA - G'),
    ('GKP', 'GORAKHPUR JN - GKP'),
    ('GR', 'GULBARGA - GR'),
    ('GNT', 'GUNTUR - GNT'),
    ('GHY', 'GUWAHATI - GHY'),
    ('GWL', 'GWALIOR - GWL'),
    ('HBJ', 'HABIBGANJ - HBJ'),
    ('HWH', 'HOWRAH - HWH'),
    ('HYB', 'HYDERABAD - HYB'),
    ('INDB', 'INDORE JN BG - INDB'),
    ('ET', 'ITARSI - ET'),
    ('JBP', 'JABALPUR - JBP'),
    ('JP', 'JAIPUR - JP'),
    ('JSM', 'JAISALMER - JSM'),
    ('JUC', 'JALANDHAR CITY - JUC'),
    ('JAT', 'JAMMU - JAT'),
    ('JHS', 'JHANSI JN - JHS'),
    ('JU', 'JODHPUR - JU'),
    ('KLK', 'KALKA - KLK'),
    ('CNB', 'KANPUR - CNB'),
    ('CAPE', 'KANYAKUMARI - CAPE'),
    ('KGM', 'KATHGODAM - KGM'),
    ('KPD', 'KATPADI - KPD'),
    ('HWH', 'KOLKATA - HWH'),
    ('KOTA', 'KOTA JN - KOTA'),
    ('KZJ', 'KAZIPET - KZJ'),
    ('LKO', 'LUCKNOW - LKO'),
    ('LDH', 'LUDHIANA - LDH'),
    ('MAO', 'MADGAON - MAO'),
    ('MDU', 'MADURAI - MDU'),
    ('MMC', 'MAHAMANDIR - MMC'),
    ('MAQ', 'MANGALORE - MAQ'),
    ('MMR', 'MANMAD - MMR'),
    ('MTJ', 'MATHURA JN - MTJ'),
    ('MAU', 'MAU JN - MAU'),
    ('MTC', 'MEERUT CITY - MTC'),
    ('MB', 'MORADABAD - MB'),
    ('MGS', 'MUGHAL SARAI - MGS'),
    ('BCT', 'MUMBAI - BCT'),
    ('MYS', 'MYSORE - MYS'),
    ('NGP', 'NAGPUR - NGP'),
    ('NK', 'NASIK - NK'),
    ('NLR', 'NELLORE - NLR'),
    ('NJP', 'NEW JALPAIGURI - NJP'),
    ('NDLS', 'NEW DELHI - NDLS'),
    ('PGT', 'PALGHAT - PGT'),
    ('PNP', 'PANIPAT JN - PNP'),
    ('PTA', 'PATIALA - PTA'),
    ('PNBE', 'PATNA JN - PNBE'),
    ('PUNE', 'PUNE JN - PUNE'),
    ('RBL', 'RAE BARELI JN - RBL'),
    ('RIG', 'RAIGARH - RIG'),
    ('R', 'RAIPUR - R'),
    ('RMM', 'RAMESWARAM - RMM'),
    ('RNC', 'RANCHI - RNC'),
    ('RRME', 'RANCHI ROAD - RRME'),
    ('RTM', 'RATLAM - RTM'),
    ('RN', 'RATNAGIRI - RN'),
    ('REWA', 'REWA - REWA'),
    ('ROK', 'ROHTAK - ROK'),
    ('RKSH', 'RISHIKESH - RKSH'),
    ('RK', 'ROORKEE - RK'),
    ('ROU', 'ROURKELA - ROU'),
    ('SRE', 'SAHARANPUR - SRE'),
    ('SA', 'SALEM - SA'),
    ('SLI', 'SANGLI - SLI'),
    ('STA', 'SATNA - STA'),
    ('SNP', 'SONIPAT - SNP'),
    ('SCL', 'SILCHAR - SCL'),
    ('SML', 'SIMLA - SML'),
    ('SVKS', 'SIVAKASI - SVKS'),
    ('ST', 'SURAT - ST'),
    ('TATA', 'TATANAGAR JN - TATA'),
    ('TNA', 'THANE - TNA'),
    ('TJ', 'THANJAVUR - TJ'),
    ('TPTY', 'TIRUPATI - TPTY'),
    ('TPJ', 'TIRUCHIRAPALLI - TPJ'),
    ('TCR', 'TRICHUR - TCR'),
    ('TVC', 'TRIVANDRUM - TVC'),
    ('TN', 'TUTICORIN - TN'),
    ('UDZ', 'UDAIPUR - UDZ'),
    ('UJN', 'UJJAIN - UJN'),
    ('BRC', 'VADODARA - BRC'),
    ('BSB', 'VARANASI JN - BSB'),
    ('VSG', 'VASCO DA GAMA - VSG'),
    ('BZA', 'VIJAYAWADA JN - BZA'),
    ('VSKP', 'VISHAKAPATNAM - VSKP'),
    ('WL', 'WARANGAL - WL'),
    ('WR', 'WARDHA - WR')
    )
