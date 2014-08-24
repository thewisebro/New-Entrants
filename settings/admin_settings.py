from development import CHANNELI_APPS, THIRD_PARTY_APPS, DJANGO_CONTRIB_APPS

ADMIN_REORDER = (
  {
    'app': 'auth',
    'label': 'Main Models',
    'models': (
      'nucleus.User',
      'auth.Group',
      'nucleus.Student',
      'nucleus.StudentInfo',
      'nucleus.WebmailAccount',
      'nucleus.Faculty',
      'nucleus.GlobalVar',
    ),
  },
)

TOP_ADMIN_APPS = (
  'nucleus',
  'academics',
  'regol',
)

ADMIN_REORDER += TOP_ADMIN_APPS

ALL_APPS = DJANGO_CONTRIB_APPS + CHANNELI_APPS + THIRD_PARTY_APPS

for app in ALL_APPS :
  app = app.split('.')[-1]
  if not app in (TOP_ADMIN_APPS + ('auth',)):
    ADMIN_REORDER += (app,)
