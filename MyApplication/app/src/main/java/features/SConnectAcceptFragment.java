package features;


import android.animation.LayoutTransition;
import android.annotation.TargetApi;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.ToggleButton;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import img.myapplication.BitmapCacheUtil;
import img.myapplication.MySQLiteHelper;
import img.myapplication.R;
import models.SeniorCardViewHolder;
import models.SeniorModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class SConnectAcceptFragment extends Fragment {

    private SeniorCardArrayAdapter cardArrayAdapter;
    private MySQLiteHelper db;
    private ListView listView;
    private TextView zerocount;
    private String acceptedURL;
    private String hostURL;
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
        db=new MySQLiteHelper(getContext());
        View view = inflater.inflate(R.layout.fragment_sconnect_accept, container, false);

        listView = (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));
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
                viewHolder.dp.setImageResource(R.drawable.ic_person_black_24dp);
                new ImageLoadTask(card.dp_link, viewHolder.dp, (int) getResources().getDimension(R.dimen.roundimage_length), (int) getResources().getDimension(R.dimen.roundimage_length))
                        .execute();
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

public class ImageLoadTask extends AsyncTask<Void, Void, Bitmap> {

    private String url;
    private ImageView imageView;
    private int ht;
    private int wt;

    public ImageLoadTask(String url, ImageView imageView, int h,int w) {
        this.url = url;
        this.imageView = imageView;
        this.ht=h;
        this.wt=w;
    }
    public int getSampleSize(){

        try {
            HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            BitmapFactory.Options options = new BitmapFactory.Options();
            options.inJustDecodeBounds = true;
            BitmapFactory.decodeStream(input, null, options);

            final int height = options.outHeight;
            final int width = options.outWidth;
            int inSampleSize = 1;

            if (height > ht || width > wt) {

                final int halfHeight = height / 2;
                final int halfWidth = width / 2;

                while ((halfHeight / inSampleSize) > ht
                        && (halfWidth / inSampleSize) > wt) {
                    inSampleSize *= 2;
                }
            }

            return inSampleSize;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return 1;
    }
    private Bitmap loadImage(){
        int insamplesize=getSampleSize();
        try {
            URL urlConnection = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) urlConnection
                    .openConnection();
            connection.setConnectTimeout(3000);
            connection.setReadTimeout(5000);
            connection.setDoInput(true);
            connection.setUseCaches(true);
            connection.connect();
            InputStream input = connection.getInputStream();

            BitmapFactory.Options options = new BitmapFactory.Options();
            options.inSampleSize=insamplesize/2;
            options.inJustDecodeBounds = false;

            return BitmapFactory.decodeStream(input,null,options);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
    private Bitmap image(){
        Bitmap bitmap=BitmapCacheUtil.getCache().get(url);
        if (bitmap==null){
            bitmap=loadImage();
            if (bitmap!=null)
                BitmapCacheUtil.getCache().put(url, bitmap);
        }
        return bitmap;
    }

    @Override
    protected Bitmap doInBackground(Void... params) {
        return image();
    }

    @TargetApi(Build.VERSION_CODES.JELLY_BEAN)
    @Override
    protected void onPostExecute(Bitmap result) {
        super.onPostExecute(result);
        if (result!=null)
            imageView.setImageBitmap(result);
    }

}
}
