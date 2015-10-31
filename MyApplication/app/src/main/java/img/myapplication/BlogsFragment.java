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


public class BlogsFragment extends Fragment {


    private BlogCardArrayAdapter cardArrayAdapter;
    private ListView listView;

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View view=inflater.inflate(R.layout.fragment_blogs, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        cardArrayAdapter = new BlogCardArrayAdapter(getContext(), R.layout.list_item_card);

        for (int i = 0; i < 10; i++) {
            //Card card = new Card("Card " + (i+1) + " Line 1", "Card " + (i+1) + " Line 2");
            BlogModel card= new BlogModel();
            card.topic="lololol";
            card.shortInfo="test";
            card.author="ankush";
            card.category="example";
            card.date="2015-10-27";
            cardArrayAdapter.add(card);
        }
        listView.setAdapter(cardArrayAdapter);

        return view;
    }
    public class BlogCardArrayAdapter  extends ArrayAdapter<BlogModel> {

        private List<BlogModel> cardList = new ArrayList<BlogModel>();

        public class CardViewHolder {
            TextView topic;
            TextView shortInfo;
            TextView author;
            TextView category;
            TextView date;
            public BlogModel model;
        }

        public BlogCardArrayAdapter(Context context, int textViewResourceId) {
            super(context, textViewResourceId);
        }

        @Override
        public void add(BlogModel object) {
            cardList.add(object);
            super.add(object);
        }

        @Override
        public int getCount() {
            return this.cardList.size();
        }

        @Override
        public BlogModel getItem(int index) {
            return this.cardList.get(index);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View row = convertView;
            BlogCardViewHolder viewHolder;
            if (row == null) {
                LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                row = inflater.inflate(R.layout.list_item_card, parent, false);
                viewHolder = new BlogCardViewHolder();
                viewHolder.topic = (TextView) row.findViewById(R.id.topic);
                viewHolder.shortInfo = (TextView) row.findViewById(R.id.shortInfo);
                viewHolder.author = (TextView) row.findViewById(R.id.author);
                viewHolder.category = (TextView) row.findViewById(R.id.category);
                viewHolder.date = (TextView) row.findViewById(R.id.date);
                viewHolder.model=new BlogModel();
                //viewHolder.position=position;
                //row.findViewById(R.id.cardTop).setOnClickListener(this);
                //row.setTag(viewHolder);
            } else {
                viewHolder = (BlogCardViewHolder)row.getTag();
            }
            BlogModel card = getItem(position);
            viewHolder.topic.setText(card.topic);
            viewHolder.shortInfo.setText(card.shortInfo);
            viewHolder.author.setText(card.author);
            viewHolder.category.setText(card.category);
            viewHolder.date.setText(card.date);
            viewHolder.model=card;
            row.setTag(viewHolder);
            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }

}
