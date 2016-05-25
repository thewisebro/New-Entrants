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
import android.support.v4.app.Fragment;
import android.support.v4.view.MenuItemCompat;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.orangegangsters.github.swipyrefreshlayout.library.SwipyRefreshLayout;
import com.orangegangsters.github.swipyrefreshlayout.library.SwipyRefreshLayoutDirection;

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

import img.myapplication.BitmapCacheUtil;
import img.myapplication.MySQLiteHelper;
import img.myapplication.Navigation;
import img.myapplication.NavigationAudience;
import img.myapplication.NavigationStudent;
import img.myapplication.NetworkErrorFragment;
import img.myapplication.R;
import models.BlogCardViewHolder;
import models.BlogModel;


@SuppressLint("ValidFragment")
public class GroupBlogList extends Fragment {


    private BlogCardArrayAdapter cardArrayAdapter;
    private List<BlogModel> items;
    private ListView listView;
    private TextView tv;   //Footer View
    private SwipyRefreshLayout swipeLayout;
    private int blogsCount;
    private int lastId;
    private String sessid;
    private String groupUrl;
    private String groupName;
    private String host;
    private boolean resume;
    public GroupBlogList(String url,String group){
        groupUrl=url;
        groupName=group;
    }
    private boolean cancelled=false;
    @Override
    public void onDestroyView(){
        cancelled=true;
        super.onDestroyView();
    }
    @Override
    public void onCreate(Bundle savedInstanceState){
        cardArrayAdapter = new BlogCardArrayAdapter(getContext(), R.layout.list_blog_card);
        blogsCount=0;
        lastId=0;
        resume=true;
        super.onCreate(savedInstanceState);
    }
    private void getURL(){
        host=getString(R.string.host);
    }
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        getURL();
        if (getActivity() instanceof Navigation) {
            ((Navigation) getActivity()).setActionBarTitle("Blogs");
            sessid=getEntrantSESSID();
        }
        else if (getActivity() instanceof NavigationStudent){
            ((NavigationStudent)getActivity()).setActionBarTitle("Blogs");
            sessid=getStudentSESSID();
        }
        else if (getActivity() instanceof NavigationAudience){
            ((NavigationAudience)getActivity()).setActionBarTitle("Blogs");
            sessid=getStudentSESSID();
        }
        cancelled=false;
        setHasOptionsMenu(true);
        View view=inflater.inflate(R.layout.fragment_blogs, container, false);
        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        tv=new TextView(getContext());
        tv.setText("Pull Up to Load More");
        tv.setGravity(Gravity.CENTER_HORIZONTAL);
        listView.addFooterView(tv);

        swipeLayout= (SwipyRefreshLayout) view.findViewById(R.id.swipe_refresh_layout);
        swipeLayout.setColorScheme(android.R.color.holo_blue_bright, android.R.color.holo_green_light, android.R.color.holo_orange_light,
                android.R.color.holo_red_light);

        swipeLayout.setOnRefreshListener(new SwipyRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh(SwipyRefreshLayoutDirection swipyRefreshLayoutDirection) {
                if (isConnected()) {
                    new LoadBlogTask().execute();
                    swipeLayout.setRefreshing(false);
                }
                else
                    getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();

            }

        });

        items=new ArrayList<BlogModel>();
        //cardArrayAdapter = new BlogCardArrayAdapter(getContext(), R.layout.list_blog_card);

        if (!isConnected())
            getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();
        else if (resume)
                new LoadBlogTask().execute();

        listView.setAdapter(cardArrayAdapter);

        return view;
    }
    private String getStudentSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getStudent().sess_id;
    }
    private String getEntrantSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getEntrant().sess_id;
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
                    Toast.makeText(getContext(), "Loading aborted!", Toast.LENGTH_SHORT).show();
                }
            });
            this.dialog.show();
        }
        @Override
        protected String doInBackground(String... params) {

            String blogUrl=null;
            if (blogsCount==0)
                blogUrl=groupUrl;
            else
                blogUrl=groupUrl+"?action=next&id="+lastId;
            try {
                URL url= new URL(blogUrl);
                HttpURLConnection conn=(HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+sessid);
                conn.setUseCaches(true);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                String result=sb.toString();
                getBlogs(result);
                return "success";

            } catch (Exception e) {
                e.printStackTrace();
                return "Unable to load blogs";
            }
        }
        @Override
        protected void onPostExecute(String result) {

            if (getActivity()==null)
                return;

            if (result.equals("success")){
                cardArrayAdapter.refresh();
                items.clear();
                resume=false;
            }
            else if (result.equals("error")){
                getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();
                Toast.makeText(getContext(), "Unable to load blogs", Toast.LENGTH_SHORT).show();
            }
            else
                Toast.makeText(getContext(), "Sorry! Unable to load blogs", Toast.LENGTH_SHORT).show();
            dialog.dismiss();
        }
    }

    public String getBlogs(String result){
        try {
            JSONObject jObject = new JSONObject(result);
            if ("success".equals(jObject.getString("status"))){
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
                    lastId =model.id;
                    blogsCount+=1;
                }
                return "success";
            }
            else
                return "fail";
        } catch (JSONException e) {
            e.printStackTrace();
            return "fail";
        }
    }

    public class BlogCardArrayAdapter  extends ArrayAdapter<BlogModel> {

        public void refresh(){
            if (items.size()==0) {
                Toast.makeText(getContext(), "No More Blogs", Toast.LENGTH_LONG).show();
                listView.removeFooterView(tv);
            }
            else {
                //Toast.makeText(getContext(), "List Updated", Toast.LENGTH_SHORT).show();
                this.cardList.addAll(items);
                notifyDataSetChanged();
            }
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
            viewHolder.id=card.id;
            viewHolder.topic.setText(card.topic);
            viewHolder.description.setText(card.desc);
            viewHolder.group.setText(card.group);
            viewHolder.date.setText(card.date);
            viewHolder.category.setText("From the Groups");
            viewHolder.blogUrl = groupUrl+"/" + card.slug;

            viewHolder.dp.setImageResource(R.drawable.ic_group_black_24dp);
            new ImageLoadTask(host+card.dpurl,viewHolder.dp,(int) getResources().getDimension(R.dimen.roundimage_length),(int) getResources().getDimension(R.dimen.roundimage_length))
                    .executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
            int screen_width=getActivity().getWindowManager().getDefaultDisplay().getWidth();

            if (card.imageurl!=null) {
                row.findViewById(R.id.card_middle).setVisibility(View.GONE);
                row.findViewById(R.id.img_layout).setVisibility(View.VISIBLE);
                viewHolder.img.setImageResource(R.drawable.loading);
                new ImageLoadTask(host + card.imageurl, viewHolder.img,screen_width,screen_width)
                        .executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
            }
            else {
                row.findViewById(R.id.img_layout).setVisibility(View.GONE);
                row.findViewById(R.id.card_middle).setVisibility(View.VISIBLE);

            }
            row.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    BlogCardViewHolder holder = (BlogCardViewHolder) v.getTag();
                    getActivity().getSupportFragmentManager().beginTransaction()
                            .replace(R.id.container, new BlogWebView(holder.blogUrl)).addToBackStack(null).commit();
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
                if (isCancelled())
                    return 0;
                HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
                connection.setDoInput(true);
                connection.setUseCaches(true);
                connection.setConnectTimeout(3000);
                connection.setReadTimeout(5000);
                connection.connect();
                InputStream input = connection.getInputStream();
                BitmapFactory.Options options = new BitmapFactory.Options();
                options.inJustDecodeBounds = true;
                BitmapFactory.decodeStream(input, null, options);
                if (isCancelled())
                    return 0;
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
            if (isCancelled())
                return null;
            int insamplesize=getSampleSize();
            try {
                if (isCancelled())
                    return null;
                URL urlConnection = new URL(url);
                HttpURLConnection connection = (HttpURLConnection) urlConnection
                        .openConnection();
                connection.setConnectTimeout(3000);
                connection.setReadTimeout(5000);
                connection.setDoInput(true);
                connection.setUseCaches(true);
                connection.connect();
                if (isCancelled())
                    return null;
                InputStream input = connection.getInputStream();
                if (isCancelled())
                    return null;
                BitmapFactory.Options options = new BitmapFactory.Options();
                options.inSampleSize=insamplesize;
                options.inJustDecodeBounds = false;
                if (isCancelled())
                    return null;
                Bitmap bitmap=BitmapFactory.decodeStream(input,null,options);
                if (isCancelled())
                    return null;
                return bitmap;
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
            if (isCancelled())
                return null;
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
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater)
    {   menu.clear();
        inflater.inflate(R.menu.menu_groups,menu);
        final MenuItem item=menu.findItem(R.id.group_name);
        TextView group= (TextView) MenuItemCompat.getActionView(item);
        group.setText(groupName);
        int padding= (int) getResources().getDimension(R.dimen.actionbarname_padding);
        group.setPadding(0,0,padding,0);
    }
}
