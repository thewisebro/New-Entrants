package features;


import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import img.myapplication.MySQLiteHelper;
import img.myapplication.R;
import models.RequestCardViewHolder;
import models.RequestModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class SConnectPendingFragment extends Fragment {

    private SeniorCardArrayAdapter cardArrayAdapter;
    private MySQLiteHelper db;
    public String extend_url;
    private TextView zerocount;
    private String hostURL;
    private void getURLs() {
        hostURL = getString(R.string.host);
        extend_url = hostURL + "/new_entrants/extend/";
    }
    private boolean cancelled;
    @Override
    public void onDestroyView(){
        cancelled=true;
        super.onDestroyView();
    }
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        getURLs();
        cancelled=false;
        db= new MySQLiteHelper(getContext());
        View view=inflater.inflate(R.layout.fragment_sconnect_pending, container, false);
        ListView listView = (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));
        zerocount= (TextView) view.findViewById(R.id.zerocount);
        cardArrayAdapter = new SeniorCardArrayAdapter(getContext(), R.layout.request_card);

        cardArrayAdapter.refresh();
        listView.setAdapter(cardArrayAdapter);

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

    private String getEntrantSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getEntrant().sess_id;
    }


    public class SeniorCardArrayAdapter  extends ArrayAdapter<RequestModel> {

        private List<RequestModel> cardList = new ArrayList<RequestModel>();

        public void refresh(){
            this.cardList.clear();
            this.cardList.addAll(db.getRequests());
            notifyDataSetChanged();
            if (getCount()==0)
                zerocount.setVisibility(View.VISIBLE);
            else
                zerocount.setVisibility(View.GONE);
        }
        public SeniorCardArrayAdapter(Context context, int textViewResourceId) {
            super(context, textViewResourceId);
        }

        @Override
        public void add(RequestModel object) {
            cardList.add(object);
            super.add(object);
        }

        @Override
        public int getCount() {
            return this.cardList.size();
        }

        @Override
        public RequestModel getItem(int index) {
            return this.cardList.get(index);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View row = convertView;
            RequestCardViewHolder viewHolder;
            if (row == null) {
                LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                row = inflater.inflate(R.layout.request_card, parent, false);
                viewHolder = new RequestCardViewHolder();
                viewHolder.param= (TextView) row.findViewById(R.id.param);
                viewHolder.accepted= (TextView) row.findViewById(R.id.accepted);
                viewHolder.value= (TextView) row.findViewById(R.id.value);
                viewHolder.date= (TextView) row.findViewById(R.id.date);
                viewHolder.query= (TextView) row.findViewById(R.id.query);
            } else {
                viewHolder = (RequestCardViewHolder)row.getTag();
            }
            RequestModel card = getItem(position);
            viewHolder.param.setText(card.param);
            viewHolder.accepted.setText(String.valueOf(card.accepted));
            viewHolder.value.setText(card.value);
            viewHolder.query.setText(card.query);
            viewHolder.date.setText(card.date);
            ((TextView)row.findViewById(R.id.request_no)).setText(String.valueOf(card.request_no));
            if (card.more){
                TextView more= (TextView) row.findViewById(R.id.more);
                more.setTag(card.id);
                more.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        new SendMoreRequests().execute(getTag().toString());
                    }
                });
            }
            else{
                TextView more= (TextView) row.findViewById(R.id.more);
                more.setAlpha(0.4F);
            }
            row.setTag(viewHolder);
            return row;
        }

    }
    private class SendMoreRequests extends AsyncTask<String, Void, String> {
        private ProgressDialog dialog;

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
                }
            });
            this.dialog.show();
        }
        @Override
        protected void onCancelled(String result){
            if (!cancelled) {
                Toast.makeText(getContext(), "Aborted!", Toast.LENGTH_LONG).show();
                dialog.dismiss();
            }
        }
        @Override
        protected String doInBackground(String... args) {
            try {
                HttpURLConnection conn = (HttpURLConnection) new URL(extend_url).openConnection();
                conn.setRequestMethod("POST");
                conn.setConnectTimeout(7000);
                conn.setReadTimeout(5000);
                conn.setRequestProperty("Cookie", "CHANNELI_SESSID=" + getEntrantSESSID());

                OutputStream os = conn.getOutputStream();
                BufferedWriter writer = new BufferedWriter(
                        new OutputStreamWriter(os, "UTF-8"));
                writer.write("id=" + args[0]);
                writer.flush();
                writer.close();
                os.close();

                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder sb = new StringBuilder();
                String line = "";
                while ((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                JSONObject result=new JSONObject(sb.toString());
                return result.getString("status");
            } catch (Exception e) {
                e.printStackTrace();
                return "error";
            }
        }
        @Override
        protected void onPostExecute(String result){
            if (result.equals("success")){
                Toast.makeText(getContext(), "Request Sent Successfully!", Toast.LENGTH_SHORT).show();
            }
            else if (result.equals("error")){
                Toast.makeText(getContext(), "Unable to send request!\nCheck network connection", Toast.LENGTH_SHORT).show();
            }
            else
                Toast.makeText(getContext(), "Request failed!", Toast.LENGTH_SHORT).show();
            dialog.dismiss();
        }
    }
}