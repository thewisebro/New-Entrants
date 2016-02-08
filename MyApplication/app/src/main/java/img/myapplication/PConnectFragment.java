package img.myapplication;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v4.app.Fragment;
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


public class PConnectFragment extends Fragment {


    private PeerCardArrayAdapter cardArrayAdapter;
    private ListView listView;

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        if (!isConnected()){
            getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();
        }

        View view=inflater.inflate(R.layout.fragment_pconnect, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        cardArrayAdapter = new PeerCardArrayAdapter(getContext(), R.layout.list_peer_card);

        for (int i = 0; i < 10; i++) {

            PeerModel card= new PeerModel();
            card.name="abc";
            card.state="utk";
            card.town="roorkee";
            cardArrayAdapter.add(card);
        }
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
    public void getCardList(){
        if (isConnected()){
            try {
                URL url= null;
                url = new URL("www.google.com");
                HttpURLConnection conn=(HttpURLConnection) url.openConnection();
                conn.setDoOutput(true);
                conn.setDoInput(true);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                String result=sb.toString();
                cardsFromString(result);
/*
                FileOutputStream fos = getContext().openFileOutput("peers.txt",Context.MODE_PRIVATE);
                fos.write(result.getBytes());
                fos.close();
                bufferedReader.close();
                */
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        else {
            /*
            try {
                FileInputStream fis;
                fis = getContext().openFileInput("peers.txt");
                StringBuffer fileContent = new StringBuffer("");

                byte[] buffer = new byte[1024];
                int n;
                while ((n = fis.read(buffer)) != -1)
                {
                    fileContent.append(new String(buffer, 0, n));
                }
                String blogString=fileContent.toString();
                cardsFromString(blogString);
            } catch (java.io.IOException e) {
                e.printStackTrace();
            }
            */
        }
    }
    private void cardsFromString(String result){
        JSONObject jObject= null;
        try {
            jObject = new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("blogs");

            for(int i=0; i<jArray.length();i++){

                JSONObject object=jArray.getJSONObject(i);
                PeerModel model= new PeerModel();
                model.name="abc";
                model.state="utk";
                model.town="roorkee";
                cardArrayAdapter.add(model);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }


    }
    public class PeerCardArrayAdapter  extends ArrayAdapter<PeerModel> {

        private List<PeerModel> cardList = new ArrayList<PeerModel>();

        public PeerCardArrayAdapter(Context context, int textViewResourceId) {
            super(context, textViewResourceId);
        }

        @Override
        public void add(PeerModel object) {
            cardList.add(object);
            super.add(object);
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
                viewHolder.name = (TextView) row.findViewById(R.id.name);
                viewHolder.town = (TextView) row.findViewById(R.id.town);
                viewHolder.state = (TextView) row.findViewById(R.id.state);

                viewHolder.model=new PeerModel();
            } else {
                viewHolder = (PeerCardViewHolder)row.getTag();
            }
            PeerModel card = getItem(position);
            viewHolder.name.setText(card.name);
            viewHolder.town.setText(card.town);
            viewHolder.state.setText(card.state);

            viewHolder.model.copy(card);
            row.setTag(viewHolder);
            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }

}
