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
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

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

import img.myapplication.NetworkErrorFragment;
import img.myapplication.R;
import models.BlogCardViewHolder;
import models.BlogModel;


public class BlogsFragment extends Fragment {


    private BlogCardArrayAdapter cardArrayAdapter;
    private List<BlogModel> items;
    private ListView listView;
    private int blogsCount;
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View view=inflater.inflate(R.layout.fragment_blogs, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        SwipeRefreshLayout swipeLayout= (SwipeRefreshLayout) view.findViewById(R.id.swipe_refresh_layout);

        swipeLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                new LoadBlogTask().execute();
            }
        });

        items=new ArrayList<BlogModel>();
        cardArrayAdapter = new BlogCardArrayAdapter(getContext(), R.layout.list_item_card);
        blogsCount=0;
/*        if (isConnected()){
            updateBlogs();
        }
        getCardList();
*/
        if (isConnected())
            new LoadBlogTask().execute();
        else
            getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();

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
    private class LoadBlogTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... params) {

            try {
                loadBlogs();
                return "success";
            } catch (Exception e) {
                return "Unable to retrieve web page. URL may be invalid.";
            }
        }
        // onPostExecute displays the results of the AsyncTask.
        @Override
        protected void onPostExecute(String result) {
            if (result.equals("success")){
                //cardArrayAdapter.notifyDataSetChanged();

                cardArrayAdapter.refresh();
                items.clear();
            }
        }
    }
    public void loadBlogs(){
        try {
            URL url= new URL("http://192.168.121.187:8080/new_entrants/blogs?action=next&id="+blogsCount);
            HttpURLConnection conn=(HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
            StringBuilder sb=new StringBuilder();
            String line = "";
            while((line = bufferedReader.readLine()) != null)
                sb.append(line + '\n');
            String result=sb.toString();
            getBlogs(result);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public void getBlogs(String result){
        try {
            JSONObject jObject = new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("blogs");
            int len=jArray.length();

            for(int i=0; i<len;i++){
                JSONObject object=jArray.getJSONObject(i);
                BlogModel model= new BlogModel();
                model.topic=object.getString("title");
                model.blogurl=object.getString("blog_url");
                model.imageurl=object.getString("dp_link");
                model.group=object.getString("group");
                model.shortInfo=object.getString("description");
                model.date=object.getString("date");
                model.id = Integer.parseInt(object.getString("id"));
                model.blogText=null;
                items.add(model);
                //cardArrayAdapter.notifyDataSetChanged();
                blogsCount+=1;
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
/*    public void updateBlogs(){
        try {
            URL url= new URL("192.168.121.187:8080/new_entrants/blogs/");
            HttpURLConnection conn=(HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
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
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        db.deleteBlogs();
        try {
            JSONObject jObject = new JSONObject(result);
            JSONArray jArray=jObject.getJSONArray("blogs");

            JSONObject object=null;

            for(int i=0; i<jArray.length();i++){

                object=jArray.getJSONObject(i);
                BlogModel model= new BlogModel();
                model.topic=object.getString("title");
                model.blogurl=object.getString("blog_url");
                model.imageurl=object.getString("dp_link");
                model.group=object.getString("group");
                model.shortInfo=object.getString("description");
                model.date=object.getString("date");
                model.id=object.getInt("id");
                model.blogText=null;
                db.addBlog(model);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    public void getCardList(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        List<BlogModel> blogList=db.getBlogs();
        for (int i=0; i<blogList.size(); i++){
            cardArrayAdapter.add(blogList.get(i));
        }
    }
*/
    public class BlogCardArrayAdapter  extends ArrayAdapter<BlogModel> {

        public void refresh(){
            this.cardList.clear();
            this.cardList.addAll(items);
            notifyDataSetChanged();
        }

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
                viewHolder.group= (TextView) row.findViewById(R.id.author);
                viewHolder.date = (TextView) row.findViewById(R.id.date);
                viewHolder.img = (ImageView) row.findViewById(R.id.card_img);
                //viewHolder.model=new BlogModel();
                viewHolder.blogUrl="";

            } else {
                viewHolder = (BlogCardViewHolder)row.getTag();
            }
            BlogModel card = getItem(position);
            viewHolder.topic.setText(card.topic);
            viewHolder.shortInfo.setText(card.shortInfo);
            viewHolder.group.setText(card.group);
            viewHolder.date.setText(card.date);
            //viewHolder.model.copy(card);
            viewHolder.blogUrl=card.blogurl;
            new ImageLoadTask(card.imageurl,viewHolder.img);
            row.setTag(viewHolder);
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

        @Override
        protected void onPostExecute(Bitmap result) {
            super.onPostExecute(result);
            imageView.setImageBitmap(result);
        }

    }

}
