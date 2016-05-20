package img.myapplication;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;
import java.util.List;

import models.JuniorModel;
import models.NewEntrantModel;
import models.RequestModel;
import models.SeniorModel;
import models.StudentModel;


public class MySQLiteHelper extends SQLiteOpenHelper {
    // Database Version
    private static final int DATABASE_VERSION = 1;
    // Database Name
    public static final String DATABASE_NAME = "Entrants_Data";

    private static final String TABLE_SENIORS="seniors";
    private static final String TABLE_REQUESTS = "requests";
    private static final String TABLE_BLOGS= "blogs";
    private static final String TABLE_JUNIORS="juniors";
    private static final String TABLE_STUDENTS="students";
    private static final String TABLE_ENTRANTS="entrants";

    private static String CREATE_SENIORS_TABLE=
            "create table if not exists seniors ( "+
                    "name varchar," +
                    "branch varchar,"+
                    "state varchar,"+
                    "town varchar,"+
                    "contact varchar,"+
                    "email varchar,"+
                    "fblink varchar,"+
                    "dp_link varchar,"+
                    "year int(1),"+
                    "unique(name,email) on conflict replace );";
    private static String TEMP_SENIOR=
            "insert into seniors values('asd','ee','uk','rk','1234567899','a@a.com','fb/asd','https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/User_icon_2.svg/2000px-User_icon_2.svg.png',2);";
    private static String CREATE_REQUESTS_TABLE=
            "create table if not exists requests ( "+
                    "param varchar,"+
                    "value varchar,"+
                    "id int,"+
                    "accepted int,"+
                    "more int(1),"+
                    "query varchar,"+
                    "date varchar,"+
                    "allowed int,"+
                    "request_no int," +
                    "unique(id) on conflict replace );";
    private static String TEMP_REQUEST=
            "insert into requests values('Location','GUJ',12,3,1,'HELP','12-3-16',5,56);";
    private static String CREATE_JUNIORS_TABLE=
            "create table if not exists juniors ( "+
                    "name varchar,"+
                    "username varchar,"+
                    "branch varchar,"+
                    "state varchar,"+
                    "town varchar,"+
                    "email varchar,"+
                    "mobile varchar,"+
                    "fblink varchar,"+
                    "description varchar,"+
                    "status varchar,"+
                    "unique(username) on conflict replace);";

    private static String CREATE_STUDENTS_TABLE=
            "create table if not exists students ( "+
                "name varchar,"+
                "enr_no char(8),"+
                "username varchar,"+
                "password varchar,"+
                "branchname varchar,"+"branchcode varchar,"+
                "year char(1),"+
                "town varchar,"+
                "state varchar,"+"statecode varchar,"+
                "email varchar,"+
                "mobile varchar,"+
                "fb_link varchar,"+
                "sess_id varchar,"+
                "img blob,"+
                "category char(10),"+
                "primary key(enr_no) on conflict replace );";

    public static String TEMP_STUDENT=
            "insert into students values ('ankush','','14115019','asd','ee','EE','2','roorkee','uk','UK','a@a.a','8006572222','fb.com/spunk','','','senior');";
    public static String TEMP_AUDIENCE=
            "insert into students values ('ankush','','14115019','asd','ee','EE','2','roorkee','uk','UK','a@a.a','8006572222','fb.com/spunk','','','audience');";

    private static String CREATE_ENTRANTS_TABLE=
            "create table if not exists entrants ( "+
                    "id text,"+
                    "name varchar,"+
                    "username varchar,"+
                    "password varchar,"+
                    "branchname varchar,"+"branchcode varchar,"+
                    "town varchar,"+
                    "state varchar,"+"statecode varchar,"+
                    "email varchar,"+
                    "mobile varchar,"+
                    "fb_link varchar,"+
                    "phone_privacy int(1),"+
                    "profile_privacy int(1),"+
                    "sess_id varchar,"+
                    "primary key(id) on conflict replace );";

    public static String TEMP_ENTRANT=
            "insert into entrants values ('1','singh','asd','asd','ee','EE','roorkee','uk','UK','a@a.a','123','fb.com/spunk',0,1,NULL);";
    public static String TEMP_BLOG=
            "insert into blogs values ('topic','short info','group','2016-02-04','content');";
    public static String TEMP_PENDING_JUNIOR=
            "insert into juniors values ('asd','ass','ee','delhi','gurgaon','asd@asd.com','1231231231','fb.com/spunk','smart','pending');";
    public static String TEMP_JUNIOR=
            "insert into juniors values ('asd','asd','ee','delhi','gurgaon','asd@asd.com','1231231231','fb.com/spunk','smart','accepted');";
    public MySQLiteHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);

        SQLiteDatabase db=this.getWritableDatabase();
        //db.execSQL("DROP TABLE IF EXISTS seniors");
        //db.execSQL("DROP TABLE IF EXISTS students");
        //db.execSQL("DROP TABLE IF EXISTS entrants");
        //db.execSQL("drop table if exists juniors");
        //db.execSQL("drop table if exists requests");
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.execSQL(CREATE_ENTRANTS_TABLE);
        //db.execSQL(TEMP_ENTRANT);
        //db.execSQL(TEMP_STUDENT);
        //db.execSQL(TEMP_AUDIENCE);
        db.execSQL(CREATE_SENIORS_TABLE);
        db.execSQL(CREATE_REQUESTS_TABLE);
        db.execSQL(CREATE_JUNIORS_TABLE);
        //db.execSQL(TEMP_REQUEST);
        //db.execSQL(TEMP_SENIOR);
        //db.execSQL(TEMP_JUNIOR);
        //db.execSQL(TEMP_PENDING_JUNIOR);
        db.close();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS juniors");
        db.execSQL("DROP TABLE IF EXISTS students");
        db.execSQL("DROP TABLE IF EXISTS entrants");
        db.execSQL("DROP TABLE IF EXISTS seniors");
        db.execSQL("DROP TABLE IF EXISTS requests");
        this.onCreate(db);
    }

    public StudentModel getStudent(){
        SQLiteDatabase db= this.getReadableDatabase();
        StudentModel student=new StudentModel();

        Cursor cursor=db.rawQuery("select * from students;", null);
        if (cursor.getCount()!=0) {
            cursor.moveToFirst();

            student.enr_no= cursor.getString(1);
            student.name= cursor.getString(0);
            student.username=cursor.getString(2);
            student.password= cursor.getString(3);
            student.branchname= cursor.getString(4);
            student.branchcode=cursor.getString(5);
            student.year= cursor.getString(6);
            student.town= cursor.getString(7);
            student.state= cursor.getString(8);
            student.statecode=cursor.getString(9);
            student.email= cursor.getString(10);
            student.mobile= cursor.getString(11);
            student.fb_link=cursor.getString(12);
            student.sess_id=cursor.getString(13);
            student.profile_img=cursor.getBlob(14);
            student.category=cursor.getString(15);
        }
        db.close();
        return student;
    }
    public boolean loggedSenior(){
        SQLiteDatabase db= this.getWritableDatabase();
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.close();
        db=this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from students where category='senior' ;", null);

        int count=cursor.getCount();
        db.close();
        if(count==0)
            return false;
        else
            return true;
    }
    public boolean loggedAudience(){
        SQLiteDatabase db= this.getWritableDatabase();
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.close();
        db=this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from students where category='audience' ;", null);

        int count=cursor.getCount();
        db.close();
        if(count==0)
            return false;
        else
            return true;
    }
    public void addStudent(StudentModel student){
        SQLiteDatabase db=this.getWritableDatabase();
        ContentValues values=new ContentValues();
        values.put("name",student.name);
        values.put("enr_no",student.enr_no);
        values.put("username",student.username);
        values.put("password",student.password);
        values.put("branchname",student.branchname);
        values.put("branchcode",student.branchcode);
        values.put("year",student.year);
        values.put("town",student.town);
        values.put("state",student.state);
        values.put("statecode",student.statecode);
        values.put("email",student.email);
        values.put("mobile",student.mobile);
        values.put("fb_link", student.fb_link);
        values.put("sess_id",student.sess_id);
        values.put("img",student.profile_img);
        values.put("category",student.category);
        db.insert(TABLE_STUDENTS,null,values);
        db.close();
    }
    public void addEntrant(NewEntrantModel entrant){
        SQLiteDatabase db=this.getWritableDatabase();
        ContentValues values=new ContentValues();
        values.put("id", entrant.id);
        values.put("name", entrant.name);
        values.put("username", entrant.username);
        values.put("password", entrant.password);
        values.put("email", entrant.email);
        values.put("branchname", entrant.branchname);
        values.put("branchcode",entrant.branchcode);
        values.put("town", entrant.town);
        values.put("state", entrant.state);
        values.put("statecode",entrant.statecode);
        values.put("mobile", entrant.mobile);
        values.put("fb_link",entrant.fb_link);
        values.put("phone_privacy",entrant.phone_privacy);
        values.put("profile_privacy",entrant.profile_privacy);
        values.put("sess_id",entrant.sess_id);
        db.insert(TABLE_ENTRANTS, null, values);
        db.close();
    }
    public void addJunior(JuniorModel junior){
        SQLiteDatabase db=this.getWritableDatabase();
        ContentValues values=new ContentValues();
        values.put("name",junior.name);
        values.put("username",junior.username);
        values.put("branch",junior.branch);
        values.put("state",junior.state);
        values.put("town",junior.town);
        values.put("email",junior.email);
        values.put("mobile",junior.mobile);
        values.put("fblink",junior.fblink);
        values.put("description",junior.description);
        values.put("status",junior.status);
        db.insert(TABLE_JUNIORS, null, values);
        db.close();
    }
    public void addSenior(SeniorModel senior){
            SQLiteDatabase db=this.getWritableDatabase();
            ContentValues values=new ContentValues();
            values.put("name",senior.name);
            values.put("branch",senior.branch);
            values.put("state", senior.state);
            values.put("town",senior.town);
            values.put("contact",senior.contact);
            values.put("email",senior.email);
            values.put("fblink",senior.fblink);
            values.put("dp_link",senior.dp_link);
            values.put("year",senior.year);
            db.insert(TABLE_SENIORS, null, values);
            db.close();
    }
    public void addRequest(RequestModel request){
        SQLiteDatabase db=this.getWritableDatabase();
        ContentValues values=new ContentValues();
        values.put("param",request.param);
        values.put("value",request.value);
        values.put("id",request.id);
        values.put("accepted",request.accepted);
        values.put("more",request.more);
        values.put("query",request.query);
        values.put("date",request.date);
        values.put("allowed",request.allowed);
        values.put("request_no",request.request_no);
        db.insert(TABLE_REQUESTS, null, values);
        db.close();
    }
    public boolean loggedEntrant(){
        SQLiteDatabase db= this.getWritableDatabase();
        db.execSQL(CREATE_ENTRANTS_TABLE);
        db.close();
        db=this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from entrants ;", null);

        int count=cursor.getCount();
        db.close();
        if(count==0)
            return false;
        else
            return true;
    }
    public NewEntrantModel getEntrant(){
        SQLiteDatabase db= this.getReadableDatabase();
        NewEntrantModel entrant=new NewEntrantModel();

        Cursor cursor=db.rawQuery("select * from entrants;", null);
        if (cursor.getCount()!=0) {
            cursor.moveToFirst();

            entrant.id = cursor.getString(0);
            entrant.name = cursor.getString(1);
            entrant.username = cursor.getString(2);
            entrant.password = cursor.getString(3);
            entrant.branchname = cursor.getString(4);
            entrant.branchcode=cursor.getString(5);
            entrant.town = cursor.getString(6);
            entrant.state = cursor.getString(7);
            entrant.statecode=cursor.getString(8);
            entrant.email = cursor.getString(9);
            entrant.mobile = cursor.getString(10);
            entrant.fb_link=cursor.getString(11);
            entrant.phone_privacy=cursor.getInt(12) >0;
            entrant.profile_privacy=cursor.getInt(13) > 0;
            entrant.sess_id=cursor.getString(14);
        }
        db.close();
        return entrant;
    }
    public int getAcceptedSeniorsCount(){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from seniors", null);
        int count=cursor.getCount();
        db.close();
        return count;
    }
    public List<SeniorModel> getAcceptedSeniors(){
        SQLiteDatabase db= this.getReadableDatabase();
        List<SeniorModel> seniorsList=new ArrayList<SeniorModel>();
        Cursor cursor=db.rawQuery("select * from seniors", null);
        if (cursor.moveToFirst()){
            do {
                SeniorModel senior=new SeniorModel();
                senior.name=cursor.getString(0);
                senior.branch=cursor.getString(1);
                senior.state=cursor.getString(2);
                senior.town=cursor.getString(3);
                senior.contact=cursor.getString(4);
                senior.email=cursor.getString(5);
                senior.fblink=cursor.getString(6);
                senior.dp_link=cursor.getString(7);
                senior.year=cursor.getInt(8);
                seniorsList.add(senior);
            }
            while (cursor.moveToNext());
        }
        db.close();
        return seniorsList;
    }
    public List<RequestModel> getRequests(){
        SQLiteDatabase db= this.getReadableDatabase();
        List<RequestModel> requestsList=new ArrayList<RequestModel>();
        Cursor cursor=db.rawQuery("select * from requests;", null);
        if (cursor.moveToFirst()){
            do {
                RequestModel request=new RequestModel();
                request.param=cursor.getString(0);
                request.value=cursor.getString(1);
                request.id=cursor.getInt(2);
                request.accepted=cursor.getInt(3);
                request.more=cursor.getInt(4)>0;
                request.query=cursor.getString(5);
                request.date=cursor.getString(6);
                request.allowed=cursor.getInt(7);
                request.request_no=cursor.getInt(8);
                requestsList.add(request);
            }
            while (cursor.moveToNext());
        }
        db.close();
        return requestsList;
    }
    public List<JuniorModel> getAcceptedJuniors(){
        SQLiteDatabase db= this.getReadableDatabase();
        List<JuniorModel> juniorsList=new ArrayList<JuniorModel>();
        Cursor cursor=db.rawQuery("select * from juniors where status='accepted';", null);
        if (cursor.moveToFirst()){
            do {
                JuniorModel junior=new JuniorModel();
                junior.name=cursor.getString(0);
                junior.username=cursor.getString(1);
                junior.branch=cursor.getString(2);
                junior.state=cursor.getString(3);
                junior.town=cursor.getString(4);
                junior.email=cursor.getString(5);
                junior.mobile=cursor.getString(6);
                junior.fblink=cursor.getString(7);
                junior.description=cursor.getString(8);
                juniorsList.add(junior);
            }
            while (cursor.moveToNext());
        }
        db.close();
        return juniorsList;
    }
    public int getPendingJuniorsCount(){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor = db.rawQuery("select * from juniors where status='pending';", null);
        int count=cursor.getCount();
        db.close();
        return count;
    }
    public List<JuniorModel> getPendingJuniors(){
        SQLiteDatabase db= this.getReadableDatabase();
        List<JuniorModel> juniorsList=new ArrayList<JuniorModel>();
        Cursor cursor=db.rawQuery("select * from juniors where status='pending';", null);
        if (cursor.moveToFirst()){
            do {
                JuniorModel junior=new JuniorModel();
                junior.name=cursor.getString(0);
                junior.username=cursor.getString(1);
                junior.branch=cursor.getString(2);
                junior.state=cursor.getString(3);
                junior.town=cursor.getString(4);
                junior.email=cursor.getString(5);
                junior.mobile=cursor.getString(6);
                junior.fblink=cursor.getString(7);
                junior.description=cursor.getString(8);
                juniorsList.add(junior);
            }
            while (cursor.moveToNext());
        }
        db.close();
        return juniorsList;
    }
    public void acceptJunior(String username){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL("UPDATE juniors set status='accepted' where username='"+username+"';");
        db.close();
    }
    public void deleteAcceptedJuniors(){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL("DELETE FROM juniors where status='accepted'");
        db.close();
    }
    public void deletePendingJuniors(){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL("DELETE FROM juniors where status='pending'");
        db.close();
    }
    public void deleteJuniors(){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL("DELETE FROM juniors");
        db.close();
    }
    public void deleteSeniors(){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL("DELETE FROM seniors");
        db.close();
    }
    public void deleteRequests(){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL("DELETE FROM requests");
        db.close();
    }
    public void deleteEntrant(){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL("DELETE FROM entrants");
        db.close();
    }
    public void deleteStudent(){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL("DELETE FROM students");
        db.close();
    }
    public void logoutStudent(){
        deleteStudent();
        deleteJuniors();
    }
    public void logoutEntrant(){
        deleteEntrant();
        deleteSeniors();
        deleteRequests();
    }
    public void logoutAudience(){
        deleteStudent();
    }
}
