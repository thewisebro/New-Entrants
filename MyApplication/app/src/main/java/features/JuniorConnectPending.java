package features;


import android.animation.LayoutTransition;
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
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import org.json.JSONArray;
import org.json.JSONException;
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

import img.myapplication.NetworkErrorFragment;
import img.myapplication.R;
import models.JuniorCardViewHolder;
import models.JuniorModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class JuniorConnectPending extends Fragment {

    private JuniorCardArrayAdapter cardArrayAdapter;
    private ListView listView;
    private String sess_id;
    private List<JuniorModel> list=new ArrayList<JuniorModel>();
    private String pendingURL="http://192.168.121.187:8080/new_entrants/pending/";
    private TextView zerocount;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_junior_connect_pending, container, false);
        sess_id=getArguments().getString("sess_id");
        listView= (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));
        cardArrayAdapter = new JuniorCardArrayAdapter(getContext(), R.layout.pending_card);
        zerocount= (TextView) view.findViewById(R.id.zerocount);
        if (isConnected()){
            new getPendingTask().execute(sess_id);
        }
        else
            getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();

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
    private class getPendingTask extends AsyncTask<String, Void, String> {
        private ProgressDialog dialog;
        @Override
        protected void onPreExecute(){
            this.dialog=new ProgressDialog(getContext());
            this.dialog.setMessage("Loading...");
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
            Toast.makeText(getContext(),"Loading aborted!",Toast.LENGTH_LONG).show();
            cardArrayAdapter.refresh();
            dialog.dismiss();
        }
        @Override
        protected String doInBackground(String... params) {

            try {

                HttpURLConnection conn=(HttpURLConnection) new URL(pendingURL).openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie", "CHANNELI_SESSID="+params[0]);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                getCards(sb.toString());
                return "success";
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            dialog.dismiss();
            if (result==null){
                getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();
                Toast.makeText(getContext(), "Unable to load!", Toast.LENGTH_SHORT).show();
            }
            else if (result.equals("success")){
                cardArrayAdapter.refresh();
            }

        }
    }
    private void getCards(String result){
        JSONObject jObject= null;
        try {
            jObject = new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("requests");
            int len=jArray.length();

            for(int i=0; i<len;i++){

                JSONObject object=jArray.getJSONObject(i);
                JuniorModel model= new JuniorModel();
                model.name=object.getString("name");
                model.town=object.getString("hometown");
                model.state=(new JSONObject(object.getString("state"))).getString("name");
                model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                model.username=object.getString("username");
                model.description=object.getString("description");
                list.add(model);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
    public class JuniorCardArrayAdapter  extends ArrayAdapter<JuniorModel> {

        public void refresh(){
            this.cardList.clear();
            this.cardList.addAll(list);
            list.clear();
            notifyDataSetChanged();
            if (getCount()==0)
                zerocount.setVisibility(View.VISIBLE);
            else
                zerocount.setVisibility(View.GONE);
        }

        private List<JuniorModel> cardList = new ArrayList<JuniorModel>();

        public JuniorCardArrayAdapter(Context context, int textViewResourceId) {
            super(context, textViewResourceId);
        }

        @Override
        public void add(JuniorModel object) {
            cardList.add(object);
            super.add(object);
        }
        public void clear(){
            cardList.clear();
            super.clear();
            notifyDataSetChanged();
        }

        @Override
        public int getCount() {
            return this.cardList.size();
        }

        @Override
        public JuniorModel getItem(int index) {
            return this.cardList.get(index);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View row = convertView;
            JuniorCardViewHolder viewHolder;
            if (row == null) {
                LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                row = inflater.inflate(R.layout.pending_card, parent, false);
                viewHolder = new JuniorCardViewHolder();
                viewHolder.name = (TextView) row.findViewById(R.id.j_name);
                viewHolder.town = (TextView) row.findViewById(R.id.j_town);
                viewHolder.state = (TextView) row.findViewById(R.id.j_state);
                viewHolder.branch= (TextView) row.findViewById(R.id.j_branch);
                viewHolder.query= (TextView) row.findViewById(R.id.j_query);
            } else {
                viewHolder = (JuniorCardViewHolder)row.getTag();
            }
            JuniorModel card = getItem(position);
            viewHolder.name.setText(card.name);
            if (!("".equals(card.town)))
                viewHolder.town.setText(card.town+", ");
            viewHolder.state.setText(card.state);
            if ("".equals(card.branch))
                viewHolder.branch.setVisibility(View.GONE);
            else {
                viewHolder.branch.setVisibility(View.VISIBLE);
                viewHolder.branch.setText(card.branch);
            }
            if ("".equals(card.description))
                viewHolder.query.setText("In need of Assistance");
            else
                viewHolder.query.setText(card.description);
            ToggleButton bt= (ToggleButton) row.findViewById(R.id.toggle_junior);
            bt.setVisibility(View.VISIBLE);
            bt.setTag(row.findViewById(R.id.card_layout));
            bt.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    LinearLayout layout = (LinearLayout) buttonView.getTag();
                    if (isChecked) {
                        ((LinearLayout) layout.findViewById(R.id.down_view)).setVisibility(View.VISIBLE);
                        layout.setLayoutTransition(null);
                    } else {
                        ((LinearLayout) layout.findViewById(R.id.down_view)).setVisibility(View.GONE);
                        layout.setLayoutTransition(new LayoutTransition());
                    }
                }
            });
            TextView connect = (TextView) row.findViewById(R.id.connect);
            connect.setTag(card.username);
            connect.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    new AcceptRequestTask().execute(v.getTag().toString());
                }
            });
            row.setTag(viewHolder);
            return row;
        }

    }
    private class AcceptRequestTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... args) {

            try {
                HttpURLConnection conn = (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/accept/").openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Cookie", "CHANNELI_SESSID=" + sess_id);
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                OutputStream os = conn.getOutputStream();
                BufferedWriter writer = new BufferedWriter(
                        new OutputStreamWriter(os, "UTF-8"));
                writer.write("from=" + args[0]);
                writer.flush();
                writer.close();
                os.close();

                int code = conn.getResponseCode();
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder sb = new StringBuilder();
                String line = "";
                while ((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                JSONObject object = new JSONObject(sb.toString());
                return (new JSONObject(sb.toString())).getString("status");

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")) {
                Toast.makeText(getActivity(), "Accepted Request", Toast.LENGTH_SHORT).show();
                refreshFragment();
            }
            else
                getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();

        }
    }
    public void refreshFragment(){
        getFragmentManager().beginTransaction().detach(this).attach(this).commit();
    }
}
