package features;

import android.annotation.SuppressLint;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.CookieManager;
import java.net.CookieStore;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import img.myapplication.R;
import models.NewEntrantModel;
import models.StudentModel;


@SuppressLint("ValidFragment")
public class ProfileFragment extends Fragment {
    private StudentModel student;
    private NewEntrantModel entrant;
    private String category;
    public Spinner state;
    public Spinner branch;
    public EditText name;
    public EditText username;
    public EditText password;
    public EditText re_password;
    public EditText town;
    public EditText mobile;
    public EditText email;
    public EditText fblink;
    public CheckBox cb_contact;
    public CheckBox cb_profile;
    private Map<String,String> params;

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){

        View view= inflater.inflate(R.layout.fragment_profile, container, false);

        setViews(view);
        setInitial(view);
        Button bt= (Button) view.findViewById(R.id.bt_update);
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getValues();
                if (validate()){
                    new UpdateTask().execute();
                }
            }
        });
        return view;
    }
    public ProfileFragment(Object user,String category){
        if (category.equals("entrant"))
            entrant= (NewEntrantModel) user;
        else
            student= (StudentModel) user;
        this.category=category;
    }
    private void getValues(){
        params=new HashMap<String,String>();
        params.put("email",email.getText().toString().trim());
        params.put("branchname",branch.getSelectedItem().toString());
        params.put("branch", (getResources().getStringArray(R.array.branch_codes))[branch.getSelectedItemPosition()]);

        params.put("statename",state.getSelectedItem().toString());
        params.put("state", (getResources().getStringArray(R.array.state_codes))[state.getSelectedItemPosition()]);

        params.put("hometown",town.getText().toString().trim());
        params.put("fb_link",fblink.getText().toString().trim());
        params.put("phone_no",mobile.getText().toString().trim());
        if (category.equals("entrants")){
            if (cb_profile.isChecked())
                params.put("profile_privacy","True");
            if (cb_contact.isChecked())
                params.put("phone_privacy","True");
        }
    }
    private void setViews(View v){
        state= (Spinner) v.findViewById(R.id.list_states);
        branch= (Spinner) v.findViewById(R.id.list_branches);
        name= (EditText) v.findViewById(R.id.name);
        username= (EditText) v.findViewById(R.id.username);
        password= (EditText) v.findViewById(R.id.password);
        re_password= (EditText) v.findViewById(R.id.password_re);
        town= (EditText) v.findViewById(R.id.town);
        mobile= (EditText) v.findViewById(R.id.mobile);
        email= (EditText) v.findViewById(R.id.email);
        fblink= (EditText) v.findViewById(R.id.fblink);
        cb_contact= (CheckBox) v.findViewById(R.id.ed_contact_visibilty);
        cb_profile= (CheckBox) v.findViewById(R.id.ed_profile_visibilty);
    }
    private void setInitial(View v){
        v.findViewById(R.id.password_row).setVisibility(View.GONE);
        v.findViewById(R.id.re_row).setVisibility(View.GONE);

        if (category.equals("student")){
            cb_contact.setVisibility(View.GONE);
            cb_profile.setVisibility(View.GONE);

            name.setText(student.name);
            username.setText(student.username);
            //password.setText(student.password);
            //re_password.setText(student.password);
            mobile.setText(student.mobile);
            email.setText(student.email);
            fblink.setText(student.fb_link);
            town.setText(student.town);
            state.setSelection(getSpinnerPos(student.statecode, getResources().getStringArray(R.array.state_codes)));
            branch.setSelection(getSpinnerPos(student.branchcode,getResources().getStringArray(R.array.branch_codes)));
        }
        else {
            name.setText(entrant.name);
            username.setText(entrant.username);
            //password.setText(entrant.password);
            //re_password.setText(entrant.password);
            mobile.setText(entrant.mobile);
            email.setText(entrant.email);
            fblink.setText(entrant.fb_link);
            town.setText(entrant.town);
            cb_contact.setChecked(entrant.phone_privacy);
            state.setSelection(getSpinnerPos(entrant.statecode, getResources().getStringArray(R.array.state_codes)));
            branch.setSelection(getSpinnerPos(entrant.branchcode, getResources().getStringArray(R.array.branch_codes)));
        }
    }
    private int getSpinnerPos(String item,String[] list){
        for (int i=1;i<list.length;i++)
             if (list[i].equals(item))
                 return i;

        return 0;
    }
    public boolean validate(){

        String emailPattern = "[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+";
        String mobilePattern="\\d+";
        String idPattern="\\d+";
        String namePattern="[a-zA-Z ]+";
        String townPattern="^$|^[a-zA-Z ]+$";
        String fbPattern="^$|^[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+$";
        boolean flag=true;
        if (!((params.get("email")).matches(emailPattern))){
            Toast.makeText(getContext(), "Invalid valid email address", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!((params.get("phone_no")).matches(mobilePattern))){
            Toast.makeText(getContext(),"Invalid Mobile Number", Toast.LENGTH_SHORT).show();
            flag=false;
        }
  /*      if(!((entrant.password).equals(((EditText) findViewById(R.id.re_password)).getText().toString()))){
            Toast.makeText(getApplicationContext(),"Passwords do not match", Toast.LENGTH_SHORT).show();
            flag=false;
        }*/
        if(!((params.get("town")).matches(townPattern))){
            Toast.makeText(getContext(),"Enter a proper City name", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if (!((params.get("fblink")).matches(fbPattern))){
            Toast.makeText(getContext(), "Invalid valid Facebook link", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if (state.getSelectedItemPosition()==0){
            Toast.makeText(getContext(), "Select a State", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if (branch.getSelectedItemPosition()==0){
            Toast.makeText(getContext(), "Select a State", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        return flag;
    }
    private class UpdateTask extends AsyncTask<String, Void, String>{

        @Override
        protected String doInBackground(String... args) {
            CookieManager cm= (CookieManager) CookieManager.getDefault();
            CookieStore cookieStore=cm.getCookieStore();
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/update/").openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Cookie", TextUtils.join(";", cookieStore.getCookies()));
                conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
                Uri.Builder builder = new Uri.Builder();
                for (Map.Entry<String, String> entry : params.entrySet()){
                    builder.appendQueryParameter(entry.getKey(),entry.getValue());
                }
                String query = builder.build().getEncodedQuery();
                conn.setUseCaches(false);

                OutputStream os = conn.getOutputStream();
                BufferedWriter writer = new BufferedWriter(
                        new OutputStreamWriter(os, "UTF-8"));
                writer.write(query);
                writer.flush();
                writer.close();
                os.close();

                BufferedReader reader= new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuffer buffer=new StringBuffer();
                String inputLine;
                while ((inputLine = reader.readLine()) != null)
                    buffer.append(inputLine+"\n");
                JSONObject object= new JSONObject(buffer.toString());
                if (object.has("status"))
                    return object.getString("status");
                else if (object.has("error"))
                    return object.getString("error");

            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPostExecute(String result){
            if (result.equals("success")){
                if (category.equals("entrant"))
                {

                }
                else{

                }
            }
        }
    }
}
