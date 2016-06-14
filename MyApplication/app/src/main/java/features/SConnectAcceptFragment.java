package features;


import android.animation.LayoutTransition;
import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.ToggleButton;

import java.util.ArrayList;
import java.util.List;

import img.myapplication.ImageDownloader;
import img.myapplication.MySQLiteHelper;
import img.myapplication.R;
import img.myapplication.RoundImageView;
import models.SeniorCardViewHolder;
import models.SeniorModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class SConnectAcceptFragment extends Fragment {

    private SeniorCardArrayAdapter cardArrayAdapter;
    private MySQLiteHelper db;
    private RoundImageView fav_button;
    private TextView zerocount;
    private String acceptedURL;
    private String hostURL;
    private ImageDownloader imageDownloader;
    private void getURLs() {
        hostURL = getString(R.string.host);
        String appURL=getString(R.string.app);
        acceptedURL = appURL + "/accepted/";
    }
    private boolean cancelled;
    @Override
    public void onDestroyView(){
        cancelled=true;
        super.onDestroyView();
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        getURLs();
        cancelled=false;
        imageDownloader=new ImageDownloader(getContext());
        db=new MySQLiteHelper(getContext());
        View view = inflater.inflate(R.layout.fragment_sconnect_accept, container, false);

        ListView listView = (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));
        fav_button= (RoundImageView) view.findViewById(R.id.fav_button);
        listView.setOnScrollListener(new AbsListView.OnScrollListener() {
            @Override
            public void onScrollStateChanged(AbsListView view, int scrollState) {
                switch (scrollState){
                    case SCROLL_STATE_IDLE:
                        fav_button.setVisibility(View.VISIBLE);
                        break;
                    default:
                        fav_button.setVisibility(View.GONE);
                }
            }
            @Override
            public void onScroll(AbsListView view, int firstVisibleItem, int visibleItemCount, int totalItemCount) {
                if (firstVisibleItem+visibleItemCount==totalItemCount)
                    fav_button.setVisibility(View.VISIBLE);
            }
        });

        zerocount= (TextView) view.findViewById(R.id.zerocount);
        cardArrayAdapter = new SeniorCardArrayAdapter(getContext(), R.layout.list_senior_card);

        cardArrayAdapter.refresh();
        listView.setAdapter(cardArrayAdapter);
        return view;
    }


    public class SeniorCardArrayAdapter  extends ArrayAdapter<SeniorModel> {

        private List<SeniorModel> cardList = new ArrayList<SeniorModel>();

        public void refresh(){
            this.cardList.clear();
            this.cardList.addAll(db.getAcceptedSeniors());
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
                viewHolder.contact= (TextView) row.findViewById(R.id.s_contact);
                viewHolder.email= (TextView) row.findViewById(R.id.s_email);
                viewHolder.fblink= (TextView) row.findViewById(R.id.s_fblink);
                viewHolder.dp= (ImageView) row.findViewById(R.id.s_dp);
                viewHolder.year= (TextView) row.findViewById(R.id.s_year);
            } else {
                viewHolder = (SeniorCardViewHolder)row.getTag();
            }
            final SeniorModel card = getItem(position);
            viewHolder.name.setText(card.name);
            viewHolder.branch.setText(card.branch);
            viewHolder.state.setText(card.state);
            viewHolder.year.setText("Year "+String.valueOf(card.year));
            if (card.town.isEmpty())
                viewHolder.town.setVisibility(View.GONE);
            else {
                viewHolder.town.setVisibility(View.VISIBLE);
                viewHolder.town.setText(card.town + ", ");
            }
            if ("".equals(card.email))
                row.findViewById(R.id.emailline).setVisibility(View.GONE);
            else {
                row.findViewById(R.id.emailline).setVisibility(View.VISIBLE);
                viewHolder.email.setText(card.email);
            }
            if (card.contact.isEmpty())
                row.findViewById(R.id.contactline).setVisibility(View.GONE);
            else {
                row.findViewById(R.id.contactline).setVisibility(View.VISIBLE);
                viewHolder.contact.setText(card.contact);
            }
            if (card.dp_link==null || "".equals(card.dp_link))
                viewHolder.dp.setVisibility(View.GONE);
            else {
                viewHolder.dp.setVisibility(View.VISIBLE);
                imageDownloader.getImage(card.dp_link, viewHolder.dp
                        , (int) getResources().getDimension(R.dimen.roundimage_length)
                        , (int) getResources().getDimension(R.dimen.roundimage_length)
                        ,R.drawable.ic_person_black_24dp);
            }
            if ("".equals(card.fblink))
                row.findViewById(R.id.fbline).setVisibility(View.GONE);
            else {
                row.findViewById(R.id.fbline).setVisibility(View.VISIBLE);
                viewHolder.fblink.setText(card.fblink);
            }

            row.findViewById(R.id.toggle_senior).setVisibility(View.VISIBLE);
            ((ToggleButton) row.findViewById(R.id.toggle_senior)).setChecked(card.toggle);
            if (card.toggle)
                ((LinearLayout) row.findViewById(R.id.down_view)).setVisibility(View.VISIBLE);
            else
                ((LinearLayout) row.findViewById(R.id.down_view)).setVisibility(View.GONE);

            row.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (card.toggle){
                        card.toggle=false;
                        ((LinearLayout) v.findViewById(R.id.card_layout)).setLayoutTransition(null);
                        ((LinearLayout) v.findViewById(R.id.down_view)).setVisibility(View.GONE);
                        ((ToggleButton) v.findViewById(R.id.toggle_senior)).setChecked(false);
                    }
                    else {
                        card.toggle=true;
                        ((LinearLayout) v.findViewById(R.id.card_layout)).setLayoutTransition(new LayoutTransition());
                        ((LinearLayout) v.findViewById(R.id.down_view)).setVisibility(View.VISIBLE);
                        ((ToggleButton) v.findViewById(R.id.toggle_senior)).setChecked(true);
                    }
                }
            });

            row.setTag(viewHolder);
            return row;
        }
    }

}
