package features;


import android.app.Activity;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

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

import img.myapplication.MySQLiteHelper;
import img.myapplication.NavigationStudent;
import img.myapplication.OpeningFragment;
import img.myapplication.R;
import models.StudentModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class StudentUpdateFragment extends Fragment {

    public boolean lock=false;
    private View view;
    private Spinner state;
    private EditText name;
    private EditText username;
    private EditText branch;
    private EditText town;
    private EditText mobile;
    private EditText email;
    private EditText fblink;
    private CookieManager cookieManager;
    private Map<String,String> params=new HashMap<String,String>();
    private String updateURL="http://192.168.121.187:8080/new_entrants/update/";
    private StudentModel student;
    private DrawerLayout drawer;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        view= inflater.inflate(R.layout.update_student,container,false);
        drawer= (DrawerLayout) getActivity().findViewById(R.id.drawer_layout);
        if (lock){
            drawer.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_CLOSED);

            ActionBar actionBar=((ActionBarActivity)getActivity()).getSupportActionBar();
            actionBar.setDisplayHomeAsUpEnabled(false);
        }

        setViews();
        setInitial();
        Button bt= (Button) view.findViewById(R.id.button_submit);
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConnected()) {
                    getParams();
                    if (checkParams())
                        new UpdateSubmitTask().execute();
                }
            }
        });
        return view;
    }
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }
    private void setViews(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        student=db.getStudent();
        db.close();
        name= (EditText) view.findViewById(R.id.u_name);
        username= (EditText) view.findViewById(R.id.u_username);
        town= (EditText) view.findViewById(R.id.u_town);
        branch= (EditText) view.findViewById(R.id.u_branch);
        mobile= (EditText) view.findViewById(R.id.u_mobile);
        email= (EditText) view.findViewById(R.id.u_email);
        fblink= (EditText) view.findViewById(R.id.u_fblink);
        state= (Spinner) view.findViewById(R.id.u_states);
    }
    private void setInitial(){
        name.setText(student.name);
        username.setText(student.username);
        branch.setText(student.branchname);
        mobile.setText(student.mobile);
        email.setText(student.email);
        fblink.setText(student.fb_link);
        town.setText(student.town);
        state.setSelection(getSpinnerPos(student.statecode,getResources().getStringArray(R.array.state_codes)));
    }
    public int getSpinnerPos(String state,String[] list){
        if (!state.isEmpty()){
            for (int i=1;i<list.length;i++)
                if (list[i].equals(state))
                    return i;
        }
        return 0;
    }
    private class UpdateSubmitTask extends AsyncTask<String, Void, String> {
        private ProgressDialog dialog;
        @Override
        protected void onPreExecute(){
            this.dialog=new ProgressDialog(getContext());
            this.dialog.setMessage("Updating...");
            this.dialog.setIndeterminate(false);
            this.dialog.setCancelable(false);
            this.dialog.setButton(DialogInterface.BUTTON_NEGATIVE, "CANCEL", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    cancel(true);
                }
            });
            this.dialog.show();
        }
        @Override
        protected void onCancelled(String result){
            Toast.makeText(getContext(),"Aborted!",Toast.LENGTH_SHORT).show();
            onPostExecute(result);
        }

        @Override
        protected String doInBackground(String... urls) {
            cookieManager=new CookieManager(null, CookiePolicy.ACCEPT_ALL);
            CookieHandler.setDefault(cookieManager);
            CookieStore cookieStore=cookieManager.getCookieStore();
            try {
                /*HttpURLConnection connGet= (HttpURLConnection) new URL(updateURL).openConnection();
                connGet.setRequestMethod("GET");
                connGet.setRequestProperty("Cookie","CHANNELI_SESSID="+student.sess_id);
                Object obj=connGet.getContent();
                //String csrftoken=cookieStore.getCookies().get(0).getValue();*/

                HttpURLConnection connPost= (HttpURLConnection) new URL(updateURL).openConnection();
                connPost.setRequestMethod("POST");
                connPost.setDoInput(true);
                connPost.setDoOutput(true);
                connPost.setRequestProperty("Cookie", "CHANNELI_SESSID=" + student.sess_id);
                //connPost.setRequestProperty("Cookie", "CHANNELI_SESSID=" + student.sess_id + ";csrftoken=" + csrftoken);
                //getParams();
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
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")){
                student.email=params.get("email");
                student.statecode=params.get("state");
                student.state=state.getSelectedItem().toString();
                student.town=params.get("hometown");
                student.mobile=params.get("phone_no");
                student.fb_link=params.get("fb_link");

                MySQLiteHelper db=new MySQLiteHelper(getContext());
                db.deleteStudent();
                db.addStudent(student);
                db.close();
                if (lock) {
                    drawer.setDrawerLockMode(DrawerLayout.LOCK_MODE_LOCKED_OPEN);
                    getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new OpeningFragment()).commit();
                    lock=false;
                }
                ((NavigationStudent)getActivity()).set_updated();
                Toast.makeText(getContext(), "Profile Updated", Toast.LENGTH_SHORT).show();

                //startActivity(new Intent(getContext(), NavigationStudent.class));
                //getActivity().finish();
            }
            else {
                Toast.makeText(getContext(), "Update failed!", Toast.LENGTH_SHORT).show();
            }
            dialog.dismiss();
        }
    }
    public void getParams(){
        params.put("email",email.getText().toString().trim());
        params.put("state",(getResources().getStringArray(R.array.state_codes))[state.getSelectedItemPosition()]);
        params.put("fb_link",fblink.getText().toString().trim());
        params.put("phone_no",mobile.getText().toString().trim());
        params.put("hometown",town.getText().toString().trim());
    }
    public boolean checkParams(){
        String emailPattern="^(([^<>()\\[\\]\\\\.,;:\\s@\"]+(\\.[^<>()\\[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$";
        //String mobilePattern="^(\\+91|0|)[0-9]{10}$";
        String mobilePattern="^$|^(\\+\\d{1,3}[- ]?)?\\d{10}$";
        //String namePattern="[a-zA-Z ]+";
        String namePattern="^[a-zA-Z ]{1,100}$";
        String usernamePattern="^[0-9a-zA-Z]{1,30}$";
        String townPattern="^$|^[a-zA-Z ]+$";
        String fbPattern="^$|^(([^<>()\\[\\]\\\\.,;:\\s@\"]+(\\.[^<>()\\[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$";

        boolean flag=true;
        if (!(params.get("email").toString()).matches(emailPattern)){
            Toast.makeText(getContext(), "Invalid valid email address", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(params.get("phone_no").toString()).matches(mobilePattern)){
            Toast.makeText(getContext(),"Invalid Mobile Number", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if(!(params.get("hometown").toString()).matches(townPattern)){
            Toast.makeText(getContext(),"Enter a proper City name", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if (!(params.get("fb_link").toString()).matches(fbPattern)){
            Toast.makeText(getContext(), "Invalid valid Facebook link", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        if (state.getSelectedItemPosition()==0){
            Toast.makeText(getContext(), "Select a State", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        return flag;
    }

}
