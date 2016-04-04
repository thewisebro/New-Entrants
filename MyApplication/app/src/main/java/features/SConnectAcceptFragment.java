package features;


import android.annotation.TargetApi;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.ToggleButton;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import img.myapplication.MySQLiteHelper;
import img.myapplication.R;
import models.SeniorCardViewHolder;
import models.SeniorModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class SConnectAcceptFragment extends Fragment {

    private SeniorCardArrayAdapter cardArrayAdapter;
    private List<SeniorModel> list=new ArrayList<SeniorModel>();
    private ListView listView;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_sconnect_accept, container, false);

        listView = (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        cardArrayAdapter = new SeniorCardArrayAdapter(getContext(), R.layout.list_senior_card);

        if (isConnected())
        {
            new UpdateAcceptedSeniorsTask().execute();
        }

        listView.setAdapter(cardArrayAdapter);
        return view;
    }
    private void getAcceptedSeniors(){
        if (isConnected()){
            new UpdateAcceptedSeniorsTask().execute();
        }
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        //list=db.getSeniors();
        cardArrayAdapter.refresh();
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
            this.dialog=new ProgressDialog(getContext());
            this.dialog.setMessage("Loading...");
            this.dialog.show();
        }
        @Override
        protected String doInBackground(String... args) {

            try {
                HttpURLConnection conn= (HttpURLConnection) new URL("http://192.168.121.187:8080/new_entrants/accepted/").openConnection();
                conn.setRequestMethod("GET");
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+getEntrantSESSID());
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');

                JSONArray jArray=(new JSONObject(sb.toString())).getJSONArray("students");
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
                    list.add(model);

                }
                return "success";
            } catch (Exception e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }

        }

        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")) {
                cardArrayAdapter.refresh();
            }
            dialog.dismiss();
        }
    }
    public class SeniorCardArrayAdapter  extends ArrayAdapter<SeniorModel> {

        private List<SeniorModel> cardList = new ArrayList<SeniorModel>();

        public void refresh(){
            this.cardList.clear();
            this.cardList.addAll(list);
            list.clear();
            notifyDataSetChanged();
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
            } else {
                viewHolder = (SeniorCardViewHolder)row.getTag();
            }
            SeniorModel card = getItem(position);
            viewHolder.name.setText(card.name);
            viewHolder.branch.setText(card.branch);
            viewHolder.state.setText(card.state);
            if (card.town.isEmpty())
                viewHolder.town.setVisibility(View.GONE);
            else
                viewHolder.town.setText(card.town);
            viewHolder.email.setText(card.email);
            viewHolder.contact.setText(card.contact);
            if (card.dp_link.isEmpty())
                viewHolder.dp.setVisibility(View.GONE);
            else
                new ImageLoadTask(card.dp_link,viewHolder.dp).execute();
            if (card.fblink.isEmpty())
                viewHolder.fblink.setVisibility(View.GONE);
            else
                viewHolder.fblink.setText(card.fblink);
            ToggleButton bt= (ToggleButton) row.findViewById(R.id.toggle_senior);
            bt.setVisibility(View.VISIBLE);
            bt.setTag(row.findViewById(R.id.down_view));
            bt.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    RelativeLayout layout = (RelativeLayout) buttonView.getTag();
                    if (isChecked)
                        layout.setVisibility(View.VISIBLE);
                    else
                        layout.setVisibility(View.GONE);
                }
            });
            return row;
        }
    }
    public class ImageLoadTask extends AsyncTask<Void, Void, Bitmap> {

        private String url;
        private ImageView imageView;

        public ImageLoadTask(String url, ImageView imageView) {
            this.url = url;
            this.imageView = imageView;
        }

        @Override
        protected Bitmap doInBackground(Void... params) {
            try {
                URL urlConnection = new URL(url);
                HttpURLConnection connection = (HttpURLConnection) urlConnection
                        .openConnection();
                connection.setDoInput(true);
                connection.connect();
                InputStream input = connection.getInputStream();
                Bitmap myBitmap = BitmapFactory.decodeStream(input);
                return myBitmap;
            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }

        @TargetApi(Build.VERSION_CODES.JELLY_BEAN)
        @Override
        protected void onPostExecute(Bitmap result) {
            super.onPostExecute(result);
            imageView.setImageBitmap(result);
        }

    }
}
