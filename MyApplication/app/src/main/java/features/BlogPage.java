package features;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

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
    public BlogPage(String blogUrl){
        this.url=blogUrl;
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_blog_page, container, false);
        topic= (TextView) view.findViewById(R.id.topic);
        description= (TextView) view.findViewById(R.id.description);
        date= (TextView) view.findViewById(R.id.date);
        content= (TextView) view.findViewById(R.id.blogText);
        group= (TextView) view.findViewById(R.id.group);
        image=(ImageView) view.findViewById(R.id.blog_img);
        category= (TextView) view.findViewById(R.id.category);
        dp= (ImageView) view.findViewById(R.id.group_dp);

        if (isConnected())
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    BlogTask task = new BlogTask();
                    task.execute();
                }
            }, 5000);
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

                getData( buffer.toString());
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
            model.category="From the Groups";
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
    private void displayBlog(){

        topic.setText(model.topic);
        date.setText(model.date);
        description.setText(model.desc);
        content.setText(model.content);
        group.setText(model.group);
        category.setText(model.category);
        ImageLoad(model.dpurl, dp);
        if (model.imageurl!=null) {
            ImageLoad(model.imageurl,image);
        }
    }
    public void ImageLoad(String url, ImageView imageView){
        try {
            URL urlConnection = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) urlConnection
                    .openConnection();
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            Bitmap myBitmap = BitmapFactory.decodeStream(input);
            imageView.setImageBitmap(myBitmap);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
