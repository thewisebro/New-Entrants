package img.myapplication;

import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class Login extends AppCompatActivity {
    private EditText Enr_No;
    private EditText Password;
    private Button button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login2);

        Enr_No=(EditText) findViewById(R.id.et_Enr_No);
        Password=(EditText) findViewById(R.id.et_Password);


    }
    public void login(View view){

        SQLiteDatabase db= openOrCreateDatabase("Entrants_Data", MODE_PRIVATE, null);

        Cursor result=db.rawQuery("select * from Entrants where Enr_No='"+Enr_No.getText().toString()+"' and Password='"+Password.getText().toString()+"';",null);

        if (result.moveToFirst()){

            Intent intent= new Intent(this, Navigation.class);
            intent.putExtra("EXTRA_ENR", Enr_No.getText().toString());
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


}
