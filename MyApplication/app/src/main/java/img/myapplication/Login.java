package img.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;

public class Login extends AppCompatActivity {
    private EditText Enr_No;
    private EditText Password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login2);

    }
    public void login(View view){

        Enr_No=(EditText) findViewById(R.id.et_Enr_No);
        Password=(EditText) findViewById(R.id.et_Password);

       MySQLiteHelper db=new MySQLiteHelper(this);
      User_Model user=db.getUser(Enr_No.getText().toString(),Password.getText().toString());
      if(db.checkUser(Enr_No.getText().toString(), Password.getText().toString()) == true)
      {
            Intent intent =new Intent(this, Navigation.class);
            Bundle mBundle=new Bundle();
            mBundle.putSerializable("user",user);
            intent.putExtras(mBundle);
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
