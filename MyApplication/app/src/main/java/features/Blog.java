package features;

import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.LevelListDrawable;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.Html;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import img.myapplication.MySQLiteHelper;
import img.myapplication.Navigation;
import img.myapplication.NavigationAudience;
import img.myapplication.NavigationStudent;
import img.myapplication.NetworkErrorFragment;
import img.myapplication.R;
import models.BlogModel;

@SuppressLint("ValidFragment")
public class Blog extends Fragment {
    private BlogModel model=new BlogModel();
    private String url;
    public TextView topic;
    public TextView description;
    public TextView date;
    public TextView content;
    public TextView group;
    public ImageView dp;
    public RelativeLayout group_card;
    private String BlogUrl;
    private String hostURL;
    private String sessid;
    private int screen_width;
    public Blog(String blogUrl){
        this.url=blogUrl;
    }
    private boolean cancelled=false;
    @Override
    public void onDestroyView(){
        cancelled=true;
        super.onDestroyView();
    }
    private void getURLs(){
        this.hostURL=getString(R.string.host);
        String appURL=getString(R.string.app);
        this.BlogUrl=appURL+"/blogs/";
    }
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        menu.clear();
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        getURLs();
        setHasOptionsMenu(true);
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

        View view= inflater.inflate(R.layout.blog, container, false);
        cancelled=false;
        topic= (TextView) view.findViewById(R.id.title);
        description= (TextView) view.findViewById(R.id.description);
        date= (TextView) view.findViewById(R.id.date);
        content= (TextView) view.findViewById(R.id.blogHTML);
        group= (TextView) view.findViewById(R.id.group);
        dp= (ImageView) view.findViewById(R.id.group_dp);
        group_card= (RelativeLayout) view.findViewById(R.id.group_card);
        screen_width=getActivity().getWindowManager().getDefaultDisplay().getWidth();
        if (isConnected())
            new BlogTask().execute();
        else
            getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();

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
    private String getStudentSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getStudent().sess_id;
    }
    private String getEntrantSESSID(){
        MySQLiteHelper db=new MySQLiteHelper(getContext());
        return db.getEntrant().sess_id;
    }
    private class BlogTask extends AsyncTask<String,Void,String>{

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
                    Toast.makeText(getContext(),"Loading aborted!",Toast.LENGTH_LONG).show();
                    dialog.dismiss();
                    topic.setText("Unable to display");

                }
            });
            this.dialog.show();
        }

        @Override
        protected String doInBackground(String... params) {
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(url).openConnection();
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestMethod("GET");
                conn.setRequestProperty("Cookie", "CHANNELI_SESSID=" + sessid);
                conn.setUseCaches(true);
                BufferedReader reader= new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuffer buffer=new StringBuffer();
                String inputLine;
                while ((inputLine = reader.readLine()) != null)
                    buffer.append(inputLine+"\n");
                JSONObject object=new JSONObject(buffer.toString());

                return getData(buffer.toString());

            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }
        @Override
        protected void onPostExecute(String result){

            if (getActivity()==null)
                return;

            dialog.dismiss();
            if (result==null){
                getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();
                Toast.makeText(getContext(), "Unable to load blog", Toast.LENGTH_SHORT).show();
            }
            else if (result.equals("success"))
                displayBlog();
            else
                Toast.makeText(getContext(), "Sorry! Unable to load blog!", Toast.LENGTH_SHORT).show();
        }
    }
    private void displayBlog(){
        date.setText(model.date);
        topic.setText(model.topic);
        description.setText(model.desc);
        content.setText(Html.fromHtml(model.content, new ImageGetter(), null));
        group.setText(model.group);
        if (model.student){
            dp.setImageResource(R.drawable.ic_person_black_24dp);
        }
        else {
            dp.setImageResource(R.drawable.ic_group_black_24dp);
            group_card.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String url = BlogUrl + model.group_username;
                    getFragmentManager().beginTransaction().replace(R.id.container, new GroupBlogList(url, model.group))
                            .addToBackStack(null).commit();
                }
            });
        }
        new ImageLoadTask(hostURL+model.dpurl,dp,(int) getResources().getDimension(R.dimen.roundimage_length),(int) getResources().getDimension(R.dimen.roundimage_length)).execute();
    }
    public String getData(String str){
        try {
            JSONObject object=new JSONObject(str);
            if ("success".equals(object.getString("status"))){

                model.dpurl=object.getString("dp_link");
                model.content=object.getString("content");
                model.date=object.getString("date");
                model.topic=object.getString("title");
                model.desc=object.getString("description");
                model.group=object.getString("group");
                model.id=object.getInt("id");
                model.group_username=object.getString("group_username");
                model.slug=object.getString("slug");
                model.student=object.getBoolean("student");
                return "success";
            }
            else
                return "fail";
        } catch (JSONException e) {
            e.printStackTrace();
            return "fail";
        }
    }
    public class ImageGetter implements Html.ImageGetter {

        @Override
        public Drawable getDrawable(String source) {
            LevelListDrawable d = new LevelListDrawable();

            new LoadImage().execute(source, d);

            return d;
        }
        class LoadImage extends AsyncTask<Object, Void, Bitmap> {

            private LevelListDrawable mDrawable;

            public int getSampleSize(String source){

                try {
                    HttpURLConnection connection = (HttpURLConnection) new URL(source).openConnection();
                    connection.setDoInput(true);
                    connection.setUseCaches(true);
                    connection.setConnectTimeout(3000);
                    connection.setReadTimeout(5000);
                    connection.connect();
                    InputStream input = connection.getInputStream();
                    BitmapFactory.Options options = new BitmapFactory.Options();
                    options.inJustDecodeBounds = true;
                    BitmapFactory.decodeStream(input, null, options);

                    final int height = options.outHeight;
                    final int width = options.outWidth;
                    int inSampleSize = 1;

                    if (width > screen_width) {

                        final int halfHeight = height / 2;
                        final int halfWidth = width / 2;

                        while ((halfWidth / inSampleSize) > screen_width) {
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
            protected Bitmap doInBackground(Object... params) {
                String source = (String) params[0];
                mDrawable = (LevelListDrawable) params[1];
                int insamplesize=getSampleSize(source);
                try {
                    //InputStream is = new URL(source).openStream();
                    HttpURLConnection connection= (HttpURLConnection) new URL(source).openConnection();
                    connection.setConnectTimeout(3000);
                    connection.setReadTimeout(7000);
                    connection.setDoInput(true);
                    connection.setUseCaches(true);
                    connection.connect();
                    InputStream is=connection.getInputStream();

                    BitmapFactory.Options options = new BitmapFactory.Options();
                    options.inSampleSize=insamplesize;
                    options.inJustDecodeBounds = false;

                    Bitmap bitmap=BitmapFactory.decodeStream(is, null, options);
                    return bitmap;
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                } catch (MalformedURLException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return null;
            }

            @Override
            protected void onPostExecute(Bitmap bitmap) {
                if (getActivity()==null)
                    return;
                if (bitmap != null) {

                    int width=bitmap.getWidth();
                    int height=bitmap.getHeight();
                    if (width>screen_width){
                        float aspectRatio = width / (float) height;
                        width=screen_width;
                        height=Math.round(screen_width / aspectRatio);
                    }

                    Bitmap resizedBitmap = Bitmap.createScaledBitmap(bitmap, width,height, true);
                    BitmapDrawable d = new BitmapDrawable(resizedBitmap);
                    mDrawable.addLevel(1, 1, d);
                    mDrawable.setBounds(0, 0, resizedBitmap.getWidth(), resizedBitmap.getHeight());
                    mDrawable.setLevel(1);

                    content.setText(content.getText());
                }
            }
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
                connection.setReadTimeout(10000);
                connection.setConnectTimeout(5000);
                connection.setDoInput(true);
                connection.connect();
                InputStream input = connection.getInputStream();

                BitmapFactory.Options options = new BitmapFactory.Options();
                options.inSampleSize=insamplesize/2;
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
            if (result!=null)
                imageView.setImageBitmap(result);
        }

    }

}
