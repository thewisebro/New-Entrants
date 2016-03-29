package features;


import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
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

import img.myapplication.R;

public class SConnectRequestFragment extends Fragment {
    private Map<String,String> params;
    public Spinner state;
    public Spinner branch;
    public String connect_url="http://192.168.121.187:8080/new_entrants/connect/";

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_sconnect_request, container, false);
        params= (Map<String, String>) getArguments().getSerializable("userParams");
        state= (Spinner) view.findViewById(R.id.list_states);
        branch= (Spinner) view.findViewById(R.id.list_branches);
        Button request_state= (Button) view.findViewById(R.id.rq_s);
        Button request_branch= (Button) view.findViewById(R.id.rq_b);
        request_state.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new sendRequestTask("location",
                        ((String[])(getResources().getStringArray(R.array.state_codes)))[state.getSelectedItemPosition()]).execute();
            }
        });
        request_branch.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new sendRequestTask("branch",
                        ((String[])(getResources().getStringArray(R.array.branch_codes)))[state.getSelectedItemPosition()]).execute();
            }
        });

        return view;
    }

    private class sendRequestTask extends AsyncTask<String, Void, String> {
        private Map<String,String> rq_params=new HashMap<String,String>();
        public sendRequestTask(String param, String value){
            this.rq_params.put("param",param);
            this.rq_params.put("value",value);

        }
        @Override
        protected String doInBackground(String... args) {
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(connect_url).openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+params.get("sess_id"));
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

                int responseCode=conn.getResponseCode();
                BufferedReader reader= new BufferedReader(new InputStreamReader(conn.getInputStream()));
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

        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")) {
                Toast.makeText(getContext(), "Request Sent Successfully!", Toast.LENGTH_SHORT).show();
            }
        }
    }
}
