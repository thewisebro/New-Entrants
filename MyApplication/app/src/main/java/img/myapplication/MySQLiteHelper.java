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
import models.StudentModel;


public class MySQLiteHelper extends SQLiteOpenHelper {
    // Database Version
    private static final int DATABASE_VERSION = 1;
    // Database Name
    public static final String DATABASE_NAME = "Entrants_Data";

    private static final String TABLE_SENIORS="seniors";
    private static final String TABLE_USERS = "users";
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
                    "dp_link varchar);";
    private static String CREATE_JUNIORS_TABLE=
            "create table if not exists juniors ( "+
                    "name varchar,"+
                    "username varchar unique,"+
                    "branch varchar,"+
                    "state varchar,"+
                    "town varchar,"+
                    "email varchar,"+
                    "mobile varchar,"+
                    "fblink varchar,"+
                    "description varchar,"+
                    "status varchar);";

    private static String CREATE_STUDENTS_TABLE=
            "create table if not exists students ( "+
                "name varchar,"+
                "enr_no char(8) primary key,"+
                "username varchar,"+
                "password varchar,"+
                "branchname varchar,"+"branchcode varchar,"+
                "year char(1),"+
                "town varchar,"+
                "state varchar,"+"statecode varchar,"+
                "email varchar,"+
                "mobile varchar,"+
                "fb_link varchar,"+"sess_id varchar,"+"img blob );";

    private static String CREATE_ENTRANTS_TABLE=
            "create table if not exists entrants ( "+
                    "id text primary key,"+
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
                    "profile_privacy int(1),"+"sess_id varchar,"+"img blob );";

    public static String TEMP_ENTRANT=
            "insert into entrants values ('1','singh','asd','asd','ee','EE','roorkee','uk','UK','a@a.a','123','singh@fb.com',1,1,'asdasd',NULL);";
    public static String TEMP_STUDENT=
            "insert into students values ('ankush','14115019','14115019','asd','ee','2','roorkee','uk','a@a.a','123','spunk@facebook.com');";
    public static String TEMP_BLOG=
            "insert into blogs values ('topic','short info','group','2016-02-04','content');";
    public static String TEMP_SENIOR=
            "insert into seniors values ('name','branch','2','state');";
    public static String TEMP_JUNIOR=
            "insert into juniors values ('asd','asd','ee','delhi','gurgaon','asd@asd.com','1231231231','fb.com/spunk','smart','pending');";
    public MySQLiteHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);

        SQLiteDatabase db=this.getWritableDatabase();
        //db.execSQL("DROP TABLE IF EXISTS seniors");
        //db.execSQL("DROP TABLE IF EXISTS students");
        //db.execSQL("DROP TABLE IF EXISTS entrants");
        //db.execSQL("drop table if exists juniors");
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.execSQL(CREATE_ENTRANTS_TABLE);
        //db.execSQL(TEMP_ENTRANT);
        //db.execSQL(CREATE_SENIORS_TABLE);
        db.execSQL(CREATE_JUNIORS_TABLE);
        //db.execSQL(TEMP_JUNIOR);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS juniors");
        db.execSQL("DROP TABLE IF EXISTS students");
        db.execSQL("DROP TABLE IF EXISTS entrants");
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
        }
        return student;
    }
    public boolean loggedStudent(){
        SQLiteDatabase db= this.getWritableDatabase();
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.close();
        db=this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from students ;", null);

        if(cursor.getCount()==0) return false;
        else return true;
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
/*    public void addSenior(SeniorModel senior){
            SQLiteDatabase db=this.getWritableDatabase();
            ContentValues values=new ContentValues();
            values.put("name",senior.name);
            values.put("branchname",senior.branch);
            values.put("branchcode",senior.branchcode);
            values.put("state", senior.state);
            values.put("hometown",senior.hometown);
            values.put("mobile",senior.mobile);
            values.put("email",senior.email);
            values.put("fb_link",senior.fb_link);
            db.insert(TABLE_SENIORS, null, values);
            db.close();
    }*/
    public boolean loggedEntrant(){
        SQLiteDatabase db= this.getWritableDatabase();
        db.execSQL(CREATE_ENTRANTS_TABLE);
        db.close();
        db=this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from entrants ;", null);

        if(cursor.getCount()==0) return false;
        else return true;
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
        return entrant;
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
        return juniorsList;
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

}
