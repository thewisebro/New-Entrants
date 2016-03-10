package features;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

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
import java.util.Map;

import img.myapplication.R;
import models.SeniorCardViewHolder;
import models.SeniorModel;


@SuppressLint("ValidFragment")
public class SConnectFragment extends Fragment {

    private SeniorCardArrayAdapter cardArrayAdapter;
    private Map<String,String> params;
    private List<SeniorModel> list=new ArrayList<SeniorModel>();
    private View view;
    private ListView listView;
    private final String s_connect_url="http://192.168.121.187:8080/new_entrants/s_connect/";

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        params= (Map<String, String>) getArguments().getSerializable("userParams");
        view=inflater.inflate(R.layout.fragment_sconnect, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        cardArrayAdapter = new SeniorCardArrayAdapter(getContext(), R.layout.list_senior_card);

        Button bt_sort= (Button) view.findViewById(R.id.bt_sort);
        bt_sort.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConnected()){
                    RadioGroup group= (RadioGroup) view.findViewById(R.id.group_sort);
                    int bt_id = group.getCheckedRadioButtonId();
                    String url = null;
                    if (bt_id == R.id.rb_branch)
                        url = s_connect_url + "?sort=branch&param="+params.get("branch").toString();
                    else
                        url = s_connect_url+"?sort=location&param="+params.get("state").toString();
                    new getSeniorsTask().execute(url);
                }

            }
        });
        if (isConnected())
            new getSeniorsTask().execute(s_connect_url + "?sort=location&param=" + params.get("state").toString());

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
    public String getCardList(String url){
        if (isConnected()){
            try {

                HttpURLConnection conn=(HttpURLConnection) new URL(url).openConnection();
                conn.setRequestMethod("GET");
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+params.get("sess_id"));
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                getCards(sb.toString());
                return "success";
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return null;

    }
    private void getCards(String result){
        JSONObject jObject= null;
        try {
            jObject = new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("students");
            int len=jArray.length();

            for(int i=0; i<len;i++){

                JSONObject object=jArray.getJSONObject(i);
                SeniorModel model= new SeniorModel();
                model.name=object.getString("name");
                model.town=object.getString("hometown");
                model.state=(new JSONObject(object.getString("state"))).getString("name");
                model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                model.username=object.getString("username");
                list.add(model);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
    private class getSeniorsTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... params) {

            return getCardList(params[0]);
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")){
                cardArrayAdapter.refresh();
            }
        }
    }


    public class SeniorCardArrayAdapter  extends ArrayAdapter<SeniorModel> {

        private List<SeniorModel> cardList = new ArrayList<SeniorModel>();

        public void refresh(){
            this.cardList.clear();
            this.cardList.addAll(list);
            list.clear();
            notifyDataSetChanged();
        }
        public SeniorCardArrayAdapter(Context context, int textViewResourceId) {
            super(context, textViewResourceId);
        }

        @Override
        public void add(SeniorModel object) {
            cardList.add(object);
            super.add(object);
        }

        @Override
        public int getCount() {
            return this.cardList.size();
        }

        @Override
        public SeniorModel getItem(int index) {
            return this.cardList.get(index);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View row = convertView;
            SeniorCardViewHolder viewHolder;
            if (row == null) {
                LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                row = inflater.inflate(R.layout.list_senior_card, parent, false);
                viewHolder = new SeniorCardViewHolder();
                viewHolder.name = (TextView) row.findViewById(R.id.s_name);
                viewHolder.branch = (TextView) row.findViewById(R.id.s_branch);
                viewHolder.town= (TextView) row.findViewById(R.id.s_town);
                viewHolder.state= (TextView) row.findViewById(R.id.s_state);
            } else {
                viewHolder = (SeniorCardViewHolder)row.getTag();
            }
            SeniorModel card = getItem(position);
            viewHolder.name.setText(card.name);
            viewHolder.branch.setText(card.branch);
            viewHolder.state.setText(card.state);
            viewHolder.town.setText(card.town);
            row.setTag(card.username);
            row.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    new sendRequestTask().execute(v.getTag().toString());
                }
            });
            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }
    private class sendRequestTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... args) {

            try {
                HttpURLConnection conn= (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/connect/").openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+params.get("sess_id"));

                OutputStream os = conn.getOutputStream();
                BufferedWriter writer = new BufferedWriter(
                        new OutputStreamWriter(os, "UTF-8"));
                writer.write("to="+args[0]);
                writer.flush();
                writer.close();
                os.close();

                int code=conn.getResponseCode();
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                JSONObject object=new JSONObject(sb.toString());
                return (new JSONObject(sb.toString())).getString("status");

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")){
                Toast.makeText(getActivity(), "Request sent", Toast.LENGTH_SHORT).show();
                refreshFragment();
            }
        }
    }
    public void refreshFragment(){
        getFragmentManager().beginTransaction().detach(this).attach(this).commit();
    }

}
