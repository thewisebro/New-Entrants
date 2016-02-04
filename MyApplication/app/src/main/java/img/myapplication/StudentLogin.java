package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class StudentLogin extends AppCompatActivity {
    private EditText Enr_No;
    private EditText Password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_login);
        if(!isConnected()){
            Toast.makeText(getApplicationContext(), "NOT CONNECTED", Toast.LENGTH_SHORT).show();
        }
    }
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }
    public void login(View view){

        Enr_No=(EditText) findViewById(R.id.et_Enr_No);
        Password=(EditText) findViewById(R.id.et_Password);

        MySQLiteHelper db=new MySQLiteHelper(this);
        /*
        StudentModel user=db.getStudent(Enr_No.getText().toString(),Password.getText().toString());
        if(db.checkEntrant(Enr_No.getText().toString(), Password.getText().toString()))
        {
            Intent intent =new Intent(this, NavigationStudent.class);
            Bundle mBundle=new Bundle();
            mBundle.putSerializable("user",user);
            intent.putExtras(mBundle);
            startActivity(intent);
            finish();
        }
        else Toast.makeText(getApplicationContext(), "Wrong Username or Password", Toast.LENGTH_SHORT).show();
        */
        JSONObject userobj=new JSONObject();
        try {
            userobj.put("Enr_No",Enr_No.getText().toString());
            userobj.put("Password",Password.getText().toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
        StudentModel student=POST("",userobj);
        if (student.valid){
            db.addStudent(student);
            Intent intent=new Intent(this, NavigationStudent.class);
            startActivity(intent);
            finish();
        }
        else Toast.makeText(getApplicationContext(), "Wrong Username or Password", Toast.LENGTH_SHORT).show();
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

    private static StudentModel POST(String url,JSONObject userobj){
        String result="";
        StudentModel model=new StudentModel();
        try{

            URL urlobj=new URL(url);
            HttpURLConnection conn=(HttpURLConnection) urlobj.openConnection();
            conn.setDoInput(true);
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");
            //conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            OutputStreamWriter wr=new OutputStreamWriter(conn.getOutputStream());
            wr.write(userobj.toString());
            wr.flush();

            BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
            String line = "";
            while((line = bufferedReader.readLine()) != null)
                result += line;
            bufferedReader.close();
            JSONObject object=new JSONObject(result);
            if (result !=null){
                model.name=object.getString("name");
                model.enr_no=object.getString("enr_no");
                //model.password=object.getString("password");
                model.town=object.getString("town");
                model.branch=object.getString("branch");
                model.email=object.getString("email");
                model.mobile=object.getString("mobile");
                model.state=object.getString("state");
                model.year=object.getString("year");
                model.fb_link=object.getString("fb_link");
                model.valid=true;
            }
            else model.valid=false;
            return model;

        } catch (Exception e) {
            Log.d("InputStream", e.getLocalizedMessage());
        }

        return model;
    }

}
