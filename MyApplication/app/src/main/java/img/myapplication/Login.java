package img.myapplication;

import android.app.Activity;
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
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.CookieManager;
import java.net.CookieStore;
import java.net.HttpCookie;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.Map;


public class Login extends ActionBarActivity {
    public JSONObject userobj;
    public String usernameText;
    public String passwordText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        MySQLiteHelper db=new MySQLiteHelper(this);
/*
        if (db.loggedEntrant()){
            Intent intent=new Intent(this, Navigation.class);
            startActivity(intent);
            finish();
        }
        else if (db.loggedStudent()){
            Intent intent=new Intent(this,NavigationStudent.class);
            startActivity(intent);
            finish();
        }*/
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
            usernameText= Username.getText().toString();
            passwordText= Password.getText().toString();
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

            if(cookiesHeader != null)
            {
                cookieStore.add(null, HttpCookie.parse(cookiesHeader).get(0));
            }
            else return null;
            csrftoken=cookieStore.getCookies().get(0).getValue().toString();
            try {
                userobj.put("csrfmiddlewaretoken",csrftoken);
                userobj.put("remember_me","on");
            } catch (JSONException e) {
                e.printStackTrace();
            }
            urlConnectionGet.disconnect();


            urlConnectionPost= (HttpURLConnection) new URL("http://people.iitr.ernet.in/login/").openConnection();
            //urlConnectionPost= (HttpURLConnection) new URL("http://172.25.55.156:8000/login/").openConnection();
            urlConnectionPost.setDoOutput(true);
            urlConnectionPost.setDoInput(true);
            urlConnectionPost.setRequestMethod("POST");
            urlConnectionPost.setRequestProperty("Cookie", TextUtils.join(";", cookieStore.getCookies()));
            cookieStore.removeAll();

/*
            urlConnectionPost.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            urlConnectionPost.setRequestProperty("Accept", "application/json");*/
            //urlConnectionPost.connect();

           /* Writer writer = new BufferedWriter(new OutputStreamWriter(urlConnectionPost.getOutputStream(), "UTF-8"));
            writer.write(String.valueOf(userobj));
            writer.flush();*/

            String charset="UTF-8";
/*            String query=URLEncoder.encode("username",charset)+"="+ URLEncoder.encode(usernameText, charset)+
                    "&password="+URLEncoder.encode(passwordText,charset)+
                    "&csrfmiddlewaretoken="+URLEncoder.encode(csrftoken,charset)+
                    "&remember_me=on";
            urlConnectionPost.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

            PrintWriter writer= new PrintWriter(urlConnectionPost.getOutputStream());
            writer.write(query);
            writer.flush();
*/
/*            StringBuilder sb=new StringBuilder();
            sb.append(URLEncoder.encode("username", charset) + "=" + URLEncoder.encode(usernameText, charset));
            sb.append("&"+URLEncoder.encode("password",charset)+"=" + URLEncoder.encode(passwordText, charset));
            sb.append("&"+URLEncoder.encode("csrfmiddlewaretoken",charset)+"=" + URLEncoder.encode(csrftoken, charset));
            sb.append("&"+URLEncoder.encode("remember_me",charset)+"=" + URLEncoder.encode("ok", charset));
            String query=sb.toString();
*/
            urlConnectionPost.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            urlConnectionPost.setRequestProperty("Host","people.iitr.ernet.in");
            urlConnectionPost.setRequestProperty("Origin","http://people.iitr.ernet.in");
            urlConnectionPost.setRequestProperty("Referer","http://people.iitr.ernet.in/login/");
            urlConnectionPost.setRequestProperty("Accept","application/xml");
            Uri.Builder builder = new Uri.Builder()
                    .appendQueryParameter("username", usernameText)
                    .appendQueryParameter("password", passwordText)
                    .appendQueryParameter("csrfmiddlewaretoken", csrftoken)
                    .appendQueryParameter("remember_me","on");
            String query = builder.build().getEncodedQuery();
            urlConnectionPost.connect();

            OutputStream os = urlConnectionPost.getOutputStream();
            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(os, "UTF-8"));
            writer.write(query);
            writer.flush();
            writer.close();
            os.close();

            int responseCode=urlConnectionPost.getResponseCode();
            String msg=urlConnectionPost.getResponseMessage();
            InputStream inputStream = urlConnectionPost.getInputStream();
            StringBuffer buffer = new StringBuffer();
            if (inputStream == null) {
                // Nothing to do.
                return null;
            }
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
            String inputLine;
            while ((inputLine = reader.readLine()) != null)
                buffer.append(inputLine + "\n");

           // if (buffer.length() == 0) {
                // Stream was empty. No point in parsing.
           //     return null;
           // }


            Map<String, List<String>> headerFields = urlConnectionPost.getHeaderFields();
            List<String> cookiesHeaders = headerFields.get(COOKIES_HEADER);

            if(cookiesHeaders != null)
            {
                for (String cookie : cookiesHeaders)
                {
                    cookieStore.add(null,HttpCookie.parse(cookie).get(0));
                }
            }
            csrftoken=cookieStore.getCookies().get(0).getValue().toString();
            CHANNELI_SESSID=cookieStore.getCookies().get(1).getValue().toString();


        } catch (IOException e) {
            e.printStackTrace();
        } finally {
                   }
        //return cookiesHeader;
        return null;
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
