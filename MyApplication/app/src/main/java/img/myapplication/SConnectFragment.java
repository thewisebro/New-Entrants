package img.myapplication;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;


public class SConnectFragment extends Fragment {


    private SeniorCardArrayAdapter cardArrayAdapter;
    private ListView listView;

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View view=inflater.inflate(R.layout.fragment_sconnect, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        cardArrayAdapter = new SeniorCardArrayAdapter(getContext(), R.layout.list_senior_card);

        for (int i = 0; i < 10; i++) {

            SeniorModel card= new SeniorModel();
            card.name="abc";
            card.branch="ee";
            card.year="2";
            cardArrayAdapter.add(card);
        }
        listView.setAdapter(cardArrayAdapter);

        return view;
    }
    public void getCardList(){

        String result=null;
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
            result=sb.toString();
            JSONObject jObject=new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("seniors");
            for(int i=0; i<jArray.length();i++){
                try {
                    JSONObject object=jArray.getJSONObject(i);
                    SeniorModel card= new SeniorModel();
                    card.name="abc";
                    card.branch="ee";
                    card.year="2";
                    cardArrayAdapter.add(card);
                } catch (Exception e){

                }


            }
            bufferedReader.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public SeniorModel getCardfromString(String line){
        SeniorModel card=new SeniorModel();
        return card;
    }
    public class SeniorCardArrayAdapter  extends ArrayAdapter<SeniorModel> {

        private List<SeniorModel> cardList = new ArrayList<SeniorModel>();

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
                viewHolder.name = (TextView) row.findViewById(R.id.name);
                viewHolder.year = (TextView) row.findViewById(R.id.year);
                viewHolder.branch = (TextView) row.findViewById(R.id.branch);

                viewHolder.model=new SeniorModel();
            } else {
                viewHolder = (SeniorCardViewHolder)row.getTag();
            }
            SeniorModel card = getItem(position);
            viewHolder.name.setText(card.name);
            viewHolder.year.setText(card.year);
            viewHolder.branch.setText(card.branch);

            viewHolder.model.copy(card);
            row.setTag(viewHolder);
            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }

}
