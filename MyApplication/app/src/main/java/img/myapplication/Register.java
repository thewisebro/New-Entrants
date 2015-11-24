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
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

public class Register extends AppCompatActivity {

    public NewEntrantModel entrant;
    public MySQLiteHelper db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        db=new MySQLiteHelper(this);
        entrant=new NewEntrantModel();
        setContentView(R.layout.activity_register);

        Spinner state= (Spinner) findViewById(R.id.new_state);
        ArrayAdapter<CharSequence> stateList=ArrayAdapter.createFromResource(this,R.array.states,android.R.layout.simple_spinner_item);
        stateList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        state.setAdapter(stateList);
        Spinner branch= (Spinner) findViewById(R.id.new_branch);
        ArrayAdapter<CharSequence> branchList=ArrayAdapter.createFromResource(this,R.array.branches,android.R.layout.simple_spinner_item);
        branchList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        branch.setAdapter(branchList);


    }

    public void register(View view){
        entrant.id= ((EditText) findViewById(R.id.new_id)).getText().toString().trim();
        entrant.name= ((EditText) findViewById(R.id.new_name)).getText().toString().trim();
        entrant.username= ((EditText) findViewById(R.id.new_username)).getText().toString().trim();
        entrant.password= ((EditText) findViewById(R.id.new_password)).getText().toString().trim();
        entrant.town= ((EditText) findViewById(R.id.new_town)).getText().toString().trim();
        entrant.email= ((EditText) findViewById(R.id.new_email)).getText().toString().trim();
        entrant.mobile= ((EditText) findViewById(R.id.new_mobile)).getText().toString().trim();

        if(validate()) {
            //SQLiteDatabase db_ = openOrCreateDatabase(db.DATABASE_NAME, MODE_PRIVATE, null);
            //db_.execSQL("create table if not exists users( enr_no varchar primary key, name varchar, password varchar, email varchar unique, mobile varchar, branch varchar, state varchar);");

            db.addEntrant(entrant);

            Intent intent = new Intent(this, NewEntrantLogin.class);
            startActivity(intent);
            finish();
        }
    }
    public boolean validate(){

        String emailPattern = "[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+";
        String mobilePattern="\\d+";
        String idPattern="\\d+";
        String namePattern="[a-zA-Z ]+";
        boolean flag=true;
        if (!(entrant.email).matches(emailPattern)){
            Toast.makeText(getApplicationContext(), "Invalid valid email address", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(entrant.mobile).matches(mobilePattern)){
            Toast.makeText(getApplicationContext(),"Invalid Mobile Number", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(entrant.id).matches(idPattern)){
            Toast.makeText(getApplicationContext(),"Invalid ID", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(entrant.name).matches(namePattern)){
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


}