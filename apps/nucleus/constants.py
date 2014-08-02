tabs = [
  ('home', False, [], 'fa fa-home', '#41AAF0'),
  ('apps', False, [], 'fa fa-th-large', '#F14D39'),
  ('events', False, [], 'fa fa-calendar', '#2ECC71'),
  ('notices',False , [], 'typcn typcn-pin', '#33EECA'),
  ('games', True, ['Student'], 'fa fa-gamepad', '#EBEB3D'),
  ('groups', False, [], 'fa fa-group', '#ACE93E'),
  ('links', False, [], 'fa fa-list-ul', '#D1D1D1'),
  ('news', False, [], 'typcn typcn-flash', '#69E6F7'),
  ('forum', True, ['Student'], 'fa fa-comments', '#C55DF0'),
]

channeli_apps = {
  'events': {'name': 'Events', 'url':'/#events'},
  'lectut' : {'name':'Lectures & Tutorials', 'url':'/lectut/'},
  'placement' : {'name':'Placement Online', 'url':'/placement/'},
  'internship' : {'name':'Internship', 'url':'/internship/'},
  'thinktank' : {'name':'Thinktank', 'url':'/thinktank/'},
  'lostfound' : {'name':'Lost & Found', 'url':'/lostfound/'},
  'buysell' : {'name':'Buy & Sell', 'url':'/buysell/'},
  'ebooks' : {'name':'E-Books', 'url':'/ebooks/'},
  'vle' : {'name':'VLE', 'url':'/vle/'},
  'games' : {'name':'Games', 'url':'/games/'},
  'jukebox' : {'name':'JukeBox', 'url':'/jukebox/'},
  'notices' : {'name':'Notice-Board', 'url':'/notices/'},
  'grades' : {'name':'Grades Online', 'url':'/grades/'},
  'androidnotices' : {'name':'Notice-Board Android App',
    'url':'https://market.android.com/details?id=in.ernet.iitr.people'},
  'notices' : {'name':'Notice-Board', 'url':'/notices/'},
  'kriti' : {'name':'Kriri', 'url':'/kriti/'},
  'facapp' : {'name':'Faculty Profile', 'url':'/facapp/'},
  'softwares':{'name':'Download Softwares', 'url':'/softwares/'},
  'messmenu' : {'name':'Mess Menu', 'url':'/messmenu/'},
  'helpcenter' : {'name':'Help Center', 'url':'/helpcenter/'},
  'peoplesearch' : {'name':'People Search',
    'url':'http://people.iitr.ernet.in/PeopleSearch/'
  },
  'research' : {'name':'Research Assistant', 'url':'/research_assistant/'},
  'facultyfilemanager' : {'name':'File Manager', 'url':'/settings/filemanager/'},
  'acad' : {'name':'Response Forms', 'url':'/acad/responses/'},
}

student_apps = ['events', 'grades','lectut','notices','placement','buysell','vle','thinktank',
                'lostfound','softwares','peoplesearch','messmenu','research']
faculty_apps = ['facapp','events','lectut','notices','placement',
                'thinktank','lostfound','softwares','peoplesearch']
other_apps = ['events', 'lectut','notices','placement','thinktank',
              'lostfound','softwares','peoplesearch']


external_links = {
  'imglink' : {'name':'Information Management Group',
    'url':'http://www.iitr.ac.in/campus_life/pages/Groups_and_Societies+IMG.html'
  },
  'iitr' : {'name':'IITR Home', 'url':'http://www.iitr.ac.in'},
  'webmail' : {'name':'Webmail', 'url':'http://mail.iitr.ac.in/iwc'},
  'library' : {'name':'Library', 'url':'http://mgcl.iitr.ac.in'},
  'antivirus' : {'name':'Anti virus',
    'url':'http://www.iitr.ac.in/centers/ISC/pages/Antivirus_Solution_for_Campus.html'
  },
}

login_page_links = ['library','webmail','notices','iitr','antivirus']

channeli_links = [
  {'name':'Instruments Search','url':'/equipments/'},
  {'name':'Campus Lynx',
    'url':'http://acadinfo2.iitr.ernet.in/CampusLynxIITR/CampusLynxFx/CampusLynxFx.swf'
  },
  {'name':'Wifi Registration','url':'/wifi/'},
  {'name':'Telephone Directory','url':'/static/pdfs/teldir-oct2013.pdf'},
  {'name':'Meeting Section','url':'/meeting_minutes/'},
  {'name':'Dairy Reports','url':'/meeting_minutes/dairy.php'},
  {'name':'Forms','url':'/forms/'},
  #{'name':'Scholarship Form','url':'/mcm/mcm/'},
]

channeli_links = map(lambda n:external_links[n],['iitr','webmail','library']) + channeli_links
