package img.myapplication;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class CardArrayAdapter  extends ArrayAdapter<BlogCard> {

    private List<BlogCard> cardList = new ArrayList<BlogCard>();

    static class CardViewHolder {
        TextView topic;
        TextView shortInfo;
        TextView author;
        TextView tag;
    }

    public CardArrayAdapter(Context context, int textViewResourceId) {
        super(context, textViewResourceId);
    }

    @Override
    public void add(BlogCard object) {
        cardList.add(object);
        super.add(object);
    }

    @Override
    public int getCount() {
        return this.cardList.size();
    }

    @Override
    public BlogCard getItem(int index) {
        return this.cardList.get(index);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View row = convertView;
        CardViewHolder viewHolder;
        if (row == null) {
            LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            row = inflater.inflate(R.layout.list_item_card, parent, false);
            viewHolder = new CardViewHolder();
            viewHolder.topic = (TextView) row.findViewById(R.id.topic);
            viewHolder.shortInfo = (TextView) row.findViewById(R.id.shortInfo);
            viewHolder.author = (TextView) row.findViewById(R.id.author);
            viewHolder.tag = (TextView) row.findViewById(R.id.tag);

            row.setTag(viewHolder);
        } else {
            viewHolder = (CardViewHolder)row.getTag();
        }
        BlogCard card = getItem(position);
        viewHolder.topic.setText(card.topic);
        viewHolder.shortInfo.setText(card.shortInfo);
        viewHolder.author.setText(card.author);
        viewHolder.tag.setText(card.tag);
        return row;
    }

    public Bitmap decodeToBitmap(byte[] decodedByte) {
        return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
    }
}