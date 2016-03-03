package features;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.RadioGroup;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.CookieStore;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import img.myapplication.MySQLiteHelper;
import img.myapplication.R;
import models.SeniorCardViewHolder;
import models.SeniorModel;


public class SConnectFragment extends Fragment {

    private SeniorCardArrayAdapter cardArrayAdapter;
    private ListView listView;
    private Map<String,String> params;

    public SConnectFragment(Map<String,String> userParams){
        this.params=userParams;
    }

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View view=inflater.inflate(R.layout.fragment_sconnect, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);
        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        Button bt_sort= (Button) view.findViewById(R.id.bt_sort);
        bt_sort.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                RadioGroup group= (RadioGroup) view.findViewById(R.id.group_sort);
                int bt_id= group.getCheckedRadioButtonId();
                if (bt_id== R.id.rb_location)
                    getCardList(1,params.get("state").toString());
                else
                    if (bt_id==R.id.rb_branch)
                        getCardList(2,params.get("branchcode").toString());
                    else
                        getCardList(0,"");
            }
        });

        cardArrayAdapter = new SeniorCardArrayAdapter(getContext(), R.layout.list_senior_card);

        if (isConnected()){
            //updateSeniors();
            new UpdateSeniorsTask().execute();
        }
        getCardList(0,"");

        listView.setAdapter(cardArrayAdapter);

        return view;
    }
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }
    private class UpdateSeniorsTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... params) {

            try {
                updateSeniors();
                return "success";
            } catch (Exception e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }
        }

        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")) {

            }
        }
    }
    public void updateSeniors(){
        CookieManager cookieManager= (CookieManager) CookieHandler.getDefault();
        CookieStore cookieStore=cookieManager.getCookieStore();
        try {
            URL url= null;
            url = new URL("http://192.168.121.187:8080/new_entrants/sconnect/");
            HttpURLConnection conn=(HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setDoInput(true);
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Cookie", TextUtils.join(";", cookieStore.getCookies()));


/*            OutputStream os = conn.getOutputStream();
            BufferedWriter writer = new BufferedWriter(
                    new OutputStreamWriter(os, "UTF-8"));
            writer.write();
            writer.flush();
            writer.close();
            os.close();
*/
            BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
            StringBuilder sb=new StringBuilder();
            String line = "";
            while((line = bufferedReader.readLine()) != null)
                sb.append(line + '\n');
            String result=sb.toString();
            updateSeniorsTable(result);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public void updateSeniorsTable(String result){

        MySQLiteHelper db=new MySQLiteHelper(getContext());

        try {
            JSONObject jObject = new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("seniors");
            SeniorModel model= new SeniorModel();

            for(int i=0; i<jArray.length();i++){

                JSONObject object=jArray.getJSONObject(i);
                model.name=object.getString("name");
                model.branchcode=object.getString("branch_code");
                model.branchname=object.getString("branch");
                model.email=object.getString("email");
                model.fb_link=object.getString("fb_link");
                model.hometown=object.getString("hometown");
                model.state=object.getString("state");
                model.mobile=object.getString("contact");
                db.addSenior(model);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
    public void getCardList(int opt,String param){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        List<SeniorModel> seniorList=db.getSeniors(opt,param);
        for (int i=0; i<seniorList.size(); i++){
            cardArrayAdapter.add(seniorList.get(i));
        }
        cardArrayAdapter.notifyDataSetChanged();
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
                viewHolder.name = (TextView) row.findViewById(R.id.s_name);
                //viewHolder.year = (TextView) row.findViewById(R.id.year);
                viewHolder.branchname = (TextView) row.findViewById(R.id.s_branch);
                viewHolder.branchcode= (TextView) row.findViewById(R.id.s_branchcode);
                viewHolder.email= (TextView) row.findViewById(R.id.s_email);
                viewHolder.hometown= (TextView) row.findViewById(R.id.s_hometown);
                viewHolder.state= (TextView) row.findViewById(R.id.s_state);
                viewHolder.mobile= (TextView) row.findViewById(R.id.s_mobile);
                viewHolder.fb_link= (TextView) row.findViewById(R.id.s_fblink);

                viewHolder.model=new SeniorModel();
            } else {
                viewHolder = (SeniorCardViewHolder)row.getTag();
            }
            SeniorModel card = getItem(position);
            viewHolder.name.setText(card.name);
            //viewHolder.year.setText(card.year);
            viewHolder.branchname.setText(card.branchname);
            viewHolder.branchcode.setText(card.branchcode);
            viewHolder.state.setText(card.state);
            viewHolder.hometown.setText(card.hometown);
            viewHolder.mobile.setText(card.mobile);
            viewHolder.fb_link.setText(card.fb_link);
            viewHolder.email.setText(card.email);

            viewHolder.model=card;
            row.setTag(viewHolder);
            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }

}
