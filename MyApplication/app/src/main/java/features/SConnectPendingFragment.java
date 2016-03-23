package features;


import android.app.Activity;
import android.support.v4.app.Fragment;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import img.myapplication.R;
import models.SeniorCardViewHolder;
import models.SeniorModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class SConnectPendingFragment extends Fragment {

    private Map<String,String> params;
    private SeniorCardArrayAdapter cardArrayAdapter;
    private List<SeniorModel> list=new ArrayList<SeniorModel>();

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        params= (Map<String, String>) getArguments().getSerializable("userParams");
        View view=inflater.inflate(R.layout.fragment_sconnect_pending, container, false);
        ListView listView = (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        cardArrayAdapter = new SeniorCardArrayAdapter(getContext(), R.layout.list_senior_card);

        if (isConnected())
            new getSeniorsTask().execute();

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
                list.add(model);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
    private class getSeniorsTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... args) {
            try {

                HttpURLConnection conn=(HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/pending/").openConnection();
                conn.setRequestMethod("GET");
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+params.get("sess_id").toString());
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

        return null;
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

            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }


}




