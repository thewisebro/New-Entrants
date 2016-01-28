package img.myapplication;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;
import java.util.List;


public class MySQLiteHelper extends SQLiteOpenHelper {// Database Version
    private static final int DATABASE_VERSION = 1;
    // Database Name
    public static final String DATABASE_NAME = "Entrants_Data";

    private static final String TABLE_SENIORS="seniors";
    private static final String TABLE_USERS = "users";
    private static final String TABLE_BLOGS= "blogs";
    private static final String TABLE_STUDENTS="students";
    private static final String TABLE_ENTRANTS="entrants";

    private static final String KEY_AUTHOR = "author";
    private static final String KEY_TOPIC = "topic";
    private static final String KEY_TAG = "tag";
    private static final String KEY_TEXT = "text";
    private static final String KEY_DATE="date";

    private static final String KEY_ENR_NO = "enr_no";
    private static final String KEY_NAME = "name";
    private static final String KEY_PASSWORD = "password";
    private static final String KEY_EMAIL = "email";
    private static final String KEY_MOBILE = "mobile";
    private static final String KEY_BRANCH = "branch";
    private static final String KEY_STATE = "state";

    private static String CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users ( " +
            " enr_no text primary key,"+
            "name text,"+
            "password text,"+
            "email text ,"+
            "mobile text ,"+
            "branch text,"+
            "state text );" ;
    private static String CREATE_SENIORS_TABLE=
            "create table if not exists seniors ( "+
                    "name varchar," +
                    "branch varchar,"+
                    "year varchar"+
                    "state varchar );";
    private static String CREATE_STUDENTS_TABLE=
            "create table if not exists students ( "+
                "name varchar,"+
                "enr_no char(8) primary key,"+
                "password varchar,"+
                "branch varchar,"+
                "year char(1),"+
                "town varchar,"+
                "state varchar,"+
                "email varchar,"+
                "mobile varchar );";

    private static String CREATE_ENTRANTS_TABLE=
            "create table if not exists entrants ( "+
                    "id text primary key,"+
                    "name text,"+
                    "username text,"+
                    "password text,"+
                    "branch text,"+
                    "town text,"+
                    "state text,"+
                    "about text,"+
                    "email text,"+
                    "mobile text );";


    public MySQLiteHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);

        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL(CREATE_USERS_TABLE);
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.execSQL(CREATE_ENTRANTS_TABLE);
        db.execSQL(CREATE_SENIORS_TABLE);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(CREATE_SENIORS_TABLE);
        db.execSQL(CREATE_USERS_TABLE);
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.execSQL(CREATE_ENTRANTS_TABLE);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS seniors");
        db.execSQL("DROP TABLE IF EXISTS users");
        db.execSQL("DROP TABLE IF EXISTS students");
        db.execSQL("DROP TABLE IF EXISTS entrants");

        this.onCreate(db);
    }

    public StudentModel getStudent(String enr_no, String password){
        SQLiteDatabase db= this.getReadableDatabase();
        StudentModel student=new StudentModel();

        Cursor cursor=db.rawQuery("select * from students where enr_no='" + enr_no + "' and password ='" + password + "';", null);
        if (cursor.getCount()!=0) {
            cursor.moveToFirst();

            student.enr_no= cursor.getString(1);
            student.name= cursor.getString(0);
            student.password= cursor.getString(2);
            //student.branch= cursor.getString(3);
            student.year= cursor.getString(4);
            student.town= cursor.getString(5);
            //student.state= cursor.getString(6);
            student.email= cursor.getString(7);
            student.mobile= cursor.getString(8);


        }
        return student;

    }
    public boolean checkStudent(String enr_no, String password){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from students where enr_no='" + enr_no + "' and password ='" + password + "';", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }

    public void addEntrant(NewEntrantModel entrant){
        SQLiteDatabase db=this.getWritableDatabase();

        db.execSQL(CREATE_ENTRANTS_TABLE);


        ContentValues values=new ContentValues();
        values.put("id", entrant.id);
        values.put("name", entrant.name);
        values.put("username", entrant.username);
        values.put("password", entrant.password);
        values.put("email", entrant.email);
        //values.put("branch", entrant.branch);
        values.put("town", entrant.town);
        //.put("state", entrant.state);
        //values.put("about", entrant.about);
        values.put("mobile", entrant.mobile);
        db.insert(TABLE_ENTRANTS, null, values);

        db.close();
    }
    public void addSenior(SeniorModel senior){
        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL(CREATE_SENIORS_TABLE);
        ContentValues values=new ContentValues();
        values.put("name",senior.name);
        values.put("branch",senior.branch);
        values.put("year",senior.year);
        values.put("state", senior.state);
        db.insert(TABLE_SENIORS,null,values);
        db.close();
    }
    public boolean checkEntrant(String username, String password){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from entrants where username='" + username + "' and password ='" + password + "';", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }
    public boolean checkSenior(SeniorModel senior){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from seniors where name='" + senior.name + "' and branch ='" + senior.branch + "' and year='"+senior.year+"';", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }
    public NewEntrantModel getEntrant(String username, String password){
        SQLiteDatabase db= this.getReadableDatabase();
        NewEntrantModel entrant=new NewEntrantModel();

        Cursor cursor=db.rawQuery("select * from entrants where username='" + username + "' and password ='" + password + "';", null);
        if (cursor.getCount()!=0) {
            cursor.moveToFirst();

            entrant.id = cursor.getString(0);
            entrant.name = cursor.getString(1);
            entrant.username = cursor.getString(2);
            entrant.password = cursor.getString(3);
            //entrant.branch = cursor.getString(4);
            entrant.town = cursor.getString(5);
            //entrant.state = cursor.getString(6);
            //entrant.about = cursor.getString(7);
            entrant.email = cursor.getString(8);
            entrant.mobile = cursor.getString(9);
        }
        return entrant;
    }
    public List<SeniorModel> getSeniors(){
        SQLiteDatabase db=this.getReadableDatabase();
        List<SeniorModel> seniors=new ArrayList<SeniorModel>();
        Cursor cursor=db.rawQuery("select * from seniors;",null);
        int len=cursor.getCount();
        if (len!=0) {
            cursor.moveToFirst();
            for (int i=0;i<len;i++){
                SeniorModel senior=new SeniorModel();
                senior.name=cursor.getString(0);
                senior.branch=cursor.getString(1);
                senior.year=cursor.getString(2);
                senior.state=cursor.getString(3);
                seniors.add(senior);
                cursor.moveToNext();
            }
        }
        return seniors;
    }
    public int updateEntrant(NewEntrantModel entrant){
        SQLiteDatabase db=this.getWritableDatabase();

        ContentValues values= new ContentValues();

        values.put("id", entrant.id);
        values.put("name", entrant.name);
        values.put("username", entrant.username);
        values.put("password", entrant.password);
        values.put("email", entrant.email);
        //values.put("branch", entrant.branch);
        values.put("town", entrant.town);
        //values.put("state", entrant.state);
        //values.put("about", entrant.about);
        values.put("mobile", entrant.mobile);

        int i=db.update(TABLE_ENTRANTS, values, " id = ? ", new String[]{entrant.id});

        return i;

    }
}
