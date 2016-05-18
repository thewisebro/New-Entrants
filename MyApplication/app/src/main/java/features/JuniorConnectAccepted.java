package features;

import android.animation.LayoutTransition;
import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.ToggleButton;

import java.util.ArrayList;
import java.util.List;

import img.myapplication.MySQLiteHelper;
import img.myapplication.R;
import models.JuniorCardViewHolder;
import models.JuniorModel;

public class JuniorConnectAccepted extends Fragment {

    private JuniorCardArrayAdapter cardArrayAdapter;
    private ListView listView;
    private TextView zerocount;
    private MySQLiteHelper db;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        db=new MySQLiteHelper(getContext());
        View view= inflater.inflate(R.layout.fragment_junior_connect_accepted, container, false);
        listView= (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));
        cardArrayAdapter = new JuniorCardArrayAdapter(getContext(), R.layout.junior_card);
        zerocount= (TextView) view.findViewById(R.id.zerocount );
        cardArrayAdapter.refresh();
        listView.setAdapter(cardArrayAdapter);
        return view;
    }


    public class JuniorCardArrayAdapter  extends ArrayAdapter<JuniorModel> {

        public void refresh(){
            this.cardList.clear();
            this.cardList.addAll(db.getAcceptedJuniors());
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
                row = inflater.inflate(R.layout.junior_card, parent, false);
                viewHolder = new JuniorCardViewHolder();
                viewHolder.name = (TextView) row.findViewById(R.id.j_name);
                viewHolder.town = (TextView) row.findViewById(R.id.j_town);
                viewHolder.state = (TextView) row.findViewById(R.id.j_state);
                viewHolder.branch= (TextView) row.findViewById(R.id.j_branch);
                viewHolder.contact= (TextView) row.findViewById(R.id.j_contact);
                viewHolder.email= (TextView) row.findViewById(R.id.j_email);
                viewHolder.fblink= (TextView) row.findViewById(R.id.j_fblink);

            } else {
                viewHolder = (JuniorCardViewHolder)row.getTag();
            }
            final JuniorModel card = getItem(position);
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
            if ("".equals(card.mobile))
                row.findViewById(R.id.contactline).setVisibility(View.GONE);
            else {
                row.findViewById(R.id.contactline).setVisibility(View.VISIBLE);
                viewHolder.contact.setText(card.mobile);
            }
            if ("".equals(card.email))
                row.findViewById(R.id.emailline).setVisibility(View.GONE);
            else {
                row.findViewById(R.id.emailline).setVisibility(View.VISIBLE);
                viewHolder.email.setText(card.email);
            }
            if ("".equals(card.fblink))
                row.findViewById(R.id.fbline).setVisibility(View.GONE);
            else {
                row.findViewById(R.id.fbline).setVisibility(View.VISIBLE);
                viewHolder.fblink.setText(card.fblink);
            }

            if (card.toggle)
                ((LinearLayout) row.findViewById(R.id.down_view)).setVisibility(View.VISIBLE);
            else
                ((LinearLayout) row.findViewById(R.id.down_view)).setVisibility(View.GONE);
            ((ToggleButton) row.findViewById(R.id.toggle_junior)).setChecked(card.toggle);
            row.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (card.toggle){
                        card.toggle=false;
                        ((LinearLayout) v.findViewById(R.id.card_layout)).setLayoutTransition(null);
                        ((LinearLayout) v.findViewById(R.id.down_view)).setVisibility(View.GONE);
                        ((ToggleButton) v.findViewById(R.id.toggle_junior)).setChecked(false);
                    }
                    else {
                        card.toggle=true;
                        ((LinearLayout) v.findViewById(R.id.card_layout)).setLayoutTransition(new LayoutTransition());
                        ((LinearLayout) v.findViewById(R.id.down_view)).setVisibility(View.VISIBLE);
                        ((ToggleButton) v.findViewById(R.id.toggle_junior)).setChecked(true);
                    }
                }
            });
            row.setTag(viewHolder);
            return row;
        }

    }


}
