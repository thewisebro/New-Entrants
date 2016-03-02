package features;

import android.annotation.SuppressLint;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
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

/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class BlogPage extends Fragment {
    //private BlogModel blog;
    private String url;
    private TextView topic;
    private TextView description;
    private TextView date;
    private TextView content;
    private TextView group;
    private ImageView image;
    public BlogPage(String blogUrl){
        this.url=blogUrl;
        //this.blog=model;
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_blog_page, container, false);

        topic= (TextView) view.findViewById(R.id.topic);
        description= (TextView) view.findViewById(R.id.shortInfo);
        date= (TextView) view.findViewById(R.id.date);
        content= (TextView) view.findViewById(R.id.blogText);
        group= (TextView) view.findViewById(R.id.group);
        image=(ImageView) view.findViewById(R.id.blog_img);

        /*topic.setText(blog.topic);
        //shortInfo.setText(blog.shortInfo);
        blogText.setText(blog.blogText);
        date.setText(blog.date);
        group.setText(blog.group);
        //author.setText(blog.author);*/
        new BlogTask().execute();
        return view;
    }

    private class BlogTask extends AsyncTask<String,Void,String>{

        @Override
        protected String doInBackground(String... params) {
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(url).openConnection();
                conn.setRequestMethod("GET");
                conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
                conn.setRequestProperty("Accept", "application/xml");

                BufferedReader reader= new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuffer buffer=new StringBuffer();
                String inputLine;
                while ((inputLine = reader.readLine()) != null)
                    buffer.append(inputLine+"\n");
                displayBlog(buffer.toString());

            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPostExecute(String result){

        }
    }
    private void displayBlog(String result){
        try {
            JSONObject object= new JSONObject(result);
            topic.setText(object.getString("topic"));
            date.setText(object.getString("date"));
            description.setText(object.getString("description"));
            content.setText(object.getString("content"));
            group.setText(object.getString("group"));
            new ImageLoadTask(object.getString("imageurl"),image);

        } catch (JSONException e) {
            e.printStackTrace();
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
