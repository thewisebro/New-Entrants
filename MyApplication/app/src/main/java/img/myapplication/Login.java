package img.myapplication;

import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.provider.BaseColumns;

public class Login extends AppCompatActivity {
    private EditText Enr_No;
    private EditText Password;
    private Button button;
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
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login2);

        Enr_No=(EditText) findViewById(R.id.et_Enr_No);
        Password=(EditText) findViewById(R.id.et_Password);


    }
    public void login(View view){
        /*DatabaseHelper mdbHelper= new DatabaseHelper(this);
        SQLiteDatabase db = mdbHelper.getReadableDatabase();

        String [] projection= {
                FeedEntry.COLUMN_NAME_ENR,
                FeedEntry.COLUMN_NAME_PASSWORD
        };
        String selection=FeedEntry.COLUMN_NAME_ENR+"=? AND "+FeedEntry.COLUMN_NAME_PASSWORD+"=?";
        String [] arg={
                String.valueOf(Enr_No),
                String.valueOf(Password)
        };*/
        SQLiteDatabase db= openOrCreateDatabase(FeedEntry.DATABASE_NAME, MODE_PRIVATE, null);

        Cursor result=db.rawQuery("select * from Entrants where Enr_No='"+Enr_No.getText().toString()+"' and Password='"+Password.getText().toString()+"';",null);

        if (result.getCount()!=0){

            Intent intent= new Intent(this, Navigation.class);
            startActivity(intent);
            finish();
        }
    }
    public void register_click(View view){
        Intent intent = new Intent(this, Register.class);
        startActivity(intent);
        finish();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_login, menu);
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
