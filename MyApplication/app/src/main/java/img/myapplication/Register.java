package img.myapplication;

import android.content.Context;
import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Bundle;
import android.provider.BaseColumns;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

public class Register extends AppCompatActivity {

    public static abstract class FeedEntry implements BaseColumns {
        public static final String TABLE_NAME = "Entrants";
        public static final String COLUMN_NAME_NAME = "Name";
        public static final String COLUMN_NAME_EMAIL = "Email";
        public static final String COLUMN_NAME_ENR = "Enr_No";
        public static final String COLUMN_NAME_PASSWORD = "Password";
        public static final String COLUMN_NAME_MOBILE = "Mobile_No";
        public static final String COLUMN_NAME_BRANCH = "Branch";
        public static final String COLUMN_NAME_State = "State";
        public static final String DATABASE_NAME = "Entrants_Data";

    }
    public User_Model user;
    public MySQLiteHelper db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        db=new MySQLiteHelper(this);
        user=new User_Model();
        setContentView(R.layout.activity_register);

    }

    public void register(View view){
        user.Enr_No= ((EditText) findViewById(R.id.new_enr)).getText().toString().trim();
        user.Name= ((EditText) findViewById(R.id.new_name)).getText().toString().trim();
        user.Password= ((EditText) findViewById(R.id.new_password)).getText().toString().trim();
        user.Email= ((EditText) findViewById(R.id.new_email)).getText().toString().trim();
        user.Mobile= ((EditText) findViewById(R.id.new_number)).getText().toString().trim();
        if(validate()) {
            SQLiteDatabase db_ = openOrCreateDatabase(db.DATABASE_NAME, MODE_PRIVATE, null);
            db_.execSQL("create table if not exists users( enr_no varchar primary key, name varchar, password varchar, email varchar unique, mobile varchar, branch varchar, state varchar);");

            db.addUser(user);

            Intent intent = new Intent(this, Login.class);
            startActivity(intent);
            finish();
        }
    }
    public boolean validate(){

        String emailPattern = "[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+";
        String mobilePattern="\\d+";
        String enrPattern="\\d+";
        String namePattern="[a-zA-Z ]";
        boolean flag=true;
        if (!(user.Email).matches(emailPattern)){
            Toast.makeText(getApplicationContext(), "Invalid valid email address", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(user.Mobile).matches(mobilePattern)){
            Toast.makeText(getApplicationContext(),"Invalid Mobile Number", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(user.Enr_No).matches(enrPattern)){
            Toast.makeText(getApplicationContext(),"Invalid Enrollment Number", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(user.Name).matches(namePattern)){
            Toast.makeText(getApplicationContext(),"Enter a proper Name", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        return flag;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_register, menu);
        return true;
    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    public class DatabaseHelper extends SQLiteOpenHelper {

        public DatabaseHelper(Context context) {
            super(context, DATABASE_NAME, null, DATABASE_VERSION);
        }

        public static final int DATABASE_VERSION = 1;
        public static final String DATABASE_NAME = "FeedReader.db";

        @Override
        public void onCreate(SQLiteDatabase db) {
           // db.execSQL();
        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

        }
    }
}