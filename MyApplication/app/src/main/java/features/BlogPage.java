package features;

import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.DialogInterface;
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
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import img.myapplication.NetworkErrorFragment;
import img.myapplication.R;
import models.BlogModel;

/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class BlogPage extends Fragment {
    private BlogModel model=new BlogModel();
    private String url;
    public TextView topic;
    public TextView description;
    public TextView date;
    public TextView content;
    public TextView group;
    public TextView category;
    public ImageView image;
    public ImageView dp;
    public RelativeLayout group_card;

    private String server="http://192.168.121.187:8080";
    private String BlogUrl="http://192.168.121.187:8080/new_entrants/blogs/";
    public BlogPage(String blogUrl){

        this.url=blogUrl;
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_blog_page, container, false);
        topic= (TextView) view.findViewById(R.id.title);
        description= (TextView) view.findViewById(R.id.description);
        date= (TextView) view.findViewById(R.id.date);
        content= (TextView) view.findViewById(R.id.blogText);
        group= (TextView) view.findViewById(R.id.group);
        image=(ImageView) view.findViewById(R.id.blog_img);
        category= (TextView) view.findViewById(R.id.category);
        dp= (ImageView) view.findViewById(R.id.group_dp);
        group_card= (RelativeLayout) view.findViewById(R.id.group_card);

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
                }
            });
            this.dialog.show();
        }
        @Override
        protected void onCancelled(String result){
            Toast.makeText(getContext(), "Loading aborted!", Toast.LENGTH_LONG).show();
            dialog.dismiss();
            topic.setText("Unable to display");
        }

        @Override
        protected String doInBackground(String... params) {
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(url).openConnection();
                conn.setRequestMethod("GET");

                BufferedReader reader= new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuffer buffer=new StringBuffer();
                String inputLine;
                while ((inputLine = reader.readLine()) != null)
                    buffer.append(inputLine+"\n");

                getData(buffer.toString());
                return "success";

            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPostExecute(String result){
            if (result.equals("success"))
                displayBlog();
            if (dialog.isShowing())
                dialog.dismiss();
            if (result==null){
                getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();
            }
        }
    }
    public void getData(String str){
        try {
            JSONObject object=new JSONObject(str);
            model.dpurl=object.getString("dp_link");
            model.content=object.getString("content");
            model.date=object.getString("date");
            model.topic=object.getString("title");
            model.desc=object.getString("description");
            model.group=object.getString("group");
            model.id=object.getInt("id");
            model.group_username=object.getString("group_username");
            model.slug=object.getString("slug");
            model.imageurl=object.getString("thumbnail");
            model.setCategory();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    private void displayBlog(){
        date.setText(model.date);
        topic.setText(model.topic);
        description.setText(model.desc);
        content.setText(model.content);
        group.setText(model.group);
        category.setText(model.category);
        new ImageLoadTask(model.dpurl,dp,(int) getResources().getDimension(R.dimen.roundimage_length),(int) getResources().getDimension(R.dimen.roundimage_length)).execute();
        if (model.imageurl!=null) {
            new ImageLoadTask(server+model.imageurl,image, (int) getResources().getDimension(R.dimen.blogimg_ht),getActivity().getWindowManager().getDefaultDisplay().getWidth())
                    .execute();
        }
        group_card.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String url=BlogUrl+model.group_username;
                getFragmentManager().beginTransaction().replace(R.id.container, new GroupBlogList(url,model.group))
                        .addToBackStack(null).commit();
            }
        });
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
            imageView.setImageBitmap(result);
        }

    }

}
