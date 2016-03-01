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

import models.NewEntrantModel;

public class NewEntrantLogin extends AppCompatActivity {
    private EditText Username;
    private EditText Password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new_entrant_login);
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

        Username=(EditText) findViewById(R.id.et_username);
        Password=(EditText) findViewById(R.id.et_Password);

        MySQLiteHelper db=new MySQLiteHelper(this);
        /*
        NewEntrantModel entrant=db.getEntrant(Username.getText().toString(),Password.getText().toString());
        if(db.checkEntrant(Username.getText().toString(), Password.getText().toString()) == true)
        {
            Intent intent =new Intent(this, Navigation.class);
            Bundle mBundle=new Bundle();
            mBundle.putSerializable("entrant",entrant);
            intent.putExtras(mBundle);
            startActivity(intent);
            finish();
        }
        else Toast.makeText(getApplicationContext(), "Wrong Username or Password", Toast.LENGTH_SHORT).show();
        */
        JSONObject userobj=new JSONObject();
        try {
            userobj.put("Username",Username.getText().toString());

            userobj.put("Password",Password.getText().toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
        NewEntrantModel entrant=POST("",userobj);
        if (entrant.valid){
            db.addEntrant(entrant);
            Intent intent=new Intent(this, Navigation.class);
            startActivity(intent);
            finish();
        }
        else Toast.makeText(getApplicationContext(), "Wrong Username or Password", Toast.LENGTH_SHORT).show();
    }
    /*
    public void register(View view){
        Intent intent = new Intent(this, Register.class);
        startActivity(intent);
    }
    */
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

    private static NewEntrantModel POST(String url,JSONObject userobj){
        String result="";
        NewEntrantModel model=new NewEntrantModel();
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
            StringBuilder sb=new StringBuilder();
            String line = "";
            while((line = bufferedReader.readLine()) != null)
                sb.append(line + '\n');
            result=sb.toString();
            bufferedReader.close();
            JSONObject object=new JSONObject(result);
            if (result !=null){
                model.name=object.getString("name");
                model.id=object.getString("id");
                model.town=object.getString("town");
                model.branch=object.getString("branch");
                model.email=object.getString("email");
                model.mobile=object.getString("mobile");
                model.state=object.getString("state");
                //model.username=object.getString("username");
                //model.password=object.getString("password");
                model.fb_link=object.getString("fb_link");
                model.phone_privacy=object.getInt("phone_privacy") > 0;
                model.profile_privacy=object.getInt("profile_privacy") > 0;
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
