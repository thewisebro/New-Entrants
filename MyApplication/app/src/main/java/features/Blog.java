package features;

import android.annotation.SuppressLint;
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
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.Html;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import img.myapplication.R;
import models.BlogModel;

@SuppressLint("ValidFragment")
public class Blog extends Fragment {
    private BlogModel model=new BlogModel();
    private String url;
    public TextView blog;
    public Blog(String blogUrl){
        this.url=blogUrl;
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.blog_page, container, false);
        blog= (TextView) view.findViewById(R.id.blogHTML);

        if (isConnected())
            new BlogTask().execute();
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
            Toast.makeText(getContext(),"Loading aborted!",Toast.LENGTH_LONG).show();
            onPostExecute(result);
        }

        @Override
        protected String doInBackground(String... params) {
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(url).openConnection();
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestMethod("GET");

                BufferedReader reader= new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuffer buffer=new StringBuffer();
                String inputLine;
                while ((inputLine = reader.readLine()) != null)
                    buffer.append(inputLine+"\n");
                JSONObject object=new JSONObject(buffer.toString());

               return object.getString("content");

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPostExecute(String result){
            if (result!=null){
                //blog.setText(Html.fromHtml(result,new URLImageParser(blog,getContext()),null));
                blog.setText(Html.fromHtml(result,new ImageGetter(),null));
            }
            else {
                Toast.makeText(getContext(),"Unable to load this blog",Toast.LENGTH_LONG).show();
            }
            dialog.dismiss();
        }
    }
    public class ImageGetter implements Html.ImageGetter {

        @Override
        public Drawable getDrawable(String source) {
            LevelListDrawable d = new LevelListDrawable();
            Drawable empty = getResources().getDrawable(R.mipmap.ic_launcher);
            d.addLevel(0, 0, empty);
            d.setBounds(0, 0, empty.getIntrinsicWidth(), empty.getIntrinsicHeight());

            new LoadImage().execute(source, d);

            return d;
        }
        class LoadImage extends AsyncTask<Object, Void, Bitmap> {

            private LevelListDrawable mDrawable;

            @Override
            protected Bitmap doInBackground(Object... params) {
                String source = (String) params[0];
                mDrawable = (LevelListDrawable) params[1];
                try {
                    InputStream is = new URL(source).openStream();
                    return BitmapFactory.decodeStream(is);
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
                if (bitmap != null) {
                    BitmapDrawable d = new BitmapDrawable(bitmap);
                    mDrawable.addLevel(1, 1, d);
                    mDrawable.setBounds(0, 0, bitmap.getWidth(), bitmap.getHeight());
                    mDrawable.setLevel(1);
                    // i don't know yet a better way to refresh TextView
                    // mTv.invalidate() doesn't work as expected
                    CharSequence t = blog.getText();
                    blog.setText(t);
                }
            }
        }
    }


}
