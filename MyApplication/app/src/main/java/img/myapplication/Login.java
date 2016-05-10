package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
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
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
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
    private StudentModel student=new StudentModel();
    private NewEntrantModel entrant=new NewEntrantModel();
    private String loginURL;
    private String userinfoURL;
    private String appURL;
    private String hostURL;
    private void getURLs(){
        this.hostURL=getString(R.string.host);
        this.loginURL=hostURL+"/login/";
        this.userinfoURL=hostURL+"/new_entrants/userinfo/";
        this.appURL=hostURL+"/new_entrants/";
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        getURLs();
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
        setContentView(R.layout.activity_login);
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
        if (isConnected()){
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
                params.put("password", passwordText);

               new LoginTask().execute();
            }
        }
        else {
            Toast.makeText(getApplicationContext(), "Check network connection!", Toast.LENGTH_LONG).show();
            getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();
        }
    }

    private String peopleLogin() {
        HttpURLConnection urlConnectionPost=null;
        String csrftoken=null;
        cookieManager = new CookieManager(null, CookiePolicy.ACCEPT_ALL);
        CookieHandler.setDefault(cookieManager);
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {

            HttpURLConnection conn= (HttpURLConnection) new URL(loginURL).openConnection();
            conn.setConnectTimeout(3000);
            conn.setReadTimeout(5000);
            conn.setRequestMethod("GET");
            int rcode=conn.getResponseCode();
            if (rcode!= HttpURLConnection.HTTP_OK && rcode!=HttpURLConnection.HTTP_ACCEPTED)
                return "false";
            Object obj = conn.getContent();

            csrftoken=cookieStore.getCookies().get(0).getValue().toString();
            params.put("csrfmiddlewaretoken",csrftoken);
            params.put("remember_me","on");

            urlConnectionPost= (HttpURLConnection) new URL(loginURL).openConnection();
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
                    return "true";
                }
            }



        } catch (Exception e) {
            e.printStackTrace();
            return "error";
        }
        return "false";
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
        protected void onPreExecute(){
            getSupportFragmentManager().beginTransaction().replace(R.id.login_container,new LoginLoad()).addToBackStack(null).commit();
            super.onPreExecute();
        }
        @Override
        protected String doInBackground(String... urls) {
            String login_result=peopleLogin();
            if (login_result.equals("true")) {
                details=new HashMap<String,String>();
                details.put("username",params.get("username"));
                details.put("password", params.get("password"));
                getDetails();
                getUser();
                return "Logged In";
            }
            else
                return login_result;
        }
        @Override
        protected void onPostExecute(String result) {

            if ("false".equals(result)){
                getSupportFragmentManager().popBackStack();
                Toast.makeText(getApplicationContext(),"Enter correct username and password", Toast.LENGTH_LONG).show();
            }
            else if ("error".equals(result)) {
                getSupportFragmentManager().popBackStack();
                Toast.makeText(getApplicationContext(), "Unable to connect to network", Toast.LENGTH_LONG).show();
            }
                else {
                    Toast.makeText(getApplicationContext(),"Login Successful", Toast.LENGTH_SHORT).show();
                    start();
                }
        }
    }

    public void getDetails(){
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {

            HttpURLConnection conn = (HttpURLConnection) new URL(userinfoURL).openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(10000);
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
    public void getUser(){
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
            student.profile_img=downloadImage(hostURL+details.get("photo")
                    ,(int) getResources().getDimension(R.dimen.roundimage_length)
                    ,(int) getResources().getDimension(R.dimen.roundimage_length));
            student.name=details.get("name");
            student.enr_no=details.get("enr_no");
            student.username=details.get("username");
            student.password=details.get("password");
            student.branchname=branchname;
            student.branchcode=branchcode;
            student.year=details.get("year");
            student.town=details.get("hometown");
            student.state=statename;
            student.statecode=statecode;
            student.email=details.get("email");
            student.mobile=details.get("phone");
            student.fb_link=details.get("fb_link");
            student.sess_id=cookieManager.getCookieStore().getCookies().get(1).getValue().toString();


        }
        else if (details.get("category").equals("junior")){
            entrant.id=details.get("id");
            entrant.name=details.get("name");
            entrant.username=details.get("username");
            entrant.password=details.get("password");
            entrant.town=details.get("hometown");
            entrant.state=statename;
            entrant.statecode=statecode;
            entrant.branchname=branchname;
            entrant.branchcode=branchcode;
            entrant.mobile=details.get("phone");
            entrant.email=details.get("email");
            entrant.fb_link=details.get("fb_link");
            entrant.phone_privacy=details.get("phone_privacy").equals("true");
            entrant.sess_id=cookieManager.getCookieStore().getCookies().get(1).getValue().toString();

        }
    }

    public byte[] downloadImage(String url,int ht,int wt){
        int inSampleSize=getSampleSize(url,ht,wt);
        try {
            URL urlConnection = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) urlConnection
                    .openConnection();
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            BitmapFactory.Options options=new BitmapFactory.Options();
            options.inSampleSize=inSampleSize;
            options.inJustDecodeBounds=false;
            Bitmap myBitmap = BitmapFactory.decodeStream(input,null,options);
            ByteArrayOutputStream baos=new ByteArrayOutputStream();
            myBitmap.compress(Bitmap.CompressFormat.PNG,100,baos);
            byte[] img=baos.toByteArray();
            return img;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
    public int getSampleSize(String url,int ht,int wt){

        try {
            HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            BitmapFactory.Options options = new BitmapFactory.Options();
            options.inJustDecodeBounds = true;
            BitmapFactory.decodeStream(input, null, options);

            final int height = options.outHeight;
            final int width = options.outWidth;
            int inSampleSize = 1;

            if (height > ht || width > wt) {

                final int halfHeight = height / 2;
                final int halfWidth = width / 2;

                while ((halfHeight / inSampleSize) > ht
                        && (halfWidth / inSampleSize) > wt) {
                    inSampleSize *= 2;
                }
            }

            return inSampleSize;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return 1;
    }

    public void start(){

        if (details.get("category").equals("senior")){

            MySQLiteHelper db = new MySQLiteHelper(this);
            db.addStudent(student);
            db.close();
            startActivity(new Intent(this, NavigationStudent.class));
            finish();

        }
        else if (details.get("category").equals("junior")){

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
        getMenuInflater().inflate(R.menu.menu_login, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        return super.onOptionsItemSelected(item);
    }
}
