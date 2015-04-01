INTERNSHIP_STATUS_CHOICES = (
      ('CLS', 'Closed'),
      ('OPN', 'Opened'),
    )

#variable name should be APPLICATION_STATUS_CHOICES
COMPANY_STATUS_CHOICES = (
      ('OPN', 'OPEN'),
      ('CLS', 'CLOSED'),
      ('DEC', 'DECLARED')
    )

COMPANY_SECTORS = (
      ('NA', 'Not Applicable'),
      ('FI', 'Finance'),
      ('PG', 'PSU/Government'),
      ('CO', 'Consultancy'),
      ('FM', 'FMCG'),
      ('PH', 'Pharmaceuticals'),
      ('RD', 'R&D'),
      ('IT', 'IT'),
      ('AC', 'Academics'),
      ('OG', 'Oil & Gas'),
      ('CI', 'Construction/Infrastructure'),
      ('CE', 'Core Engineering'),
    )

FORUM_CHOICES = (
      ('T', 'Technical'),
      ('P', 'Placement'),
    )

COMPANY_APPLICATION_STATUS = (
      ('APP','Applied'),
      ('FIN','Finalized'),
      ('SEL','Selected'),
    )

FEEDBACK_QUESTIONS = (
  '1. How did you prepare for this company & when did you start ? (Provide links of video lectures/web pages etc.)',
  '2. What was the profile offered by the company?',
  '3. Briefly explain the preliminary process (Written test/Online test - Technical/Aptitude/Programming and level of questions)',
  '4. Provide details of GD (if applicable) and discuss the topic/case study and the required qualities that the company was looking for.',
  '5. Describe the interview process (Duration/No.of rounds - Also discuss the solutions of problems/puzzles/case study asked)',
  '6. Provide details of companies in which you got shortlisted before your final placement and give possible reasons for your elimination from the company\'s process.',
  '7. Provide your facebook profile link and email address.',
  '8. Other comments/feedback that you think may be helpful.',
  )

PAY_PACKAGE_CURRENCY_CHOICES = (
  ('INR', 'INR'),
  ('USD', 'USD'),
  )

PAY_WHOLE_CHOICES = (
  ('Thousands', 'Thousands'),
  ('Lacs', 'Lacs'),
  )

PAY_PACKAGE_CURRENCY_CONVERSION_RATES = {
  'INR' : 1,
  'USD' : 50,
  }
