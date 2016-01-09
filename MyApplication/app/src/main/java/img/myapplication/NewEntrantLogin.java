package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
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

        JSONObject userobj=new JSONObject();
        try {
            userobj.put("Username",Username.getText().toString());

            userobj.put("Password",Password.getText().toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
        //new HttpAsyncTask(userobj).execute();
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

        int id = item.getItemId();

        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
    private class HttpAsyncTask extends AsyncTask<String, Void, String> {
        JSONObject user;
        public HttpAsyncTask(JSONObject userobj){
            user=userobj;
        }
        @Override
        protected String doInBackground(String... urls) {

            return POST(urls[0],user);
        }
        @Override
        protected void onPostExecute(String result) {
            Toast.makeText(getBaseContext(), "Data Sent!", Toast.LENGTH_LONG).show();
        }
    }

    private static String POST(String url,JSONObject userobj){
        String result="";
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

        } catch (Exception e) {
            Log.d("InputStream", e.getLocalizedMessage());
        }

        return result;
    }

}
