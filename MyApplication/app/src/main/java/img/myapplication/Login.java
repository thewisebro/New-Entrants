package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.CookieManager;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;


public class Login extends ActionBarActivity {

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

        EditText Username=(EditText) findViewById(R.id.et_username);
        EditText Password=(EditText) findViewById(R.id.et_Password);

        JSONObject userobj=new JSONObject();
        try {
            userobj.put("Username",Username.getText().toString());
            userobj.put("Password",Password.getText().toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
        peopleLogin(userobj);
    }
 /*   private void peopleLogin(JSONObject userobj){
        try {
            URL urlobj=new URL("");
            HttpURLConnection conn= (HttpURLConnection) urlobj.openConnection();
            conn.setDoOutput(true);
            conn.setDoInput(true);
            conn.setRequestMethod("GET");

        } catch (java.io.IOException e) {
            e.printStackTrace();
        }
// Continue from here
    }*/
    private void peopleLogin(JSONObject userobj){
        HttpURLConnection urlConnection = null;
        try {
            String csrftoken=null;
            String CHANNELI_SESSID=null;
            URL url=new URL("http://people.iitr.ernet.in/login/");
            urlConnection = (HttpURLConnection) url.openConnection();
            CookieManager cookieManager = CookieManager.getInstance();
            urlConnection.setRequestMethod("GET");
            String cookie = cookieManager.getCookie(urlConnection.getURL().toString());
            csrftoken=(getValues(cookie))[0];
            cookieManager.setCookie("http://people.iitr.ernet.in/login/", "csrftoken=" + csrftoken);
            urlConnection.connect();
            cookie = cookieManager.getCookie(urlConnection.getURL().toString());
            String values[]=getValues(cookie);
            csrftoken=values[0];
            CHANNELI_SESSID=values[1];
            cookieManager.setCookie("http://people.iitr.ernet.in/login/","csrftoken="+csrftoken+";CHANNELI_SESSID="+CHANNELI_SESSID);
            urlConnection.setRequestMethod("POST");
            urlConnection.connect();

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (urlConnection != null) {
                urlConnection.disconnect();
            }
        }
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
