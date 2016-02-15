package img.myapplication;

import android.content.pm.ActivityInfo;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
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
    public Spinner state;
    public Spinner branch;
    public int pos_state;
    public int pos_branch;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        db=new MySQLiteHelper(this);
        entrant=new NewEntrantModel();
        setContentView(R.layout.activity_register);

        state= (Spinner) findViewById(R.id.new_state);
        ArrayAdapter<CharSequence> stateList=ArrayAdapter.createFromResource(this,R.array.states,android.R.layout.simple_spinner_item);
        stateList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        state.setAdapter(stateList);

        branch= (Spinner) findViewById(R.id.new_branch);
        ArrayAdapter<CharSequence> branchList=ArrayAdapter.createFromResource(this,R.array.branches,android.R.layout.simple_spinner_item);
        branchList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        branch.setAdapter(branchList);

    }

    public void register(View view) throws IllegalAccessException {
        pos_branch=branch.getSelectedItemPosition();
        pos_state=state.getSelectedItemPosition();
        entrant.name= ((EditText) findViewById(R.id.new_name)).getText().toString().trim();
        entrant.username= ((EditText) findViewById(R.id.new_username)).getText().toString().trim();
        entrant.password= ((EditText) findViewById(R.id.new_password)).getText().toString().trim();
        entrant.town= ((EditText) findViewById(R.id.new_town)).getText().toString().trim();
        entrant.email= ((EditText) findViewById(R.id.new_email)).getText().toString().trim();
        entrant.mobile= ((EditText) findViewById(R.id.new_mobile)).getText().toString().trim();
        entrant.fb_link= ((EditText) findViewById(R.id.new_fblink)).getText().toString().trim();
        entrant.branch=branch.getSelectedItem().toString().trim();
        entrant.state= state.getSelectedItem().toString().trim();
        entrant.phone_privacy= ((CheckBox) findViewById(R.id.contact_visibilty)).isChecked();
        entrant.profile_privacy= ((CheckBox) findViewById(R.id.profile_visibilty)).isChecked();
        if(validate()) {
            //setParams();
            new RegisterTask().execute();
        }
        else {
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
        if(!(entrant.name).matches(namePattern)){
            Toast.makeText(getApplicationContext(),"Enter a proper Name", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(entrant.password).equals(((EditText)findViewById(R.id.re_password)).getText().toString())){
            Toast.makeText(getApplicationContext(),"Passwords do not match", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        return flag;
    }
    private void setParams() throws IllegalAccessException {
        params=new HashMap<String,String>();
        //String[] state_codes=getResources().getStringArray(R.array.state_codes);
        //String[] branch_codes=getResources().getStringArray(R.array.branch_codes);
        params.put("csrfmiddlewaretoken",csrftoken);
        params.put("name",entrant.name);
        params.put("username",entrant.username);
        params.put("password1",entrant.password);
        params.put("password2",entrant.password);
        //params.put("branch",(getResources().getStringArray(R.array.branch_codes))[pos_branch]);
        params.put("branch","EE");
        params.put("email",entrant.email);
        params.put("fb_link",entrant.fb_link);
        params.put("state",(getResources().getStringArray(R.array.state_codes))[pos_state]);
        params.put("hometown",entrant.town);
        params.put("phone_no",entrant.mobile);
        if (entrant.phone_privacy)
            params.put("phone_privacy","on");

        if (entrant.profile_privacy)
            params.put("profile_privacy","on");

    }
    private void registerNow(){

        HttpURLConnection urlConnectionPost=null;
        cookieManager = new CookieManager(null, CookiePolicy.ACCEPT_ALL);
        CookieHandler.setDefault(cookieManager);
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {
            cookieStore.removeAll();
            HttpURLConnection conn= (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/register/").openConnection();
            conn.setRequestMethod("GET");
            Object obj = conn.getContent();

            csrftoken=cookieStore.getCookies().get(0).getValue().toString();

            urlConnectionPost= (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/register/").openConnection();
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

            //obj=urlConnectionPost.getContent();
            BufferedReader reader= new BufferedReader(new InputStreamReader(urlConnectionPost.getInputStream()));
            StringBuffer buffer=new StringBuffer();
            String inputLine;
            while ((inputLine = reader.readLine()) != null)
                buffer.append(inputLine+"\n");
            getResult(buffer.toString());
            int responseCode=urlConnectionPost.getResponseCode();

        } catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            urlConnectionPost.disconnect();
        }
    }
    public void getResult(String result){
        try {
            JSONObject rObj=new JSONObject(result);
            String status=rObj.get("status").toString();
            if (status.equals("success")){
                Toast.makeText(getApplicationContext(),"Registration Successful!", Toast.LENGTH_SHORT).show();
                finish();
            }
            else {
                Toast.makeText(getApplicationContext(),"Registraation Failed!", Toast.LENGTH_SHORT).show();
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    private class RegisterTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            // params comes from the execute() call: params[0] is the url.
            try {
                registerNow();
                return null;
            } catch (Exception e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {

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
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }


}