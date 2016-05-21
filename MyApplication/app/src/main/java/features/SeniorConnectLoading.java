package features;


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
import img.myapplication.Navigation;
import img.myapplication.R;
import models.RequestModel;
import models.SeniorModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class SeniorConnectLoading extends Fragment {

    private MySQLiteHelper db;
    private String acceptedURL;
    private String hostURL;
    private String request_url;

    private void getURLs() {
        hostURL = getString(R.string.host);
        String appURL=getString(R.string.app);
        acceptedURL = appURL + "/accepted/";
        request_url = appURL + "/pending/";
    }
    private boolean cancelled;
    @Override
    public void onDestroyView(){
        cancelled=true;
        super.onDestroyView();
    }
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        menu.clear();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ((Navigation)getActivity()).setActionBarTitle("Senior Connect");
        setHasOptionsMenu(true);
        getURLs();
        cancelled=false;
        db=new MySQLiteHelper(getContext());
        View view = inflater.inflate(R.layout.blank, container, false);
        if (isConnected())
            new UpdateSeniorsTask().execute();
        else
            loadTabs();
        return view;
    }
    public boolean isConnected() {
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }

    private String getEntrantSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getEntrant().sess_id;
    }
    private void loadTabs(){
        getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new SConnectTabFragment()).commit();
    }
    private class UpdateSeniorsTask extends AsyncTask<String, Void, String> {
        private ProgressDialog dialog;
        @Override
        protected void onPreExecute(){
            this.dialog=new ProgressDialog(getContext());
            this.dialog.setMessage("Updating Seniors List...");
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

        private String acceptedSeniors(){
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(acceptedURL).openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+getEntrantSESSID());
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');

                JSONObject jObject=new JSONObject(sb.toString());
                if ("success".equals(jObject.getString("status"))){
                    JSONArray jArray=jObject.getJSONArray("students");
                    int len=jArray.length();
                    db.deleteSeniors();
                    for(int i=0; i<len;i++){
                        JSONObject object=jArray.getJSONObject(i);
                        SeniorModel model= new SeniorModel();
                        model.name=object.getString("name");
                        model.town=object.getString("hometown");
                        model.state=(new JSONObject(object.getString("state"))).getString("name");
                        model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                        model.fblink=object.getString("fb_link");
                        model.contact=object.getString("contact");
                        model.email=object.getString("email");
                        model.dp_link=object.getString("dp_link");
                        model.year=object.getInt("year");
                        db.addSenior(model);
                    }
                    return "success";
                }
                else
                    return "fail";
            } catch (JSONException e){
                return "fail";
            } catch (Exception e) {
                return "error";
            }
        }
        private String pendingRequests(){
            try {
                HttpURLConnection conn=(HttpURLConnection) new URL(request_url).openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+getEntrantSESSID());
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                JSONObject jObject = new JSONObject(sb.toString());
                if ("success".equals(jObject.getString("status"))){
                    JSONArray jArray=jObject.getJSONArray("requests");
                    int len=jArray.length();
                    db.deleteRequests();
                    for(int i=0; i<len;i++){

                        JSONObject object=jArray.getJSONObject(i);
                        RequestModel model=new RequestModel();
                        model.value=object.getString("value");
                        model.accepted=object.getInt("accepted");
                        model.id=object.getInt("id");
                        model.param=object.getString("param");
                        model.more=object.getBoolean("more");
                        model.allowed=object.getInt("allowed");
                        model.query=object.getString("description");
                        model.date=object.getString("date");
                        model.request_no=i+1;
                        db.addRequest(model);
                    }
                    return "success";
                }
                else
                    return "fail";
            } catch (JSONException e) {
                e.printStackTrace();
                return "fail";
            }catch (Exception e) {
                e.printStackTrace();
                return "error";
            }
        }

        @Override
        protected String doInBackground(String... args) {
            String result1=acceptedSeniors();
            String result2=pendingRequests();
            if ("success".equals(result1))
                return result2;
            else
                return result1;
        }

        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {

            dialog.dismiss();
            if (result.equals("success")) {
                //Toast.makeText(getContext(), "List Updated!", Toast.LENGTH_SHORT).show();
            }
            else if (result.equals("error")){
                //getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();
                Toast.makeText(getContext(), "Unable to update!\nCheck network connection", Toast.LENGTH_SHORT).show();
            }
            else
                Toast.makeText(getContext(), "Sorry! Unable to update", Toast.LENGTH_SHORT).show();

            loadTabs();
        }
    }

}
