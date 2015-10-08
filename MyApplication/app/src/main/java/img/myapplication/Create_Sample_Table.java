package img.myapplication;

import android.content.Context;
import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.provider.BaseColumns;

public class Create_Sample_Table extends AppCompatActivity {
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
       // FeedReaderDbHelper mDbHelper = new FeedReaderDbHelper(this);
        SQLiteDatabase db= openOrCreateDatabase("Entrants_Data",MODE_PRIVATE,null);

        Intent intent= new Intent(this, Login.class);
        startActivity(intent);
        finish();
    }
    public class FeedReaderDbHelper extends SQLiteOpenHelper {
        // If you change the database schema, you must increment the database version.
        public static final int DATABASE_VERSION = 1;
        public static final String DATABASE_NAME = "FeedReader.db";

        public FeedReaderDbHelper(Context context) {
            super(context, DATABASE_NAME, null, DATABASE_VERSION);
        }
        public void onCreate(SQLiteDatabase db) {
            db.execSQL("CREATE TABLE Entrants ( Enr_No varchar(10) primary key, Name varchar(25), Email varchar(30), Password varchar(20), Mobile_No varchar(10), Branch varchar(15), State varchar(15) );");
        }
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

        }
        public void onDowngrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            onUpgrade(db, oldVersion, newVersion);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_create__sample__table, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
