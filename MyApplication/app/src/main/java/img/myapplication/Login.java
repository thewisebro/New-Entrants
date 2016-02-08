package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.OutputStream;
import java.net.CookieManager;
import java.net.CookieStore;
import java.net.HttpCookie;
import java.net.HttpURLConnection;
import java.net.URL;


public class Login extends ActionBarActivity {
    public JSONObject userobj;

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

                try {
                    userobj=new JSONObject();
                    userobj.put("username",Username.getText().toString());
                    userobj.put("password",Password.getText().toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                //peopleLogin(userobj);
                new LoginTask().execute();
            }
        }
    }

    private String peopleLogin() throws IOException{
        HttpURLConnection urlConnectionGet = null;
        HttpURLConnection urlConnectionPost=null;
        String COOKIES_HEADER = "Set-Cookie";
        String cookiesHeader=null;
        String csrftoken=null;
        String CHANNELI_SESSID=null;
        CookieManager msCookieManager = new CookieManager();
        CookieStore cookieStore=msCookieManager.getCookieStore();
        try {
            URL url=new URL("http://people.iitr.ernet.in/login/");
            urlConnectionGet = (HttpURLConnection) url.openConnection();
            urlConnectionGet.setDoInput(true);
            urlConnectionGet.setRequestMethod("GET");
            urlConnectionGet.connect();
            cookiesHeader=urlConnectionGet.getHeaderField(COOKIES_HEADER);
            //Map<String, List<String>> headerFields = urlConnection.getHeaderFields();
            //List<String> cookiesHeader = headerFields.get(COOKIES_HEADER);

            if(cookiesHeader != null)
            {
                /*
                for (String cookie : cookiesHeader)
                {
                    cookieStore.add(null, HttpCookie.parse(cookie).get(0));
                }
                */
                cookieStore.add(null, HttpCookie.parse(cookiesHeader).get(0));
            }
            else return null;

            csrftoken=cookieStore.getCookies().get(0).getValue().toString();
            try {
                userobj.put("csrfmiddlewaretoken",csrftoken);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            //urlConnection.disconnect();
            urlConnectionPost= (HttpURLConnection) new URL("http://people.iitr.ernet.in/login/channeli_login").openConnection();
            urlConnectionPost.setDoOutput(true);
            urlConnectionPost.setRequestMethod("POST");
            urlConnectionPost.setRequestProperty("Cookie", "csrftoken=" + csrftoken);
            urlConnectionPost.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            //urlConnection.setRequestProperty("Accept", "application/json");
/*
            OutputStreamWriter osw=new OutputStreamWriter(urlConnectionPost.getOutputStream(), "UTF-8");
            osw.write(userobj.toString());
            osw.flush();
*/
            OutputStream os= urlConnectionPost.getOutputStream();
            byte[] objInBytes = userobj.toString().getBytes("UTF-8");
            os.write(objInBytes);
            os.close();

            int responseCode=urlConnectionPost.getResponseCode();
            StringBuilder sb=new StringBuilder();


        } catch (IOException e) {
            e.printStackTrace();
        } finally {
                   }
        //return cookiesHeader;
        return null;
    }
    private String[] getValues(String cookie){
        String[] values=cookie.split(";");
        String v[]=new String[2];
        for(String temp : values){
            String[] list=temp.split("=");
            if (list[0].equals("csrftoken")){
                v[0]=list[1];
            }
            else if (list[0].equals("CHANNELI_SESSID")){
               v[1]=list[1];
            }
        }
        return v;
    }
    private class LoginTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            // params comes from the execute() call: params[0] is the url.
            try {
                return peopleLogin();
            } catch (IOException e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {

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
