package features;


import android.animation.LayoutTransition;
import android.annotation.TargetApi;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.util.LruCache;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import img.myapplication.MySQLiteHelper;
import img.myapplication.Navigation;
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
    private LruCache<String,Bitmap> bitmapCache;
    private TextView zerocount;
    private String acceptedURL;
    private String hostURL;
    private void getURLs() {
        hostURL = getString(R.string.host);
        acceptedURL = hostURL + "/new_entrants/accepted/";
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
        //setCache();
        bitmapCache=((Navigation)getActivity()).bitmapCache;
        listView = (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));
        zerocount= (TextView) view.findViewById(R.id.zerocount);
        cardArrayAdapter = new SeniorCardArrayAdapter(getContext(), R.layout.list_senior_card);

/*        if (isConnected())
        {
            new UpdateAcceptedSeniorsTask().execute();
        }
        else
            getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();
*/
        new UpdateAcceptedSeniorsTask().execute();
        listView.setAdapter(cardArrayAdapter);
        return view;
    }

    public boolean isConnected() {
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }
    private String getEntrantSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getEntrant().sess_id;
    }
    private class UpdateAcceptedSeniorsTask extends AsyncTask<String, Void, String> {
        private ProgressDialog dialog;
        @Override
        protected void onPreExecute(){
            cardArrayAdapter.refresh();
            this.dialog=new ProgressDialog(getContext());
            this.dialog.setMessage("Updating List...");
            this.dialog.setIndeterminate(false);
            this.dialog.setCancelable(false);
            this.dialog.setButton(DialogInterface.BUTTON_NEGATIVE, "CANCEL", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    cancel(true);
                }
            });
            this.dialog.show();
        }
        @Override
        protected void onCancelled(String result){
            if (!cancelled){
                Toast.makeText(getContext(), "Update aborted!", Toast.LENGTH_SHORT).show();
                cardArrayAdapter.refresh();
                dialog.dismiss();
            }
        }
        @Override
        protected String doInBackground(String... args) {

            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(acceptedURL).openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+getEntrantSESSID());
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');

                JSONObject jObject=new JSONObject(sb.toString());
                if ("success".equals(jObject.getString("status"))){
                    JSONArray jArray=jObject.getJSONArray("students");
                    int len=jArray.length();

                    for(int i=0; i<len;i++){
                        JSONObject object=jArray.getJSONObject(i);
                        SeniorModel model= new SeniorModel();
                        model.name=object.getString("name");
                        model.town=object.getString("hometown");
                        model.state=(new JSONObject(object.getString("state"))).getString("name");
                        model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                        model.fblink=object.getString("fb_link");
                        model.contact=object.getString("contact");
                        model.email=object.getString("email");
                        model.dp_link=object.getString("dp_link");
                        model.year=object.getInt("year");
                        db.addSenior(model);
                    }
                    return "success";
                }
                else
                    return "fail";
            } catch (JSONException e){
                return "fail";
            } catch (Exception e) {
                return "error";
            }
        }

        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            dialog.dismiss();
            if (result.equals("success")) {
                Toast.makeText(getContext(), "List Updated!", Toast.LENGTH_SHORT).show();
            }
            else if (result.equals("error")){
                //getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();
                Toast.makeText(getContext(), "Unable to update! Check network connection", Toast.LENGTH_SHORT).show();
            }
            else
                Toast.makeText(getContext(), "Sorry! Unable to update", Toast.LENGTH_SHORT).show();
            cardArrayAdapter.refresh();
        }
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
            SeniorModel card = getItem(position);
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
                new ImageLoadTask(card.dp_link, viewHolder.dp, (int) getResources().getDimension(R.dimen.roundimage_length), (int) getResources().getDimension(R.dimen.roundimage_length))
                        .execute();
            }
            if ("".equals(card.fblink))
                row.findViewById(R.id.fbline).setVisibility(View.GONE);
            else {
                row.findViewById(R.id.fbline).setVisibility(View.VISIBLE);
                viewHolder.fblink.setText(card.fblink);
            }
            ToggleButton bt= (ToggleButton) row.findViewById(R.id.toggle_senior);
            bt.setVisibility(View.VISIBLE);
            bt.setTag(row.findViewById(R.id.card_layout));
            bt.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    LinearLayout layout = (LinearLayout) buttonView.getTag();
                    if (isChecked) {
                        ((LinearLayout) layout.findViewById(R.id.down_view)).setVisibility(View.VISIBLE);
                        layout.setLayoutTransition(null);

                    } else {
                        ((LinearLayout) layout.findViewById(R.id.down_view)).setVisibility(View.GONE);
                        layout.setLayoutTransition(new LayoutTransition());
                    }
                }
            });
            row.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    ToggleButton bt= (ToggleButton) v.findViewById(R.id.toggle_senior);
                    if (bt.isChecked())
                        bt.setChecked(false);
                    else
                        bt.setChecked(true);
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
        Bitmap bitmap=bitmapCache.get(url);
        if (bitmap==null){
            bitmap=loadImage();
            if (bitmap!=null)
                bitmapCache.put(url,bitmap);
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
