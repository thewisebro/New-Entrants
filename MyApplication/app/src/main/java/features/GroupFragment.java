package features;

import android.annotation.SuppressLint;
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
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

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


@SuppressLint("ValidFragment")
public class GroupFragment extends Fragment {


    private BlogCardArrayAdapter cardArrayAdapter;
    private List<BlogModel> items;
    private ListView listView;
    private SwipeRefreshLayout swipeLayout;
    private int blogsCount;
    private int lastId;
    private String groupUrl;
    private String server="http://192.168.121.187:8080";

    public GroupFragment(String url){
        groupUrl=url;
    }
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View view=inflater.inflate(R.layout.fragment_blogs, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        listView.addFooterView(new View(getContext()));

        swipeLayout= (SwipeRefreshLayout) view.findViewById(R.id.swipe_refresh_layout);
        swipeLayout.setColorScheme(android.R.color.holo_blue_bright, android.R.color.holo_green_light, android.R.color.holo_orange_light,
                android.R.color.holo_red_light);

        swipeLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                if (isConnected()) {
                    new Handler().postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            new LoadBlogTask().execute();
                            Toast.makeText(getContext(), "List Updated", Toast.LENGTH_SHORT).show();
                            swipeLayout.setRefreshing(false);
                        }
                    }, 5000);
                }
            }

        });

        items=new ArrayList<BlogModel>();
        cardArrayAdapter = new BlogCardArrayAdapter(getContext(), R.layout.list_blog_card);
        blogsCount=0;
        lastId=0;
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
        private ProgressDialog dialog;
        @Override
        protected void onPreExecute(){
            this.dialog=new ProgressDialog(getContext());
            this.dialog.setMessage("Loading...");
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
            Toast.makeText(getContext(),"Loading aborted!",Toast.LENGTH_LONG).show();
            onPostExecute(result);
        }
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
            dialog.dismiss();
        }
    }
    public void loadBlogs(){
        String blogUrl=null;
        if (blogsCount==0)
            blogUrl=groupUrl;
        else
            blogUrl=groupUrl+"?action=next&id="+lastId;
        try {
            URL url= new URL(blogUrl);
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
                model.dpurl=object.getString("dp_link");
                model.group=object.getString("group");
                model.desc=object.getString("description");
                model.date=object.getString("date");
                model.id = Integer.parseInt(object.getString("id"));
                model.group_username=object.getString("group_username");
                model.slug=object.getString("slug");
                if (object.has("thumbnail"))
                    model.imageurl=object.getString("thumbnail");
                items.add(model);
                //cardArrayAdapter.notifyDataSetChanged();
                lastId =model.id;
                blogsCount+=1;
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public class BlogCardArrayAdapter  extends ArrayAdapter<BlogModel> {

        public void refresh(){
            //this.cardList.clear();
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
                row = inflater.inflate(R.layout.list_blog_card, parent, false);
                viewHolder = new BlogCardViewHolder();
                viewHolder.img = (ImageView) row.findViewById(R.id.blog_img);
                viewHolder.topic = (TextView) row.findViewById(R.id.topic);
                viewHolder.date = (TextView) row.findViewById(R.id.date);
                viewHolder.description = (TextView) row.findViewById(R.id.description);
                viewHolder.dp = (ImageView) row.findViewById(R.id.blog_dp);
                viewHolder.category = (TextView) row.findViewById(R.id.category);
                viewHolder.group = (TextView) row.findViewById(R.id.group);

            } else {
                viewHolder = (BlogCardViewHolder) row.getTag();
            }
            final BlogModel card = getItem(position);
            viewHolder.topic.setText(card.topic);
            viewHolder.description.setText(card.desc);
            viewHolder.group.setText(card.group);
            viewHolder.date.setText(card.date);
            viewHolder.category.setText("From the Groups");
            viewHolder.blogUrl = groupUrl+"/" + card.slug;
            new ImageLoadTask(card.dpurl,viewHolder.dp,(int) getResources().getDimension(R.dimen.roundimage_length),(int) getResources().getDimension(R.dimen.roundimage_length)).execute();
            if (card.imageurl!=null) {
                row.findViewById(R.id.card_middle).setVisibility(View.GONE);
                row.findViewById(R.id.img_layout).setVisibility(View.VISIBLE);
                new ImageLoadTask(server+card.imageurl, viewHolder.img,(int) getResources().getDimension(R.dimen.blogcardimg_height),getActivity().getWindowManager().getDefaultDisplay().getWidth()).execute();
            }
            else {
                row.findViewById(R.id.img_layout).setVisibility(View.GONE);
                row.findViewById(R.id.card_middle).setVisibility(View.VISIBLE);

            }
            row.setTag(viewHolder);
            row.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    BlogCardViewHolder holder = (BlogCardViewHolder) v.getTag();
                    getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new BlogPage(holder.blogUrl)).addToBackStack(null).commit();
                }
            });
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

        @Override
        protected Bitmap doInBackground(Void... params) {
            int insamplesize=getSampleSize();
            try {
                URL urlConnection = new URL(url);
                HttpURLConnection connection = (HttpURLConnection) urlConnection
                        .openConnection();
                connection.setDoInput(true);
                connection.connect();
                InputStream input = connection.getInputStream();

                BitmapFactory.Options options = new BitmapFactory.Options();
                options.inSampleSize=insamplesize;
                options.inJustDecodeBounds = false;

                Bitmap myBitmap= BitmapFactory.decodeStream(input,null,options);
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
