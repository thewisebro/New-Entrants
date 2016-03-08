package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
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
import java.util.Iterator;
import java.util.Map;

import models.NewEntrantModel;
import models.StudentModel;


public class Login extends ActionBarActivity {
    public Map<String,String> params;
    public CookieManager cookieManager;
    public Map<String,String> details;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        MySQLiteHelper db=new MySQLiteHelper(this);

        if (db.loggedEntrant()){
            Intent intent=new Intent(this, Navigation.class);
            startActivity(intent);
            finish();
        }
        else if (db.loggedStudent()){
            Intent intent=new Intent(this,NavigationStudent.class);
            startActivity(intent);
            finish();
        }

        params=new HashMap<String,String>();
        setContentView(R.layout.activity_login2);
    }
    //public TextView blogText;
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }
    public void login(View view){
        if (!isConnected()){
            Toast.makeText(getApplicationContext(), "Not Connected", Toast.LENGTH_SHORT).show();
        }
        else {
            params.clear();
            EditText Username=(EditText) findViewById(R.id.et_username);
            EditText Password=(EditText) findViewById(R.id.et_Password);
            String usernameText= Username.getText().toString();
            String passwordText= Password.getText().toString();
            if (usernameText.matches("")){
                Toast.makeText(getApplicationContext(),"Enter username", Toast.LENGTH_SHORT).show();
            }
            else if (passwordText.matches("")){
                Toast.makeText(getApplicationContext(),"Enter password", Toast.LENGTH_SHORT).show();
            }
            else {
                params.put("username",usernameText);
                params.put("password",passwordText);

                new LoginTask().execute();
            }
        }
    }

    private boolean peopleLogin() throws IOException{
        Boolean result=false;
        HttpURLConnection urlConnectionPost=null;
        String csrftoken=null;
        cookieManager = new CookieManager(null, CookiePolicy.ACCEPT_ALL);
        CookieHandler.setDefault(cookieManager);
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {

            HttpURLConnection conn= (HttpURLConnection) new URL("http://192.168.121.187:8080/login/").openConnection();
            conn.setRequestMethod("GET");
            Object obj = conn.getContent();

            csrftoken=cookieStore.getCookies().get(0).getValue().toString();
            params.put("csrfmiddlewaretoken",csrftoken);
            params.put("remember_me","on");

            urlConnectionPost= (HttpURLConnection) new URL("http://192.168.121.187:8080/login/").openConnection();
            urlConnectionPost.setDoOutput(true);
            urlConnectionPost.setDoInput(true);
            urlConnectionPost.setRequestMethod("POST");
            urlConnectionPost.setRequestProperty("Cookie", TextUtils.join(";", cookieStore.getCookies()));
            cookieStore.removeAll();

            urlConnectionPost.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            urlConnectionPost.setRequestProperty("Accept","application/xml");
            urlConnectionPost.setInstanceFollowRedirects(true);

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

            int responseCode=urlConnectionPost.getResponseCode();


            if (responseCode== HttpURLConnection.HTTP_OK){
                obj=urlConnectionPost.getContent();
                if (cookieStore.getCookies().size()>1){
                    result=true;
                }
            }



        } catch (IOException e) {
            e.printStackTrace();
        }
        finally {
            urlConnectionPost.disconnect();
        }
        return result;
    }

    private void parseUserData(String userDetails){
        try {
            JSONObject userJSON= new JSONObject(userDetails);
            Iterator<String> keys=userJSON.keys();
            while (keys.hasNext()){
                String key=keys.next();
                String val=userJSON.getString(key);
                if (val!=null){
                    details.put(key,val);
                }
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private class LoginTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            // params comes from the execute() call: params[0] is the url.
            try {
                if (peopleLogin()) {
                    details=new HashMap<String,String>();
                    details.put("username",params.get("username"));
                    details.put("password", params.get("password"));
                    getDetails();
                    return "Logged In";
                }
                else return null;
            } catch (IOException e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (cookieManager.getCookieStore().getCookies().size()>0){
                Toast.makeText(getApplicationContext(),"Login Successful", Toast.LENGTH_SHORT).show();
                start();
            }
            else {
                Toast.makeText(getApplicationContext(),"Enter correct Username or Password", Toast.LENGTH_SHORT).show();
            }
        }
    }
    public void getDetails(){
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {

            HttpURLConnection conn = (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/userinfo/").openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Cookie", TextUtils.join(";", cookieStore.getCookies()));
            conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            conn.setRequestProperty("Accept", "application/xml");

            BufferedReader reader= new BufferedReader(new InputStreamReader(conn.getInputStream()));
            StringBuffer buffer=new StringBuffer();
            String inputLine;
            while ((inputLine = reader.readLine()) != null)
                buffer.append(inputLine+"\n");
            parseUserData(buffer.toString());
            int responseCode=conn.getResponseCode();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void start(){
        String branchname = null;
        String branchcode=null;
        String statename=null;
        String statecode=null;

        try {
            JSONObject object=new JSONObject(details.get("branch"));
            branchcode=object.getString("code");
            branchname=object.getString("name");

            object=new JSONObject(details.get("state"));
            statecode=object.getString("code");
            statename=object.getString("name");

        } catch (JSONException e) {
            e.printStackTrace();
        }

        if (details.get("category").equals("senior")){
            StudentModel student=new StudentModel();
            student.name=details.get("name");
            student.enr_no=details.get("enr_no");
            student.username=details.get("username");
            student.password=details.get("password");
            student.branchname=branchname;
            student.branchcode=branchcode;
            student.year=details.get("year");
            student.town=details.get("town");
            student.state=statename;
            student.statecode=statecode;
            student.email=details.get("email");
            student.mobile=details.get("mobile");
            student.fb_link=details.get("fb_link");
            student.sess_id=cookieManager.getCookieStore().getCookies().get(1).getValue().toString();
            MySQLiteHelper db=new MySQLiteHelper(this);
            db.addStudent(student);
            db.close();
            startActivity(new Intent(this,NavigationStudent.class));
            finish();
        }
        else if (details.get("category").equals("junior")){
            NewEntrantModel entrant= new NewEntrantModel();
            entrant.id=details.get("id");
            entrant.name=details.get("name");
            entrant.username=details.get("username");
            entrant.password=details.get("password");
            entrant.town=details.get("town");
            entrant.state=statename;
            entrant.statecode=statecode;
            entrant.branchname=branchname;
            entrant.branchcode=branchcode;
            entrant.mobile=details.get("mobile");
            entrant.email=details.get("email");
            entrant.fb_link=details.get("fb_link");
            entrant.profile_privacy=details.get("profile_privacy").equals("true");
            entrant.phone_privacy=details.get("phone_privacy").equals("true");
            entrant.sess_id=cookieManager.getCookieStore().getCookies().get(1).getValue().toString();
            MySQLiteHelper db=new MySQLiteHelper(this);
            db.addEntrant(entrant);
            db.close();
            startActivity(new Intent(this,Navigation.class));
            finish();
        }
    }

    public void register(View view){
        Intent intent = new Intent(this, Register.class);
        startActivity(intent);
    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_login, menu);
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
