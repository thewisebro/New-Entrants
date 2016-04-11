package img.myapplication;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.CookiePolicy;
import java.net.CookieStore;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import models.NewEntrantModel;

public class Register extends AppCompatActivity {

    public NewEntrantModel entrant;
    public MySQLiteHelper db;
    public CookieManager cookieManager;
    public Map<String,String > params;
    public String csrftoken;
    private String registerURL="http://192.168.121.187:8080/new_entrants/register/";
    private String appURL="http://192.168.121.187:8080/new_entrants/";
    private EditText name;
    private EditText username;
    private EditText password;
    private EditText re_password;
    private EditText town;
    private EditText email;
    private EditText mobile;
    private EditText fblink;
    private CheckBox phone_privacy;
    private Spinner state;
    private Spinner branch;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        ActionBar bar=getSupportActionBar();
        bar.setHomeButtonEnabled(true);
        bar.setDisplayHomeAsUpEnabled(true);
        db=new MySQLiteHelper(this);
        entrant=new NewEntrantModel();
        setContentView(R.layout.activity_register);
        setViews();
    }

    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }
    private void setViews(){
        name=(EditText) findViewById(R.id.new_name);
        username= (EditText) findViewById(R.id.new_username);
        password= (EditText) findViewById(R.id.new_password);
        re_password=(EditText) findViewById(R.id.re_password);
        town=(EditText) findViewById(R.id.new_town);
        email=(EditText) findViewById(R.id.new_email);
        mobile=(EditText) findViewById(R.id.new_mobile);
        fblink=(EditText) findViewById(R.id.new_fblink);
        phone_privacy= (CheckBox) findViewById(R.id.contact_visibility);
        state= (Spinner) findViewById(R.id.new_state);
        branch= (Spinner) findViewById(R.id.new_branch);
    }

    public void register(View view) throws IllegalAccessException {
        if (isConnected()){
            entrant.name= name.getText().toString().trim();
            entrant.username= username.getText().toString().trim();
            entrant.password= password.getText().toString().trim();
            entrant.town= town.getText().toString().trim();
            entrant.email= email.getText().toString().trim();
            entrant.mobile= mobile.getText().toString().trim();
            entrant.fb_link= fblink.getText().toString().trim();
            entrant.branchname=branch.getSelectedItem().toString().trim();
            entrant.branchcode=(getResources().getStringArray(R.array.branch_codes))[branch.getSelectedItemPosition()];
            entrant.state= state.getSelectedItem().toString().trim();
            entrant.statecode=(getResources().getStringArray(R.array.state_codes))[state.getSelectedItemPosition()];
            entrant.phone_privacy= phone_privacy.isChecked();
            if(validate())
                new RegisterTask().execute();
        }

    }
    public boolean validate(){

        //String emailPattern = "[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+";
        String emailPattern="^(([^<>()\\[\\]\\\\.,;:\\s@\"]+(\\.[^<>()\\[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$";
        //String mobilePattern="^(\\+91|0|)[0-9]{10}$";
        String mobilePattern="^$|^(\\+\\d{1,3}[- ]?)?\\d{10}$";
        //String namePattern="[a-zA-Z ]+";
        String namePattern="^[a-zA-Z ]{1,100}$";
        String usernamePattern="^[0-9a-zA-Z]{1,30}$";
        String townPattern="^$|^[a-zA-Z ]+$";
        String fbPattern="^$|^(([^<>()\\[\\]\\\\.,;:\\s@\"]+(\\.[^<>()\\[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$";
        //String fbPattern="^$|^[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+$";
        boolean flag=true;

        if(!(entrant.password).equals(re_password.getText().toString())){
            re_password.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getApplicationContext(),"Passwords do not match", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            re_password.setBackgroundDrawable(null);
        if (!(entrant.email).matches(emailPattern)){
            email.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getApplicationContext(), "Invalid email address", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            email.setBackgroundDrawable(null);
        if (!(entrant.username).matches(usernamePattern)){
            username.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getApplicationContext(), "Invalid username", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            username.setBackgroundDrawable(null);
        if(!(entrant.mobile).matches(mobilePattern)){
            mobile.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getApplicationContext(),"Invalid Mobile Number", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            mobile.setBackgroundDrawable(null);
        if(!(entrant.name).matches(namePattern)){
            name.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getApplicationContext(),"Enter a proper Name", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            name.setBackgroundDrawable(null);
        if(!(entrant.town).matches(townPattern)){
            town.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getApplicationContext(),"Enter a proper City name", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            town.setBackgroundDrawable(null);
        if (!(entrant.fb_link).matches(fbPattern)){
            fblink.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getApplicationContext(), "Invalid Facebook link", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            fblink.setBackgroundDrawable(null);
        if (state.getSelectedItemPosition()==0){
            state.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getApplicationContext(), "Select a State", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            state.setBackgroundDrawable(null);
        return flag;
    }
    private void setParams() throws IllegalAccessException {
        params=new HashMap<String,String>();
        params.put("csrfmiddlewaretoken",csrftoken);
        params.put("name",entrant.name);
        params.put("username",entrant.username);
        params.put("password1",entrant.password);
        params.put("password2",entrant.password);
        params.put("branch",entrant.branchcode);
        params.put("email",entrant.email);
        params.put("fb_link",entrant.fb_link);
        params.put("state",entrant.statecode);
        params.put("hometown",entrant.town);
        params.put("phone_no",entrant.mobile);
        if (entrant.phone_privacy)
            params.put("phone_privacy","on");

        params.put("droid","True");

    }
    private String registerNow(){
        String result=null;
        HttpURLConnection urlConnectionPost=null;
        cookieManager = new CookieManager(null, CookiePolicy.ACCEPT_ALL);
        CookieHandler.setDefault(cookieManager);
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {
            cookieStore.removeAll();
            HttpURLConnection conn= (HttpURLConnection) new URL(registerURL).openConnection();
            conn.setRequestMethod("GET");
            conn.setReadTimeout(5000);
            if (conn.getResponseCode()== HttpURLConnection.HTTP_OK) {
                Object obj = conn.getContent();
            }

            csrftoken=cookieStore.getCookies().get(0).getValue().toString();

            urlConnectionPost= (HttpURLConnection) new URL(registerURL).openConnection();
            urlConnectionPost.setDoOutput(true);
            urlConnectionPost.setDoInput(true);
            urlConnectionPost.setRequestMethod("POST");
            urlConnectionPost.setRequestProperty("Cookie", TextUtils.join(";", cookieStore.getCookies()));
            cookieStore.removeAll();

            urlConnectionPost.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            urlConnectionPost.setRequestProperty("Accept","application/json");
            urlConnectionPost.setInstanceFollowRedirects(true);
            setParams();
            Uri.Builder builder = new Uri.Builder();
            for (Map.Entry<String, String> entry : params.entrySet()){
                builder.appendQueryParameter(entry.getKey(),entry.getValue());
            }
            String query = builder.build().getEncodedQuery();
            urlConnectionPost.setUseCaches(false);

            OutputStream os = urlConnectionPost.getOutputStream();
            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(os, "UTF-8"));
            writer.write(query);
            writer.flush();
            writer.close();
            os.close();

            BufferedReader reader= new BufferedReader(new InputStreamReader(urlConnectionPost.getInputStream()));
            StringBuffer buffer=new StringBuffer();
            String inputLine;
            while ((inputLine = reader.readLine()) != null)
                buffer.append(inputLine+"\n");
            result=getResult(buffer.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }
    public String getResult(String result){
        String status=null;
        try {
            JSONObject rObj=new JSONObject(result);
            status=rObj.get("status").toString();
            if (status.equals("fails"))
                status=rObj.getString("error");

        } catch (JSONException e) {
            e.printStackTrace();
        }


        return status;
    }
    private class RegisterTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            try {
                return registerNow();
            } catch (Exception e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")){
                Toast.makeText(getApplicationContext(),"Registration Successful!", Toast.LENGTH_SHORT).show();
                finish();
            }
            else {
                if (result==null)
                    Toast.makeText(getApplicationContext(),"Registration Failed!", Toast.LENGTH_SHORT).show();
                else
                    Toast.makeText(getApplicationContext(),result, Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_register, menu);
        return true;
    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id==android.R.id.home) {
            finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }


}