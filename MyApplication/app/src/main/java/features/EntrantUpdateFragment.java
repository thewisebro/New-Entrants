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
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import img.myapplication.MySQLiteHelper;
import img.myapplication.Navigation;
import img.myapplication.R;
import models.NewEntrantModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class EntrantUpdateFragment extends Fragment {

    private NewEntrantModel entrant;
    private Map<String,String> params=new HashMap<String,String>();
    private View view;
    private EditText name;
    private EditText username;
    private EditText town;
    private Spinner branch;
    private EditText mobile;
    private EditText email;
    private EditText fblink;
    private Spinner state;
    private CheckBox visibility;
    private String updateURL;
    private String hostURL;
    private void getURLs(){
        this.hostURL=getString(R.string.host);
        String appURL=getString(R.string.app);
        this.updateURL=appURL+"/j_update/";
    }
    private boolean cancelled=false;
    @Override
    public void onDestroyView(){
        cancelled=true;
        super.onDestroyView();
    }
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater){
        menu.clear();
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        setHasOptionsMenu(true);
        getURLs();
        ((Navigation) getActivity()).getSupportActionBar().show();
        ((Navigation)getActivity()).setActionBarTitle(getString(R.string.title_profile));
        cancelled=false;
        view= inflater.inflate(R.layout.update_entrant,container,false);
        setViews();
        setInitial();
        Button bt= (Button) view.findViewById(R.id.bt_update);
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConnected()) {
                    getParams();
                    if (checkParams())
                        new UpdateSubmitTask().execute();
                } else
                    Toast.makeText(getContext(), "Check network connection", Toast.LENGTH_SHORT).show();
                //getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();

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
        name= (EditText) view.findViewById(R.id.u_name);
        username= (EditText) view.findViewById(R.id.u_username);
        town= (EditText) view.findViewById(R.id.u_town);
        branch= (Spinner) view.findViewById(R.id.u_branches);
        mobile= (EditText) view.findViewById(R.id.u_mobile);
        email= (EditText) view.findViewById(R.id.u_email);
        fblink= (EditText) view.findViewById(R.id.u_fblink);
        state= (Spinner) view.findViewById(R.id.u_states);
        visibility= (CheckBox) view.findViewById(R.id.u_contact_visibility);
    }
    private void setInitial(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        entrant=db.getEntrant();
        db.close();
        name.setText(entrant.name);
        username.setText(entrant.username);
        branch.setSelection(getSpinnerPos(entrant.branchcode, getResources().getStringArray(R.array.branch_codes)));
        mobile.setText(entrant.mobile);
        email.setText(entrant.email);
        fblink.setText(entrant.fb_link);
        town.setText(entrant.town);
        state.setSelection(getSpinnerPos(entrant.statecode, getResources().getStringArray(R.array.state_codes)));
        visibility.setChecked(entrant.phone_privacy);
    }
    public int getSpinnerPos(String state,String[] list){

        if (state!=null)
            if (!state.isEmpty())
                for (int i=1;i<list.length;i++)
                    if (list[i].equals(state))
                        return i;

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
                    dialog.dismiss();
                }
            });
            this.dialog.show();
        }
        @Override
        protected void onCancelled(String result){
            if (!cancelled) {
                onPostExecute(result);
            }
        }

        @Override
        protected String doInBackground(String... urls) {
            try {
                HttpURLConnection connPost= (HttpURLConnection) new URL(updateURL).openConnection();
                connPost.setRequestMethod("POST");
                connPost.setConnectTimeout(7000);
                connPost.setReadTimeout(7000);
                connPost.setDoInput(true);
                connPost.setDoOutput(true);
                String cookieHeader="CHANNELI_SESSID="+entrant.sess_id;
                cookieHeader+=";CHANNELI_DEVICE="+"android";
                connPost.setRequestProperty("Cookie", cookieHeader);
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
                return null;
            }
        }
        @Override
        protected void onPostExecute(String result) {

            if (getActivity()==null)
                return;

            dialog.dismiss();
            if (result==null){
                Toast.makeText(getContext(), "Update failed! Check network connection", Toast.LENGTH_SHORT).show();
                //getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();
            }
            else if (result.equals("success")){
                entrant.email=params.get("email");
                entrant.state=state.getSelectedItem().toString();
                entrant.statecode=params.get("state");
                entrant.town=params.get("hometown");
                entrant.mobile=params.get("phone_no");
                entrant.fb_link=params.get("fb_link");
                entrant.branchcode=params.get("branch");
                entrant.branchname=branch.getSelectedItem().toString();
                entrant.phone_privacy=visibility.isChecked();

                MySQLiteHelper db=new MySQLiteHelper(getContext());
                db.deleteEntrant();
                db.addEntrant(entrant);
                db.close();
                ((Navigation)getActivity()).set_updated();
                Toast.makeText(getContext(), "Profile Updated", Toast.LENGTH_SHORT).show();
            }
            else
                Toast.makeText(getContext(), "Sorry! Update failed!", Toast.LENGTH_SHORT).show();
        }
    }
    public void getParams(){
        params.put("email", email.getText().toString().trim());
        params.put("state", (getResources().getStringArray(R.array.state_codes))[state.getSelectedItemPosition()]);
        params.put("fb_link", fblink.getText().toString().trim());
        params.put("phone_no", mobile.getText().toString().trim());
        params.put("hometown", town.getText().toString().trim());
        params.put("branch",(getResources().getStringArray(R.array.branch_codes))[branch.getSelectedItemPosition()]);
        if (visibility.isChecked())
            params.put("phone_privacy","on");
        params.put("droid","True");
    }
    public boolean checkParams(){
        String emailPattern="^(([^<>()\\[\\]\\\\.,;:\\s@\"]+(\\.[^<>()\\[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$";
        String mobilePattern="^$|^(\\+\\d{1,3}[- ]?)?\\d{10}$";
        String townPattern="^$|^[a-zA-Z ]+$";
        String fbPattern="^$|^(https?:\\/\\/)?([\\da-z\\.-]+)\\.([a-z\\.]{2,6})([\\/\\w \\.-]*)*\\/?$";

        boolean flag=true;
        if (!(params.get("email").toString()).matches(emailPattern)){
            email.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getContext(), "Invalid email address", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            email.setBackgroundDrawable(null);
        if(!(params.get("phone_no").toString()).matches(mobilePattern)){
            mobile.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getContext(),"Invalid Mobile Number", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            mobile.setBackgroundDrawable(null);
        if(!(params.get("hometown").toString()).matches(townPattern)){
            town.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getContext(),"Enter a proper City name", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            town.setBackgroundDrawable(null);
        if (!(params.get("fb_link").toString()).matches(fbPattern)){
            fblink.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getContext(), "Invalid Facebook link", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            fblink.setBackgroundDrawable(null);
        if (state.getSelectedItemPosition()==0){
            state.setBackgroundDrawable(getResources().getDrawable(R.drawable.highlight));
            Toast.makeText(getContext(), "Select a State", Toast.LENGTH_SHORT).show();
            flag=false;
        }
        else
            state.setBackgroundDrawable(null);
        return flag;
    }
}
