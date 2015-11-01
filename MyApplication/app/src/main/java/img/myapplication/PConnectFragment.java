package img.myapplication;

import android.content.Context;
import android.content.Intent;
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
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;


public class PConnectFragment extends Fragment {


    private PeerCardArrayAdapter cardArrayAdapter;
    private ListView listView;

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
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
                //viewHolder.position=position;
                //row.findViewById(R.id.cardTop).setOnClickListener(this);
                //row.setTag(viewHolder);
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
