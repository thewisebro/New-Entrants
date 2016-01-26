package img.myapplication;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
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
        if (isConnected()){
            updateBlogs();
        }
        getCardList();

        for (int i = 0; i < 10; i++) {

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
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }
    public void updateBlogs(){
        try {
            URL url= null;
            url = new URL("www.google.com");
            HttpURLConnection conn=(HttpURLConnection) url.openConnection();
            conn.setDoOutput(true);
            conn.setDoInput(true);
            BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
            StringBuilder sb=new StringBuilder();
            String line = "";
            while((line = bufferedReader.readLine()) != null)
                sb.append(line + '\n');
            String result=sb.toString();
            updateBlogsTable(result);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public void updateBlogsTable(String result){
        JSONObject jObject= null;
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        try {
            jObject = new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("blogs");

            for(int i=0; i<jArray.length();i++){

                JSONObject object=jArray.getJSONObject(i);
                BlogModel model= new BlogModel();

                model.topic="lololol";
                model.shortInfo="test";
                model.author="ankush";
                model.category="example";
                model.date="2015-10-27";

                db.addBlog(model);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    public void getCardList(){
        List<BlogModel> blogList=db.getBlogs();
        for (int i=0; i<blogList.size(); i++){
            cardArrayAdapter.add(blogList.get(i));
        }
    }
/*    public void getCardList(){
        if (isConnected()){
            try {
                URL url= null;
                url = new URL("www.google.com");
                HttpURLConnection conn=(HttpURLConnection) url.openConnection();
                conn.setDoOutput(true);
                conn.setDoInput(true);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                String result=sb.toString();
                cardsFromString(result);

                FileOutputStream fos = getContext().openFileOutput("blogs.txt",Context.MODE_PRIVATE);
                fos.write(result.getBytes());
                fos.close();
                bufferedReader.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        else {
            try {
                FileInputStream fis;
                fis = getContext().openFileInput("blogs.txt");
                StringBuffer fileContent = new StringBuffer("");

                byte[] buffer = new byte[1024];
                int n;
                while ((n = fis.read(buffer)) != -1)
                {
                    fileContent.append(new String(buffer, 0, n));
                }
                String blogString=fileContent.toString();
                cardsFromString(blogString);
            } catch (java.io.IOException e) {
                e.printStackTrace();
            }
        }
    }
    private void cardsFromString(String result){
        JSONObject jObject= null;
        try {
            jObject = new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("blogs");

            for(int i=0; i<jArray.length();i++){

                JSONObject object=jArray.getJSONObject(i);
                BlogModel card= new BlogModel();

                card.topic="lololol";
                card.shortInfo="test";
                card.author="ankush";
                card.category="example";
                card.date="2015-10-27";
                cardArrayAdapter.add(card);

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }


    }
    */
    public class BlogCardArrayAdapter  extends ArrayAdapter<BlogModel> {

        private List<BlogModel> cardList = new ArrayList<BlogModel>();

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

            } else {
                viewHolder = (BlogCardViewHolder)row.getTag();
            }
            BlogModel card = getItem(position);
            viewHolder.topic.setText(card.topic);
            viewHolder.shortInfo.setText(card.shortInfo);
            viewHolder.author.setText(card.author);
            viewHolder.category.setText(card.category);
            viewHolder.date.setText(card.date);
            viewHolder.model.copy(card);
            row.setTag(viewHolder);
            return row;
        }

        public Bitmap decodeToBitmap(byte[] decodedByte) {
            return BitmapFactory.decodeByteArray(decodedByte, 0, decodedByte.length);
        }
    }

}
