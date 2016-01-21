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

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;


public class RequestsFragment extends Fragment {


    private RequestCardArrayAdapter cardArrayAdapter;
    private ListView listView;

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View view=inflater.inflate(R.layout.fragment_requests, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        cardArrayAdapter = new RequestCardArrayAdapter(getContext(), R.layout.list_requests);

        for (int i = 0; i < 10; i++) {

            NewEntrantModel card= new NewEntrantModel();
            card.name="abc";
            card.state="utk";
            card.town="roorkee";
            cardArrayAdapter.add(card);
        }
        listView.setAdapter(cardArrayAdapter);

        return view;
    }
    public void getCardList(){


        try {
            URL url= null;
            url = new URL("www.google.com");
            HttpURLConnection conn=(HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setDoInput(true);
            BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
            String line = "";
            while((line = bufferedReader.readLine()) != null)
                cardArrayAdapter.add(getCardfromString(line));
            bufferedReader.close();
        } catch (Exception e) {
            e.printStackTrace();
        }


    }
    public NewEntrantModel getCardfromString(String line){
        NewEntrantModel card=new NewEntrantModel();
        return card;
    }
    public class RequestCardArrayAdapter  extends ArrayAdapter<NewEntrantModel> {

        private List<NewEntrantModel> cardList = new ArrayList<NewEntrantModel>();

        public RequestCardArrayAdapter(Context context, int textViewResourceId) {
            super(context, textViewResourceId);
        }

        @Override
        public void add(NewEntrantModel object) {
            cardList.add(object);
            super.add(object);
        }

        @Override
        public int getCount() {
            return this.cardList.size();
        }

        @Override
        public NewEntrantModel getItem(int index) {
            return this.cardList.get(index);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View row = convertView;
            RequestCardViewHolder viewHolder;
            if (row == null) {
                LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                row = inflater.inflate(R.layout.list_requests, parent, false);
                viewHolder = new RequestCardViewHolder();
                viewHolder.name = (TextView) row.findViewById(R.id.name);
                viewHolder.town = (TextView) row.findViewById(R.id.town);
                viewHolder.state = (TextView) row.findViewById(R.id.state);


            } else {
                viewHolder = (RequestCardViewHolder)row.getTag();
            }
            NewEntrantModel card = getItem(position);
            viewHolder.name.setText(card.name);
            viewHolder.town.setText(card.town);
            viewHolder.state.setText(card.state);

            viewHolder.model=card;
            row.setTag(viewHolder);
            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }

}
