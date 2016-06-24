package features;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

import img.myapplication.ImageDownloader;
import img.myapplication.MySQLiteHelper;
import img.myapplication.Navigation;
import img.myapplication.NavigationAudience;
import img.myapplication.NavigationStudent;
import img.myapplication.NetworkErrorFragment;
import img.myapplication.R;
import models.BlogModel;

@SuppressLint("ValidFragment")
public class BlogWebView extends Fragment {
    private BlogModel model=new BlogModel();
    private String url;
    public TextView topic;
    public TextView description;
    public TextView date;
    public WebView content;
    public TextView group;
    public ImageView dp;
    public RelativeLayout group_card;
    private String BlogUrl;
    private String hostURL;
    private String sessid;
    private int screen_width;
    public BlogWebView(String blogUrl){
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
            ((Navigation) getActivity()).setActionBarTitle(getString(R.string.title_blogs));
            sessid=getEntrantSESSID();
        }
        else if (getActivity() instanceof NavigationStudent){
            ((NavigationStudent)getActivity()).setActionBarTitle(getString(R.string.title_blogs));
            sessid=getStudentSESSID();
        }
        else if (getActivity() instanceof NavigationAudience){
            ((NavigationAudience)getActivity()).setActionBarTitle(getString(R.string.title_blogs));
            sessid=getStudentSESSID();
        }

        View view= inflater.inflate(R.layout.blogwebview, container, false);
        cancelled=false;
        topic= (TextView) view.findViewById(R.id.title);
        description= (TextView) view.findViewById(R.id.description);
        date= (TextView) view.findViewById(R.id.date);
        content= (WebView) view.findViewById(R.id.blogHTML);
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

        StringBuilder sb=new StringBuilder();
        sb.append("<HTML><HEAD>" +
                "<style>" +
                "a.ckeditor_img > img {" +
                "width: 100% !important;" +
                "height: auto !important;" +
                "}" +
                "</style>" +
                "</HEAD><body>");
        sb.append(model.content);
        sb.append("</body></HTML>");
        content.loadData(sb.toString(), "text/html; charset=utf-8", "UTF-8");
        WebSettings settings= content.getSettings();
        settings.setTextSize(WebSettings.TextSize.SMALLER);
        //settings.setDefaultFontSize((int) getResources().getDimension(R.dimen.webview_textsize));
        settings.setBuiltInZoomControls(true);
        settings.setSupportZoom(true);
        //settings.setDisplayZoomControls(false);
        //settings.setLayoutAlgorithm(WebSettings.LayoutAlgorithm.SINGLE_COLUMN);
        //settings.setDefaultZoom(WebSettings.ZoomDensity.FAR);
        //settings.setUseWideViewPort(true);
        //settings.setLoadWithOverviewMode(false);
        content.setBackgroundColor(getResources().getColor(R.color.light_blue));

        group.setText(model.group);
        if (model.student){
            dp.setImageResource(R.drawable.ic_person_black_24dp);
        }
        else {
            dp.setImageResource(R.drawable.ic_group_black_24dp);
            group_card.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    getFragmentManager().beginTransaction().replace(R.id.container, new GroupBlogList(model.group_username, model.group))
                            .addToBackStack(null).commit();
                }
            });
        }
        new ImageDownloader(getContext()).loadImage(hostURL+model.dpurl,dp
                ,(int) getResources().getDimension(R.dimen.roundimage_length)
                ,(int) getResources().getDimension(R.dimen.roundimage_length));
    }
    public String getData(String str){
        try {
            JSONObject object=new JSONObject(str);
            if ("success".equals(object.getString("status"))){

                model.dpurl=object.getString("dp_link");
                model.content=object.getString("content");
                model.date=object.getString("date");
                SimpleDateFormat inputDate=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                SimpleDateFormat outputDate=new SimpleDateFormat("d MMM, yyyy");
                try {
                    Date input=inputDate.parse(model.date);
                    model.date=outputDate.format(input);
                } catch (ParseException e) {
                    e.printStackTrace();
                }
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

}
