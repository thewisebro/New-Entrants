package img.myapplication;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.widget.ListView;
import android.widget.TextView;


public class MySQLiteHelper extends SQLiteOpenHelper {// Database Version
    private static final int DATABASE_VERSION = 1;
    // Database Name
    public static final String DATABASE_NAME = "Entrants_Data";

    private static final String TABLE_USERS = "users";
    private static final String TABLE_BLOGS= "blogs";

    private static final String KEY_ENR_NO = "enr_no";
    private static final String KEY_NAME = "name";
    private static final String KEY_PASSWORD = "password";
    private static final String KEY_EMAIL = "email";
    private static final String KEY_MOBILE = "mobile";
    private static final String KEY_BRANCH = "branch";
    private static final String KEY_STATE = "state";

    public MySQLiteHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        String CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users ( " +
                " enr_no text primary key,"+
                "name text,"+
                "password text,"+
                "email text ,"+
                "mobile text ,"+
                "branch text,"+
                "state text );" ;

        SQLiteDatabase db=this.getWritableDatabase();
        db.execSQL(CREATE_USERS_TABLE);

    }

    @Override
    public void onCreate(SQLiteDatabase db) {

        String CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users ( " +
                " enr_no text primary key,"+
                "name text,"+
                "password text,"+
                "email text ,"+
                "mobile text ,"+
                "branch text,"+
                "state text );" ;


        db.execSQL(CREATE_USERS_TABLE);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

        db.execSQL("DROP TABLE IF EXISTS users");

        this.onCreate(db);
    }
  /*  public void createTable(){
        SQLiteDatabase db= SQLiteDatabase.openOrCreateDatabase(DATABASE_NAME,null,null);
        db.execSQL("create table if not exists users( enr_no varchar primary key, name varchar, password varchar, email varchar unique, mobile varchar, branch varchar, state varchar);");
    }*/
    public void addUser(User_Model user){
        SQLiteDatabase db=this.getWritableDatabase();
        String CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users ( " +
                " enr_no text primary key,"+
                "name text,"+
                "password text,"+
                "email text ,"+
                "mobile text ,"+
                "branch text,"+
                "state text );" ;


        db.execSQL(CREATE_USERS_TABLE);

        ContentValues values=new ContentValues();
        values.put(KEY_ENR_NO, user.Enr_No);
        values.put(KEY_NAME, user.Name);
        values.put(KEY_PASSWORD, user.Password);
        values.put(KEY_EMAIL, user.Email);
        values.put(KEY_MOBILE, user.Mobile);
       // values.put(KEY_BRANCH, user.Branch);
    //    values.put(KEY_STATE, user.State);

        db.insert(TABLE_USERS, null, values);

        db.close();
    }
    public boolean checkUser(String enr_no, String password){
        SQLiteDatabase db= this.getReadableDatabase();
        Cursor cursor=db.rawQuery("select * from users where enr_no='" + enr_no + "' and password ='" + password + "';", null);

        if(cursor.getCount()==0) return false;
        else return true;
    }
    public User_Model getUser(String enr_no, String password){
        SQLiteDatabase db= this.getReadableDatabase();
        User_Model user=new User_Model();

        //Cursor cursor= db.query(TABLE_USERS, COLUMNS, " enr_no = ? and password = ? ", new String[]{enr_no, password}, null, null, null, null);
        Cursor cursor=db.rawQuery("select * from users where enr_no='" + enr_no + "' and password ='" + password + "';", null);
        if (cursor.getCount()!=0) {
            cursor.moveToFirst();

            user.Enr_No = cursor.getString(0);
           user.Name = cursor.getString(1);
            user.Password = cursor.getString(2);
            user.Email = cursor.getString(3);
            user.Mobile = cursor.getString(4);
        //    user.Branch = cursor.getString(5);
        //    user.State = cursor.getString(6);


        }
        return user;


    }

    public int updateUser(User_Model user){
        SQLiteDatabase db=this.getWritableDatabase();

        ContentValues values= new ContentValues();
        values.put(KEY_ENR_NO, user.Enr_No);
        values.put(KEY_NAME, user.Name);
        values.put(KEY_PASSWORD, user.Password);
        values.put(KEY_EMAIL, user.Email);
        values.put(KEY_MOBILE, user.Mobile);
        //values.put(KEY_BRANCH, user.Branch);
       // values.put(KEY_STATE, user.State);
        int i=db.update(TABLE_USERS, values, " enr_no = ? ", new String[]{user.Enr_No});

        return i;

    }
    public void deleteUser(User_Model user){
        SQLiteDatabase db= this.getWritableDatabase();
        db.delete(TABLE_USERS, " enr_no = ? ", new String[]{ user.Enr_No});
        db.close();
    }

    public void displayBlog(){

    }
    public void displayPeers(){
        ListView peers_state= (ListView) findViewById(R.id.peers_state);
        for(int i=0; i<3; i++){
            TextView peer=new TextView(getContext());
        }


    }
    public void sortPeers(){

    }
    public void displaySeniors(){

    }
    public void sortSeniors(){

    }
}
