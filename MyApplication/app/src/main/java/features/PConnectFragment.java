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

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import img.myapplication.NetworkErrorFragment;
import img.myapplication.R;
import models.PeerCardViewHolder;
import models.PeerModel;


@SuppressLint("ValidFragment")
public class PConnectFragment extends Fragment {


    private PeerCardArrayAdapter cardArrayAdapter;
    private ListView listView;
    private List<PeerModel> list = new ArrayList<PeerModel>();
    private String p_connect_url="http://192.168.121.187:8080/new_entrants/p_connect/";
    private View view;
    private String sess_id;
    public PConnectFragment(String cookie){
        this.sess_id=cookie;
    }

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        if (!isConnected()){
            getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();
        }

        view=inflater.inflate(R.layout.fragment_pconnect, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        cardArrayAdapter = new PeerCardArrayAdapter(getContext(), R.layout.list_peer_card);

        Button bt_sort= (Button) view.findViewById(R.id.bt_psort);
        bt_sort.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConnected()){
                    list.clear();
                    cardArrayAdapter.clear();
                    RadioGroup group = (RadioGroup) view.findViewById(R.id.peer_sort);
                    int bt_id = group.getCheckedRadioButtonId();
                    String url = null;
                    if (bt_id == R.id.rb_pbranch)
                        url = p_connect_url + "?sort=branch";
                    else
                        url = p_connect_url;
                    new getPeersTask().execute(url);
                }

            }
        });
        new getPeersTask().execute(p_connect_url);
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
                conn.setRequestProperty("Cookie", "CHANNELI_SESSID="+sess_id);
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
                PeerModel model= new PeerModel();
                model.name=object.getString("name");
                model.town=object.getString("hometown");
                model.state=(new JSONObject(object.getString("state"))).getString("name");
                model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                model.contact=object.getString("contact");
                model.email=object.getString("email");
                model.fblink=object.getString("fb_link");
                list.add(model);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
    private class getPeersTask extends AsyncTask<String, Void, String> {
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
    public class PeerCardArrayAdapter  extends ArrayAdapter<PeerModel> {

        public void refresh(){
            this.cardList.clear();
            this.cardList.addAll(list);
            notifyDataSetChanged();
        }

        private List<PeerModel> cardList = new ArrayList<PeerModel>();

        public PeerCardArrayAdapter(Context context, int textViewResourceId) {
            super(context, textViewResourceId);
        }

        @Override
        public void add(PeerModel object) {
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
        public PeerModel getItem(int index) {
            return this.cardList.get(index);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View row = convertView;
            PeerCardViewHolder viewHolder;
            if (row == null) {
                LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                row = inflater.inflate(R.layout.list_peer_card, parent, false);
                viewHolder = new PeerCardViewHolder();
                viewHolder.name = (TextView) row.findViewById(R.id.pname);
                viewHolder.town = (TextView) row.findViewById(R.id.ptown);
                viewHolder.state = (TextView) row.findViewById(R.id.pstate);
                viewHolder.branch= (TextView) row.findViewById(R.id.pbranch);
                //viewHolder.contact=row.findFocus(R.id.pcontact);
                //viewHolder.email=row.findViewById(R.id.pemail);
                //viewHolder.fblink=row.findViewById(R.id.pfblink);
                viewHolder.model=new PeerModel();
            } else {
                viewHolder = (PeerCardViewHolder)row.getTag();
            }
            PeerModel card = getItem(position);
            viewHolder.name.setText(card.name);
            viewHolder.town.setText(card.town);
            viewHolder.state.setText(card.state);
            viewHolder.branch.setText(card.branch);

            viewHolder.model=card;
            row.setTag(viewHolder);
            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }

}
