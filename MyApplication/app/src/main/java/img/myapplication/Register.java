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
        user.Enr_No= ((EditText) findViewById(R.id.new_enr)).getText().toString();
        user.Name= ((EditText) findViewById(R.id.new_name)).getText().toString();
        user.Password= ((EditText) findViewById(R.id.new_password)).getText().toString();
        user.Email= ((EditText) findViewById(R.id.new_email)).getText().toString();
        user.Mobile= ((EditText) findViewById(R.id.new_number)).getText().toString();
        SQLiteDatabase db_= openOrCreateDatabase(db.DATABASE_NAME, MODE_PRIVATE,null);
        db_.execSQL("create table if not exists users( enr_no varchar primary key, name varchar, password varchar, email varchar unique, mobile varchar, branch varchar, state varchar);");

        db.addUser(user);

        Intent intent=new Intent(this, Login.class);
        startActivity(intent);
        finish();
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