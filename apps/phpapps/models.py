from django.db import models

class LectutDesignChoice(models.Model):
    id = models.BigIntegerField(primary_key=True)
    faculty_id = models.CharField(max_length=45)
    choice = models.IntegerField()
    class Meta:
        db_table = u'lectut_design_choice'

class LectutExamPapers(models.Model):
    id = models.BigIntegerField(primary_key=True)
    faculty_id = models.CharField(max_length=45)
    course_id = models.CharField(max_length=24)
    file = models.CharField(max_length=450)
    topic = models.CharField(max_length=450)
    permission = models.IntegerField()
    timestamp = models.DateTimeField()
    year = models.CharField(max_length=45, blank=True)
    class Meta:
        db_table = u'lectut_exam_papers'

class LectutLectures(models.Model):
    id = models.BigIntegerField(primary_key=True)
    faculty_id = models.CharField(max_length=45)
    course_id = models.CharField(max_length=24)
    file = models.CharField(max_length=450)
    topic = models.CharField(max_length=450)
    permission = models.IntegerField()
    timestamp = models.DateTimeField()
    class Meta:
        db_table = u'lectut_lectures'

class LectutSolutions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    faculty_id = models.CharField(max_length=45)
    course_id = models.CharField(max_length=24)
    file = models.CharField(max_length=450)
    topic = models.CharField(max_length=450)
    permission = models.IntegerField()
    timestamp = models.DateTimeField()
    link_type = models.CharField(max_length=3, blank=True)
    link_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'lectut_solutions'

class LectutTutorials(models.Model):
    id = models.BigIntegerField(primary_key=True)
    faculty_id = models.CharField(max_length=45)
    course_id = models.CharField(max_length=24)
    file = models.CharField(max_length=450)
    topic = models.CharField(max_length=450)
    permission = models.IntegerField()
    timestamp = models.DateTimeField()
    class Meta:
        db_table = u'lectut_tutorials'




class VleAdmin(models.Model):
    slno = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30, blank=True)
    perm = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'vle_admin'

class VleAnsagree(models.Model):
    aid = models.IntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=30, blank=True)
    slno = models.IntegerField(primary_key=True)
    qid = models.IntegerField(null=True, blank=True)
    agree = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'vle_ansagree'

class VleAnswers(models.Model):
    ans_id = models.IntegerField(primary_key=True)
    qid = models.IntegerField(null=True, blank=True)
    ans = models.TextField(blank=True)
    post_time = models.DateTimeField()
    user_id = models.CharField(max_length=30, blank=True)
    flagger = models.CharField(max_length=30, blank=True)
    flag = models.IntegerField(null=True, blank=True)
    agrees = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'vle_answers'

class VleCategory(models.Model):
    category = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'vle_category'

class VleFiles(models.Model):
    fid = models.IntegerField(primary_key=True)
    qid = models.IntegerField(null=True, blank=True)
    aid = models.IntegerField(null=True, blank=True)
    filename = models.CharField(max_length=150, blank=True)
    upload_time = models.DateTimeField()
    mimetype = models.CharField(max_length=420, blank=True)
    class Meta:
        db_table = u'vle_files'

class VleFollowuser(models.Model):
    slno = models.IntegerField(primary_key=True)
    followed = models.CharField(max_length=30, blank=True)
    follower = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'vle_followuser'

class VleQfollowed(models.Model):
    qid = models.IntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=30, blank=True)
    sl = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'vle_qfollowed'

class VleQuesliked(models.Model):
    sl = models.IntegerField(primary_key=True)
    qid = models.IntegerField(null=True, blank=True)
    user_id = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'vle_quesliked'

class VleQuestions(models.Model):
    qid = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=30, blank=True)
    text = models.TextField(blank=True)
    post_time = models.DateTimeField()
    last_activity = models.DateTimeField()
    category = models.CharField(max_length=30, blank=True)
    status = models.IntegerField(null=True, blank=True)
    tags = models.CharField(max_length=300, blank=True)
    files = models.CharField(max_length=3000, blank=True)
    open = models.IntegerField(null=True, blank=True)
    flag = models.IntegerField(null=True, blank=True)
    flagger = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'vle_questions'

class VleUsers(models.Model):
    sl = models.IntegerField(primary_key=True)
    user_id = models.CharField(max_length=24, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=240, blank=True)
    class Meta:
        db_table = u'vle_users'
        
