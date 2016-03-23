package img.myapplication;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
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

import models.NewEntrantModel;

public class Register extends AppCompatActivity {

    public NewEntrantModel entrant;
    public MySQLiteHelper db;
    public CookieManager cookieManager;
    public Map<String,String > params;
    public String csrftoken;
    public ImageView img;
    public int pos_state;
    public int pos_branch;
    public int PICK_IMAGE_REQUEST=1;
    public int REQUEST_CAMERA=1;
    public int SELECT_FILE=2;
    private String registerURL="http://192.168.121.187:8080/new_entrants/register/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        ActionBar bar=getSupportActionBar();
        bar.setHomeButtonEnabled(true);
        bar.setDisplayHomeAsUpEnabled(true);
        db=new MySQLiteHelper(this);
        entrant=new NewEntrantModel();
        setContentView(R.layout.register_new);

        img= (ImageView) findViewById(R.id.profile_img);
        img.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                pickImage();
            }
        });

    }
    private void pickImage() {
        final CharSequence[] items = { "Take Photo", "Choose from Library", "Cancel" };

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Select Picture");
        builder.setItems(items, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int item) {
                if (items[item].equals("Take Photo")) {
                    Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    startActivityForResult(intent, REQUEST_CAMERA);
                } else if (items[item].equals("Choose from Library")) {
                    Intent intent = new Intent(Intent.ACTION_GET_CONTENT,
                            android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                    intent.setType("image/*");
                    startActivityForResult(Intent.createChooser(intent, "Select File"), SELECT_FILE);
                } else if (items[item].equals("Cancel")) {
                    dialog.dismiss();
                }
            }
        });
        builder.show();
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == SELECT_FILE && resultCode == RESULT_OK && data != null && data.getData() != null) {

            Uri uri = data.getData();

            try {
                Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), uri);
                ImageView imageView = (ImageView) findViewById(R.id.profile_img);
                imageView.setImageBitmap(bitmap);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else if (requestCode == REQUEST_CAMERA && resultCode == RESULT_OK && data != null) {

            Bitmap bitmap = (Bitmap) data.getExtras().get("data");
            ImageView imageView = (ImageView) findViewById(R.id.profile_img);
            imageView.setImageBitmap(bitmap);
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

    public void register(View view) throws IllegalAccessException {
        if (isConnected()){
            pos_branch=((Spinner) findViewById(R.id.new_branch)).getSelectedItemPosition();
            pos_state=((Spinner) findViewById(R.id.new_state)).getSelectedItemPosition();
            entrant.name= ((EditText) findViewById(R.id.new_name)).getText().toString().trim();
            entrant.username= ((EditText) findViewById(R.id.new_username)).getText().toString().trim();
            entrant.password= ((EditText) findViewById(R.id.new_password)).getText().toString().trim();
            entrant.town= ((EditText) findViewById(R.id.new_town)).getText().toString().trim();
            entrant.email= ((EditText) findViewById(R.id.new_email)).getText().toString().trim();
            entrant.mobile= ((EditText) findViewById(R.id.new_mobile)).getText().toString().trim();
            entrant.fb_link= ((EditText) findViewById(R.id.new_fblink)).getText().toString().trim();
            entrant.branchname=((Spinner) findViewById(R.id.new_branch)).getSelectedItem().toString().trim();
            entrant.branchcode=(getResources().getStringArray(R.array.branch_codes))[pos_branch];
            entrant.state= ((Spinner) findViewById(R.id.new_branch)).getSelectedItem().toString().trim();
            entrant.statecode=(getResources().getStringArray(R.array.state_codes))[pos_state];
            entrant.phone_privacy= ((CheckBox) findViewById(R.id.contact_visibilty)).isChecked();
            entrant.profile_privacy= ((CheckBox) findViewById(R.id.profile_visibilty)).isChecked();
            Bitmap imgBitmap= ((BitmapDrawable)((ImageView) findViewById(R.id.profile_img)).getDrawable()).getBitmap();
            ByteArrayOutputStream baos= new ByteArrayOutputStream();
            imgBitmap.compress(Bitmap.CompressFormat.PNG,100,baos);
            entrant.profile_img=baos.toByteArray();
            if(validate())
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
        String townPattern="^$|^[a-zA-Z ]+$";
        String fbPattern="^$|^[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+$";
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
        if(!(entrant.password).equals(((EditText) findViewById(R.id.re_password)).getText().toString())){
            Toast.makeText(getApplicationContext(),"Passwords do not match", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(entrant.town).matches(townPattern)){
            Toast.makeText(getApplicationContext(),"Enter a proper City name", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if (!(entrant.fb_link).matches(fbPattern)){
            Toast.makeText(getApplicationContext(), "Invalid valid Facebook link", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if (pos_state==0){
            Toast.makeText(getApplicationContext(), "Select a State", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        return flag;
    }
    private void setParams() throws IllegalAccessException {
        params=new HashMap<String,String>();
        params.put("csrfmiddlewaretoken",csrftoken);
        params.put("name",entrant.name);
        params.put("username",entrant.username);
        params.put("password1",entrant.password);
        params.put("password2",entrant.password);
        params.put("branch",entrant.branchcode);
        params.put("email",entrant.email);
        params.put("fb_link",entrant.fb_link);
        params.put("state",entrant.statecode);
        params.put("hometown",entrant.town);
        params.put("phone_no",entrant.mobile);
        if (entrant.phone_privacy)
            params.put("phone_privacy","on");

        if (entrant.profile_privacy)
            params.put("profile_privacy","on");

    }
    private String registerNow(){
        String result=null;
        HttpURLConnection urlConnectionPost=null;
        cookieManager = new CookieManager(null, CookiePolicy.ACCEPT_ALL);
        CookieHandler.setDefault(cookieManager);
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {
            cookieStore.removeAll();
            HttpURLConnection conn= (HttpURLConnection) new URL(registerURL).openConnection();
            conn.setRequestMethod("GET");
            conn.setReadTimeout(5000);
            if (conn.getResponseCode()== HttpURLConnection.HTTP_OK) {
                Object obj = conn.getContent();
            }

            csrftoken=cookieStore.getCookies().get(0).getValue().toString();

            urlConnectionPost= (HttpURLConnection) new URL(registerURL).openConnection();
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

            BufferedReader reader= new BufferedReader(new InputStreamReader(urlConnectionPost.getInputStream()));
            StringBuffer buffer=new StringBuffer();
            String inputLine;
            while ((inputLine = reader.readLine()) != null)
                buffer.append(inputLine+"\n");
            result=getResult(buffer.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }
    public String getResult(String result){
        String status=null;
        try {
            JSONObject rObj=new JSONObject(result);
            status=rObj.get("status").toString();

        } catch (JSONException e) {
            e.printStackTrace();
        }
        return status;
    }
    private class RegisterTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {

            try {
                return registerNow();
            } catch (Exception e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")){
                Toast.makeText(getApplicationContext(),"Registration Successful!", Toast.LENGTH_SHORT).show();
                finish();
            }
            else {
                Toast.makeText(getApplicationContext(),"Registration Failed!", Toast.LENGTH_SHORT).show();
            }
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
        if (id==android.R.id.home) {
            finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }


}