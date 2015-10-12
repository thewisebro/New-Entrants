package img.myapplication;

import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;

public class Register extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

    }
    public void register(View view){

        String enr= ((EditText) findViewById(R.id.new_enr)).getText().toString();
        String name= ((EditText) findViewById(R.id.new_name)).getText().toString();
        String password= ((EditText) findViewById(R.id.new_password)).getText().toString();
        String email= ((EditText) findViewById(R.id.new_email)).getText().toString();
        String number= ((EditText) findViewById(R.id.new_number)).getText().toString();

        SQLiteDatabase db= openOrCreateDatabase("Entrants_Data", MODE_PRIVATE,null);
        db.execSQL("create table if not exists Entrants( Enr_No varchar, Name varchar, Password varchar, Email varchar, Number varchar);");
        db.execSQL("insert into Entrants values('"+enr+"','"+name+"','"+password+"','"+email+"','"+number+"');");
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

}