package img.myapplication;

import android.content.ContentValues;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.provider.BaseColumns;
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


    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        DatabaseHelper mdbHelper = new DatabaseHelper(this);
        SQLiteDatabase db = mdbHelper.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put(FeedEntry.COLUMN_NAME_NAME, String.valueOf((EditText) findViewById(R.id.new_name)));
        values.put(FeedEntry.COLUMN_NAME_PASSWORD, String.valueOf((EditText) findViewById(R.id.new_password)));
        values.put(FeedEntry.COLUMN_NAME_ENR, String.valueOf((EditText) findViewById(R.id.new_enr)));
        values.put(FeedEntry.COLUMN_NAME_EMAIL, String.valueOf((EditText) findViewById(R.id.new_email)));
        values.put(FeedEntry.COLUMN_NAME_MOBILE, String.valueOf((EditText) findViewById(R.id.new_number)));
        values.put(FeedEntry.COLUMN_NAME_BRANCH, String.valueOf((EditText) findViewById(R.id.new_branch)));
        values.put(FeedEntry.COLUMN_NAME_State, String.valueOf((EditText) findViewById(R.id.new_state)));

// Insert the new row, returning the primary key value of the new row
        long newRowId;
        newRowId = db.insert(
                FeedEntry.TABLE_NAME, null,values);
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


        public void onCreate(SQLiteDatabase db) {
            db.execSQL();
        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

        }
    }
}