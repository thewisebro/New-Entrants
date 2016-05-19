package features;


import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import img.myapplication.MySQLiteHelper;
import img.myapplication.NavigationStudent;
import img.myapplication.R;
import models.JuniorModel;

/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class JuniorConnectLoading extends Fragment {

    private MySQLiteHelper db;
    private boolean cancelled=false;
    private String hostURL;
    private String pendingURL;
    private String acceptedURL;

    private void getURLs() {
        hostURL = getString(R.string.host);
        pendingURL = hostURL + "/new_entrants/pending/";
        acceptedURL = hostURL + "/new_entrants/accepted/";
    }

    @Override
    public void onDestroyView(){
        cancelled=true;
        super.onDestroyView();
    }
    @Override
    public void onCreate (Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        db=new MySQLiteHelper(getContext());
        cancelled=false;
        getURLs();
    }
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        menu.clear();
        inflater.inflate(R.menu.menu_connect, menu);
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ((NavigationStudent)getActivity()).setActionBarTitle("Junior Connect");
        setHasOptionsMenu(true);
        View view= inflater.inflate(R.layout.blank, container, false);

        if (isConnected())
            new updateTask().execute(getStudentSESSID());
        else
            loadTabs();
        return view;
    }
    private void loadTabs(){
        getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new JuniorConnect()).commit();
    }
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }

    private String getStudentSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getStudent().sess_id;
    }
    private class updateTask extends AsyncTask<String, Void, String> {
        private ProgressDialog dialog;

        @Override
        protected void onPreExecute(){
            this.dialog=new ProgressDialog(getContext());
            this.dialog.setMessage("Updating Juniors List...");
            this.dialog.setIndeterminate(false);
            this.dialog.setCancelable(false);
            this.dialog.setButton(DialogInterface.BUTTON_NEGATIVE, "CANCEL", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    cancel(true);
                    loadTabs();
                }
            });
            this.dialog.show();
        }

        private String acceptedJuniors(String sess_id){
            try {
                HttpURLConnection conn=(HttpURLConnection) new URL(acceptedURL).openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie", "CHANNELI_SESSID="+sess_id);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                return getAcceptedCards(sb.toString());
            } catch (Exception e) {
                e.printStackTrace();
                return "error";
            }
        }
        private String pendingJuniors(String sess_id){
            try {
                HttpURLConnection conn=(HttpURLConnection) new URL(pendingURL).openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie", "CHANNELI_SESSID="+sess_id);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                return getPendingCards(sb.toString());
            } catch (Exception e) {
                e.printStackTrace();
                return "error";
            }
        }
        @Override
        protected String doInBackground(String... params) {

            String result1=acceptedJuniors(params[0]);
            String result2=pendingJuniors(params[0]);
            if ("success".equals(result1))
                return result2;
            else
                return result1;
        }
        @Override
        protected void onPostExecute(String result) {

            if (getActivity()==null)
                return;

            dialog.dismiss();
            if (result.equals("success")){
                //Toast.makeText(getContext(), "List Updated", Toast.LENGTH_SHORT).show();
            }
            else if (result.equals("error")){
                Toast.makeText(getContext(), "Unable to Update!\nCheck network connection", Toast.LENGTH_SHORT).show();
            }
            else
                Toast.makeText(getContext(), "Sorry! Unable to update!", Toast.LENGTH_SHORT).show();

            loadTabs();
            }

    }
    private String getAcceptedCards(String result){

        try {
            JSONObject jObject = new JSONObject(result);
            if ("success".equals(jObject.getString("status"))){
                JSONArray jArray=jObject.getJSONArray("students");
                int len=jArray.length();
                db.deleteAcceptedJuniors();
                for(int i=0; i<len;i++){
                    JSONObject object=jArray.getJSONObject(i);
                    JuniorModel model= new JuniorModel();
                    model.name=object.getString("name");
                    model.town=object.getString("hometown");
                    model.state=(new JSONObject(object.getString("state"))).getString("name");
                    model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                    model.fblink=object.getString("fb_link");
                    model.mobile=object.getString("contact");
                    model.email=object.getString("email");
                    model.status="accepted";
                    db.addJunior(model);
                }
                return "success";
            }
            else
                return "fail";
        } catch (JSONException e) {
            e.printStackTrace();
            return "fail";
        }
    }
    private String getPendingCards(String result){

        try {
            JSONObject jObject = new JSONObject(result);
            if ("success".equals(jObject.getString("status"))){
                JSONArray jArray=jObject.getJSONArray("requests");
                int len=jArray.length();
                db.deletePendingJuniors();
                for(int i=0; i<len;i++){

                    JSONObject object=jArray.getJSONObject(i);
                    JuniorModel model= new JuniorModel();
                    model.name=object.getString("name");
                    model.town=object.getString("hometown");
                    model.state=(new JSONObject(object.getString("state"))).getString("name");
                    model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                    model.username=object.getString("username");
                    model.description=object.getString("description");
                    model.status="pending";
                    db.addJunior(model);
                }
                return "success";
            }
            else
                return "fail";
        } catch (JSONException e) {
            e.printStackTrace();
            return "fail";
        }
    }


}
