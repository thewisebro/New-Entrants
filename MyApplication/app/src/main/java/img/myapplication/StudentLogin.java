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


import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.net.URLConnection;

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
        User_Model user=db.getUser(Enr_No.getText().toString(),Password.getText().toString());
        if(db.checkUser(Enr_No.getText().toString(), Password.getText().toString()))
        {
            Intent intent =new Intent(this, NavigationStudent.class);
            Bundle mBundle=new Bundle();
            mBundle.putSerializable("user",user);
            intent.putExtras(mBundle);
            startActivity(intent);
            finish();
        }
        else Toast.makeText(getApplicationContext(), "Wrong Username or Password", Toast.LENGTH_SHORT).show();

        JSONObject userobj=new JSONObject();
        userobj.put("Enr_No",Enr_No.getText().toString());
        userobj.put("Password",Password.getText().toString());
        new HttpAsyncTask(userobj).execute();
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
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            Toast.makeText(getBaseContext(), "Data Sent!", Toast.LENGTH_LONG).show();
        }
    }

    private static String POST(String url,JSONObject userobj){
        String result="";
        try{
            /*HttpClient client=new DefaultHttpClient();
            HttpPost httpPost=new HttpPost(url);

            String user=userobj.toString();
            StringEntity se= new StringEntity(user);
            httpPost.setEntity(se);
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");
            HttpResponse httpResponse=client.execute(httpPost);
            is=httpResponse.getEntity().getContent();*/
            URL urlobj=new URL(url);
            URLConnection conn=urlobj.openConnection();
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
