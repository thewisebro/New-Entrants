package img.myapplication;

import android.app.Activity;
import android.content.Intent;
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
import java.util.Map;


public class Login extends ActionBarActivity {
    public Map<String,String> params;
    public Map<String,String> SESSION_VALUES;
    public CookieManager cookieManager;
    public JSONObject userJSON;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
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
        SESSION_VALUES=new HashMap<String,String>();
        setContentView(R.layout.activity_login2);
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
        if (!isConnected()){
            Toast.makeText(getApplicationContext(), "Not Connected", Toast.LENGTH_SHORT).show();
        }
        else {
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

            HttpURLConnection conn= (HttpURLConnection) new URL("http://people.iitr.ernet.in/login/").openConnection();
            conn.setRequestMethod("GET");
            Object obj = conn.getContent();

            csrftoken=cookieStore.getCookies().get(0).getValue().toString();
            params.put("csrfmiddlewaretoken",csrftoken);
            params.put("remember_me","on");

            urlConnectionPost= (HttpURLConnection) new URL("http://people.iitr.ernet.in/login/").openConnection();
            urlConnectionPost.setDoOutput(true);
            urlConnectionPost.setDoInput(true);
            urlConnectionPost.setRequestMethod("POST");
            urlConnectionPost.setRequestProperty("Cookie", TextUtils.join(";", cookieStore.getCookies()));
            cookieStore.removeAll();

            urlConnectionPost.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            urlConnectionPost.setRequestProperty("Host","people.iitr.ernet.in");
            urlConnectionPost.setRequestProperty("Origin","http://people.iitr.ernet.in");
            urlConnectionPost.setRequestProperty("Referer","http://people.iitr.ernet.in/login/");
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
                    SESSION_VALUES.put("csrftoken",cookieStore.getCookies().get(0).getValue().toString());
                    SESSION_VALUES.put("CHANNELI_SESSID",cookieStore.getCookies().get(1).getValue().toString());
                    result=true;
                }
            }



        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }
    private void getUser(){
        CookieHandler.setDefault(cookieManager);
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {

            HttpURLConnection conn = (HttpURLConnection) new URL("http://people.iitr.ernet.in/peoplesearch/return_details/?username="+params.get("username")).openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Cookie", TextUtils.join(";", cookieStore.getCookies()));
            conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            conn.setRequestProperty("Accept", "application/xml");

            //Object obj = conn.getContent();
            BufferedReader reader= new BufferedReader(new InputStreamReader(conn.getInputStream()));
            StringBuffer buffer=new StringBuffer();
            String inputLine;
            while ((inputLine = reader.readLine()) != null)
                buffer.append(inputLine+"\n");
            parseUserData(buffer.toString());
            int responseCode=conn.getResponseCode();
        }catch (IOException e) {
            e.printStackTrace();
        }
    }
    private void parseUserData(String userDetails){
        try {
            userJSON= new JSONObject(userDetails);
            userJSON.remove("msg");
            userJSON.remove("session_variable");
            userJSON.put("username", params.get("username"));
            userJSON.put("password",params.get("password"));
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
                    getUser();
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
            if (SESSION_VALUES.size()>0){
                Toast.makeText(getApplicationContext(),"Login Successful", Toast.LENGTH_SHORT).show();
                MySQLiteHelper db=new MySQLiteHelper(getApplication());

            }
            else {
                Toast.makeText(getApplicationContext(),"Enter correct Username or Password", Toast.LENGTH_SHORT).show();
            }
        }
    }

    public void register(View view){
        /*Intent intent = new Intent(this, Register.class);
        startActivity(intent);*/
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
