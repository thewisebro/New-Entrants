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
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioGroup;
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

public class SConnectRequestFragment extends Fragment {
    private Map<String,String> rq_params=new HashMap<>();
    public Spinner list;
    public EditText query;
    public RadioGroup options;
    public String connect_url;
    private String hostURL;
    private void getURLs() {
        hostURL = getString(R.string.host);
        connect_url = hostURL + "/new_entrants/connect/";
    }
    private boolean cancelled=false;
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
        getURLs();
        setHasOptionsMenu(true);
        ((Navigation)getActivity()).setActionBarTitle("Senior Connect");
        View view= inflater.inflate(R.layout.send_request, container, false);
        cancelled=false;
        list= (Spinner) view.findViewById(R.id.list);
        ArrayAdapter adapter = ArrayAdapter.createFromResource(getContext(), R.array.states, R.layout.request_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        list.setAdapter(adapter);

        query= (EditText) view.findViewById(R.id.query);
        options= (RadioGroup) view.findViewById(R.id.options);
        options.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                int pos = group.indexOfChild(group.findViewById(checkedId));
                ArrayAdapter<CharSequence> adapter = null;
                switch (pos) {
                    case 0:
                        adapter = ArrayAdapter.createFromResource(getContext(), R.array.states, R.layout.request_spinner_item);
                        break;
                    default:
                        adapter = ArrayAdapter.createFromResource(getContext(), R.array.branches, R.layout.request_spinner_item);
                        break;
                }
                adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                list.setAdapter(adapter);
            }
        });

        Button bt= (Button) view.findViewById(R.id.send);

        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConnected()){
                    int pos=options.indexOfChild(options.findViewById(options.getCheckedRadioButtonId()));
                    int selected_pos=list.getSelectedItemPosition();
                    if (selected_pos==0){
                        Toast.makeText(getContext(), "Select a Parameter", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    String description=query.getText().toString().trim();
                    if (description.length()==0)
                        description="In Need of Assistance";
                    switch(pos){
                        case 0: rq_params.put("param", "Location");
                            rq_params.put("value", ((String[]) (getResources().getStringArray(R.array.state_codes)))[list.getSelectedItemPosition()]);
                            rq_params.put("description", description);
                            new sendRequestTask().execute();
                            break;
                        default: rq_params.put("param","Branch");
                            rq_params.put("value", ((String[]) (getResources().getStringArray(R.array.branch_codes)))[list.getSelectedItemPosition()]);
                            rq_params.put("description",description);
                            new sendRequestTask().execute();
                            break;
                    }
                }
                else
                    Toast.makeText(getContext(),"Check network connection!",Toast.LENGTH_SHORT).show();
                    //getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();
            }
        });

        return view;
    }

    private String getEntrantSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getEntrant().sess_id;
    }
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }

    private class sendRequestTask extends AsyncTask<String, Void, String> {

        ProgressDialog dialog;
        @Override
        protected void onPreExecute(){
            this.dialog=new ProgressDialog(getContext());
            this.dialog.setMessage("Sending Request...");
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
        protected String doInBackground(String... args) {
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(connect_url).openConnection();
                conn.setRequestMethod("POST");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+getEntrantSESSID());
                conn.setDoOutput(true);
                conn.setDoInput(true);

                Uri.Builder builder = new Uri.Builder();
                for (Map.Entry<String, String> entry : rq_params.entrySet()){
                    builder.appendQueryParameter(entry.getKey(),entry.getValue());
                }
                String query = builder.build().getEncodedQuery();

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
                String result=buffer.toString();
                JSONObject object=new JSONObject(buffer.toString());
                if ("success".equals(object.getString("status")))
                    return "success";
                else
                    return object.getString("error");

            } catch (Exception e) {
                e.printStackTrace();
                return "error";
            }
        }

        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (getActivity()==null)
                return;

            dialog.dismiss();

            if (result.equals("success")) {
                Toast.makeText(getContext(), "Request Sent Successfully!", Toast.LENGTH_SHORT).show();
                getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new SConnectTabFragment()).commit();
            }
            else if (result.equals("error")) {
                //getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();
                Toast.makeText(getContext(), "Unable to send request!\nCheck network connection", Toast.LENGTH_SHORT).show();
            }
            else
                Toast.makeText(getContext(),"Request failed!\n"+result,Toast.LENGTH_SHORT).show();
        }
    }
}
