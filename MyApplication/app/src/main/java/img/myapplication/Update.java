package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;

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

import models.StudentModel;


public class Update extends ActionBarActivity {

    private Spinner state;
    private EditText name;
    private EditText username;
    private EditText branch;
    private EditText town;
    private EditText mobile;
    private EditText email;
    private EditText fblink;
    private StudentModel student;
    private CookieManager cookieManager;
    private Map<String,String> params=new HashMap<String,String>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_update);
        student= (StudentModel) getIntent().getSerializableExtra("student");

        setViews();
        setInitial();

        Button bt= (Button) findViewById(R.id.button_submit);
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConnected());
                    new UpdateSubmitTask().execute();
            }
        });

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
        name= (EditText) findViewById(R.id.u_name);
        username= (EditText) findViewById(R.id.u_username);
        town= (EditText) findViewById(R.id.u_town);
        branch= (EditText) findViewById(R.id.u_branch);
        mobile= (EditText) findViewById(R.id.u_mobile);
        email= (EditText) findViewById(R.id.u_email);
        fblink= (EditText) findViewById(R.id.u_fblink);

        state= (Spinner) findViewById(R.id.u_state);
        ArrayAdapter<CharSequence> stateList=ArrayAdapter.createFromResource(this,R.array.states,android.R.layout.simple_spinner_item);
        stateList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        state.setAdapter(stateList);
    }
    private void setInitial(){
            name.setText(student.name);
            username.setText(student.username);
            branch.setText(student.branchname);
            mobile.setText(student.mobile);
            email.setText(student.email);
            fblink.setText(student.fb_link);
            town.setText(student.town);
            state.setSelection(getSpinnerPos(student.statecode));
    }
    private int getSpinnerPos(String state){
        if (!state.isEmpty()){
            String[] list= getResources().getStringArray(R.array.state_codes);
            for (int i=1;i<list.length;i++)
                if (list[i].equals(state.toCharArray()))
                    return i;
        }
        return 0;
    }
    private class UpdateSubmitTask extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... urls) {
            cookieManager=new CookieManager(null, CookiePolicy.ACCEPT_ALL);
            CookieHandler.setDefault(cookieManager);
            CookieStore cookieStore=cookieManager.getCookieStore();
            try {
                HttpURLConnection connGet= (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/update/").openConnection();
                connGet.setRequestMethod("GET");
                connGet.setRequestProperty("Cookie","CHANNELI_SESSID="+student.sess_id);
                Object obj=connGet.getContent();
                //String csrftoken=cookieStore.getCookies().get(0).getValue();

                HttpURLConnection connPost= (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/update/").openConnection();
                connPost.setRequestMethod("POST");
                connPost.setDoInput(true);
                connPost.setDoOutput(true);
                connPost.setRequestProperty("Cookie", "CHANNELI_SESSID=" + student.sess_id);
                //connPost.setRequestProperty("Cookie", "CHANNELI_SESSID=" + student.sess_id + ";csrftoken=" + csrftoken);
                getParams();
                //params.put("csrfmiddlewaretoken",csrftoken);
                Uri.Builder builder = new Uri.Builder();
                for (Map.Entry<String, String> entry : params.entrySet()){
                    builder.appendQueryParameter(entry.getKey(),entry.getValue());
                }
                String query = builder.build().getEncodedQuery();
                connPost.setUseCaches(false);
                OutputStream os = connPost.getOutputStream();
                BufferedWriter writer = new BufferedWriter(
                        new OutputStreamWriter(os, "UTF-8"));
                writer.write(query);
                writer.flush();
                writer.close();
                os.close();
                int rcode=connPost.getResponseCode();
                BufferedReader reader= new BufferedReader(new InputStreamReader(connPost.getInputStream()));
                StringBuffer buffer=new StringBuffer();
                String inputLine;
                while ((inputLine = reader.readLine()) != null)
                    buffer.append(inputLine+"\n");
                String result=buffer.toString();
                JSONObject object=new JSONObject(buffer.toString());
                return object.getString("status");
                //return  null;
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")){
                student.email=params.get("email");
                student.state=params.get("state");
                student.town=params.get("hometown");
                student.mobile=params.get("phone_no");
                student.fb_link=params.get("fb_link");

                MySQLiteHelper db=new MySQLiteHelper(getApplicationContext());
                db.deleteStudent();
                db.addStudent(student);
                db.close();
                startActivity(new Intent(getApplicationContext(), NavigationStudent.class));
                finish();
            }
        }
    }
    public void getParams(){
        params.put("email",email.getText().toString().trim());
        params.put("state",(getResources().getStringArray(R.array.state_codes))[state.getSelectedItemPosition()]);
        params.put("fb_link",fblink.getText().toString().trim());
        params.put("phone_no",mobile.getText().toString().trim());
        params.put("hometown",town.getText().toString().trim());
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_update, menu);
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
