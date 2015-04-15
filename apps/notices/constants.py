OPTIONS = (
  ('Placement', 'Placement'),
  ('Authorities', 'Authorities'),
  ('Departments', 'Departments'),
  ('Bhawans', 'Bhawans'),
  ('All', 'All'),
  )

AUTHORITIES = (
  ('A_All','All'),
  ('acad','Academics'),
  ('CPO','CPO'),
  ('DOSW','DOSW'),
  ('alumni','Alumni Affairs'),
  ('cnst','Construction'),
  ('clib','Central Library'),
  ('CD','CD'),
  ('dean','Deans'),
  ('hod','Heads'),
  ('hspl','Hospital'),
  ('rgst','Registrar'),
  ('finc','Finance'),
  ('pstd','Ps to Director'),
  ('stdd','Steno to Deputy Director'),
  ('QIP','QIP'),
  ('snt','Senate'),
  ('ISC','ISC'),
  )

BHAWANS = (
  ('B_All','All'),
  ('azd','Azad'),
  ('ctl','Cautley'),
  ('gng','Ganga'),
  ('gvnd','Govind'),
  ('jwhr','Jawahar'),
  ('rjnd','Rajendra'),
  ('rvnd','Ravindra'),
  ('srjn','Sarojini'),
  ('kstr','Kasturba'),
  ('mlvy','Malviya'),
  ('rjv','Rajeev'),
  ('rkb','Radhakrishnan'),
  )

DEPARTMENTS = (
  ('D_All','All'),
  ('ahec','Alternative Hydro Energy Centre'),
  ('arch','Architecture and Planning'),
  ('bt','Biotechnology'),
  ('chem','Chemical'),
  ('cvl','Civil'),
  ('cy','Chemistry'),
  ('erts','Earth Science'),
  ('ertq','Earthquake'),
  ('ee','Electrical'),
  ('ec','Electronics and Computer Science'),
  ('hydr','Hydrology'),
  ('hs','Humanities'),
  ('dpt','DPT'),
  ('ms','Management Studies'),
  ('mi','Mechanical and Indstrial'),
  ('meta','Metallurgy'),
  ('ph','Physics'),
  ('wtr','Water Resources Development and Management'),
  ('icc','Institute Computer Centre'),
  )

AUTHORITIES_LIST = ["All", "Academics", "CPO", "DOSW", "Alumni Affairs", "Construction", "Central Library", "CD", "Deans", "Heads", "Hospital", "Registrar", "Finance", "Ps to Director", "Steno to Deputy Director", "QIP", "Senate", "ISC"]
DEPARTMENTS_LIST = ["All", "Alternative Hydro Energy Centre", "Architecture and Planning", "Biotechnology", "Chemical", "Civil", "Chemistry", "Earth Science", "Earthquake", "Electrical", "Electronics and Computer Science", "Hydrology", "Humanities", "DPT", "Management Studies", "Mechanical and Indstrial", "Metallurgy", "Physics", "WRDM", "Institute Computer Centre"]


MAIN_CATEGORIES = {
  'All' : [],
  'Placement' : [],
  'Authorities' : AUTHORITIES_LIST,
  'Departments': DEPARTMENTS_LIST
}

MAIN_CATEGORIES_CHOICES = (
  ('Placement', 'Placement'),
  ('Authorities', 'Authorities'),
  ('Departments', 'Departments'),
)
