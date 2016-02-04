package img.myapplication;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;
import java.util.List;


public class MySQLiteHelper extends SQLiteOpenHelper {
    // Database Version
    private static final int DATABASE_VERSION = 1;
    // Database Name
    public static final String DATABASE_NAME = "Entrants_Data";

    private static final String TABLE_SENIORS="seniors";
    private static final String TABLE_USERS = "users";
    private static final String TABLE_BLOGS= "blogs";
    private static final String TABLE_STUDENTS="students";
    private static final String TABLE_ENTRANTS="entrants";

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
                    "year char(1),"+
                    "state varchar );";
    private static String CREATE_BLOGS_TABLE=
            "create table if not exists blogs ( "+
                    "topic varchar,"+
                    "shortinfo varchar,"+
                    "author varchar,"+
                    "date_published text,"+
                    "blogtext text );";
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
                "mobile varchar,"+
                "fb_link varchar );";

    private static String CREATE_ENTRANTS_TABLE=
            "create table if not exists entrants ( "+
                    "id text primary key,"+
                    "name text,"+
                    "username text,"+
                    "password text,"+
                    "branch text,"+
                    "town text,"+
                    "state text,"+
                    "email text,"+
                    "mobile text,"+
                    "fb_link text,"+
                    "phone_privacy int,"+
                    "profile_privacy int );";

    public static String TEMP_ENTRANT=
            "insert into entrants values ('1','singh','asd','asd','ee','roorkee','uk','a@a.a','123','singh@fb.com',1,1);";
    public static String TEMP_STUDENT=
            "insert into students values ('ankush','14115019','asd','ee','2','roorkee','uk','a@a.a','123','spunk@facebook.com');";
    public static String TEMP_BLOG=
            "insert into blogs values ('topic','short info','group','2016-02-04','content');";
    public static String TEMP_SENIOR=
            "insert into seniors values ('name','branch','2','state');";

    public MySQLiteHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);

        SQLiteDatabase db=this.getWritableDatabase();
        /*db.execSQL("DROP TABLE IF EXISTS seniors");
        db.execSQL("DROP TABLE IF EXISTS students");
        db.execSQL("DROP TABLE IF EXISTS entrants");
        db.execSQL("DROP TABLE IF EXISTS blogs");*/
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.execSQL(CREATE_ENTRANTS_TABLE);
        db.execSQL(CREATE_SENIORS_TABLE);
        db.execSQL(CREATE_BLOGS_TABLE);
        //db.execSQL(TEMP_ENTRANT);
        db.execSQL(TEMP_STUDENT);
        db.execSQL(TEMP_BLOG);
        db.execSQL(TEMP_SENIOR);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        /*db.execSQL("DROP TABLE IF EXISTS seniors");
        db.execSQL("DROP TABLE IF EXISTS students");
        db.execSQL("DROP TABLE IF EXISTS entrants");
        db.execSQL("DROP TABLE IF EXISTS blogs");
        db.execSQL(CREATE_SENIORS_TABLE);
        db.execSQL(CREATE_STUDENTS_TABLE);
        db.execSQL(CREATE_ENTRANTS_TABLE);
        db.execSQL(CREATE_BLOGS_TABLE);
        db.execSQL(TEMP_ENTRANT);
        db.execSQL(TEMP_STUDENT);
        db.execSQL(TEMP_BLOG);
        db.execSQL(TEMP_SENIOR);*/
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS seniors");
        db.execSQL("DROP TABLE IF EXISTS users");
        db.execSQL("DROP TABLE IF EXISTS students");
        db.execSQL("DROP TABLE IF EXISTS entrants");
        db.execSQL("DROP TABLE IF EXISTS blogs");
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
            //student.password= cursor.getString(2);
            student.branch= cursor.getString(3);
            student.year= cursor.getString(4);
            student.town= cursor.getString(5);
            student.state= cursor.getString(6);
            student.email= cursor.getString(7);
            student.mobile= cursor.getString(8);
            student.fb_link=cursor.getString(9);

        }
        return student;
    }
    public boolean checkStudent(String enr_no, String password){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from students where enr_no='" + enr_no + "' and password ='" + password + "';", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }
    public boolean loggedStudent(){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from students ;", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }
    public void addStudent(StudentModel student){
        SQLiteDatabase db=this.getWritableDatabase();
        deleteStudent();
        //db.execSQL(CREATE_STUDENTS_TABLE);
        ContentValues values=new ContentValues();
        values.put("name",student.name);
        //values.put("enr_no",student.enr_no);
        //values.put("password",student.branch);
        values.put("branch",student.branch);
        values.put("year",student.year);
        values.put("town",student.town);
        values.put("state",student.state);
        values.put("email",student.email);
        values.put("mobile",student.mobile);
        values.put("fb_link", student.fb_link);
        db.insert(TABLE_STUDENTS,null,values);
        db.close();
    }
    public void addEntrant(NewEntrantModel entrant){
        SQLiteDatabase db=this.getWritableDatabase();
        //db.execSQL(CREATE_ENTRANTS_TABLE);
        deleteEntrant();
        ContentValues values=new ContentValues();
        values.put("id", entrant.id);
        values.put("name", entrant.name);
        //values.put("username", entrant.username);
        //values.put("password", entrant.password);
        values.put("email", entrant.email);
        values.put("branch", entrant.branch);
        values.put("town", entrant.town);
        values.put("state", entrant.state);
        values.put("mobile", entrant.mobile);
        values.put("fb_link",entrant.fb_link);
        values.put("phone_privacy",entrant.phone_privacy);
        values.put("profile_privacy",entrant.profile_privacy);
        db.insert(TABLE_ENTRANTS, null, values);
        db.close();
    }
    public void addBlog(BlogModel blog){
        if (!checkBlog(blog)){
            SQLiteDatabase db=this.getWritableDatabase();
            //db.execSQL(CREATE_BLOGS_TABLE);

            ContentValues values=new ContentValues();
            values.put("topic", blog.topic);
            //values.put("shortinfo",blog.shortInfo);
            //values.put("author",blog.author);
            //values.put("category",blog.category);
            values.put("author",blog.group);
            values.put("date",blog.date);
            values.put("blogtext",blog.blogText);

            db.insert(TABLE_BLOGS,null,values);
            db.close();
        }
    }
    public void addSenior(SeniorModel senior){
        if (!checkSenior(senior)){
            SQLiteDatabase db=this.getWritableDatabase();
            //db.execSQL(CREATE_SENIORS_TABLE);
            ContentValues values=new ContentValues();
            values.put("name",senior.name);
            values.put("branch",senior.branch);
            values.put("year",senior.year);
            values.put("state", senior.state);
            db.insert(TABLE_SENIORS, null, values);
            db.close();
        }
    }
    public boolean checkEntrant(String username, String password){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from entrants where username='" + username + "' and password ='" + password + "';", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }
    public boolean loggedEntrant(){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from entrants ;", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }
    public boolean checkBlog(BlogModel blog){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from blogs where topic='" + blog.topic + "' and date ='" + blog.date +"';", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }
    public boolean checkSenior(SeniorModel senior){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from seniors where name='" + senior.name + "' and branch ='" + senior.branch + "' and year='"+senior.year+"';", null);

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
            //entrant.username = cursor.getString(2);
            //entrant.password = cursor.getString(3);
            entrant.branch = cursor.getString(4);
            entrant.town = cursor.getString(5);
            entrant.state = cursor.getString(6);
            //entrant.about = cursor.getString(7);
            entrant.email = cursor.getString(7);
            entrant.mobile = cursor.getString(8);
            entrant.fb_link=cursor.getString(9);
            entrant.phone_privacy=cursor.getInt(10) >0;
            entrant.profile_privacy=cursor.getInt(11) > 0;

        }
        return entrant;
    }
    public List<BlogModel> getBlogs(){
        SQLiteDatabase db=this.getReadableDatabase();
        List<BlogModel> blogs=new ArrayList<BlogModel>();
        Cursor cursor=db.rawQuery("select * from blogs;",null);
        int len=cursor.getCount();
        if (len!=0) {
            cursor.moveToFirst();
            for (int i=0;i<len;i++){
                BlogModel blog=new BlogModel();
                blog.topic=cursor.getString(0);
                //blog.shortInfo=cursor.getString(1);
                //blog.author=cursor.getString(2);
                //blog.category=cursor.getString(3);
                blog.group=cursor.getString(2);
                blog.date=cursor.getString(3);
                blog.blogText=cursor.getString(4);
                blogs.add(blog);
                cursor.moveToNext();
            }
        }
        return blogs;
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
        //values.put("username", entrant.username);
        //values.put("password", entrant.password);
        values.put("email", entrant.email);
        //values.put("branch", entrant.branch);
        values.put("town", entrant.town);
        //values.put("state", entrant.state);
        //values.put("about", entrant.about);
        values.put("mobile", entrant.mobile);

        int i=db.update(TABLE_ENTRANTS, values, " id = ? ", new String[]{entrant.id});

        return i;

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
