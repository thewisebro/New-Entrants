package features;

import android.annotation.TargetApi;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.Typeface;
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
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.orangegangsters.github.swipyrefreshlayout.library.SwipyRefreshLayout;
import com.orangegangsters.github.swipyrefreshlayout.library.SwipyRefreshLayoutDirection;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import img.myapplication.ImageDownloader;
import img.myapplication.MySQLiteHelper;
import img.myapplication.Navigation;
import img.myapplication.NavigationAudience;
import img.myapplication.NavigationStudent;
import img.myapplication.NetworkErrorFragment;
import img.myapplication.R;
import models.BlogCardViewHolder;
import models.BlogModel;


public class BlogsList extends Fragment {

    public boolean refreshing=false;
    private BlogCardArrayAdapter cardArrayAdapter;
    private List<BlogModel> items;
    private ListView listView;
    private TextView tv;        //Footer View
    private TextView noblog;
    private TextView failed;
    private SwipyRefreshLayout swipeLayout;
    private int blogsCount;
    private int lastId;
    private String BlogUrl;
    private String url;
    boolean flag=false;
    boolean resume;
    private String sessid;
    private int spinnerPos;
    private String hostURL;
    private ImageDownloader imageDownloader;
    private void getURLs(){
        this.hostURL=getString(R.string.host);
        String appURL=getString(R.string.app);
        this.BlogUrl=appURL+"/blogs/";
    }
    private boolean visible;
    private boolean cancelled=false;
    @Override
    public void onDestroyView(){
        cancelled=true;
        super.onDestroyView();
    }
    @Override
    public void onCreate(Bundle savedInstanceState){
        getURLs();
        spinnerPos=0;
        cardArrayAdapter = new BlogCardArrayAdapter(getContext(), R.layout.list_blog_card);
        resume=true;
        visible=true;
        blogsCount=0;
        lastId=0;
        imageDownloader=new ImageDownloader(getContext());
        super.onCreate(savedInstanceState);
    }
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        if (getActivity() instanceof Navigation) {
            ((Navigation) getActivity()).getSupportActionBar().show();
            ((Navigation) getActivity()).setActionBarTitle(getString(R.string.title_blogs));
            sessid=getEntrantSESSID();
        }
        else if (getActivity() instanceof NavigationStudent){
            ((NavigationStudent) getActivity()).getSupportActionBar().show();
            ((NavigationStudent)getActivity()).setActionBarTitle(getString(R.string.title_blogs));
            sessid=getStudentSESSID();
        }
        else if (getActivity() instanceof NavigationAudience){
            ((NavigationAudience) getActivity()).getSupportActionBar().show();
            ((NavigationAudience)getActivity()).setActionBarTitle(getString(R.string.title_blogs));
            sessid=getStudentSESSID();
        }

        cancelled=false;
        setHasOptionsMenu(true);
        View view=inflater.inflate(R.layout.fragment_blogs, container, false);

        listView = (ListView) view.findViewById(R.id.card_listView);

        listView.addHeaderView(new View(getContext()));
        tv=new TextView(getContext());
        tv.setText("\nPull Up to Load More\n");
        tv.setGravity(Gravity.CENTER_HORIZONTAL);
        listView.addFooterView(tv);

        noblog=new TextView(getContext());
        noblog.setText(getString(R.string.no_blog));
        noblog.setGravity(Gravity.CENTER_HORIZONTAL);
        noblog.setTypeface(null, Typeface.BOLD);

        failed=new TextView(getContext());
        failed.setText("\nNetwork Error\n");
        failed.setGravity(Gravity.CENTER_HORIZONTAL);
        failed.setTypeface(null, Typeface.BOLD);

        swipeLayout= (SwipyRefreshLayout) view.findViewById(R.id.swipe_refresh_layout);
        swipeLayout.setColorScheme(android.R.color.holo_blue_bright, android.R.color.holo_green_light, android.R.color.holo_orange_light,
                android.R.color.holo_red_light);
        url=BlogUrl;

        swipeLayout.setOnRefreshListener(new SwipyRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh(SwipyRefreshLayoutDirection swipyRefreshLayoutDirection) {
                if (isConnected()) {

                    swipeLayout.setRefreshing(false);
                    refreshing = true;
                    new LoadBlogTask().execute();
                }
                else
                    getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new NetworkErrorFragment()).addToBackStack(null).commit();

            }

        });

        items=new ArrayList<BlogModel>();
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
                    dialog.dismiss();
                    Toast.makeText(getContext(), "Loading aborted!", Toast.LENGTH_SHORT).show();
                }
            });
            this.dialog.show();
        }
        @Override
        protected void onCancelled(String result){
            cardArrayAdapter.refresh();
            items.clear();
        }
        @Override
        protected String doInBackground(String... params) {

            String blogUrl=url;
            if (blogsCount!=0)
                blogUrl+="?action=next&id="+lastId;
            try {
                URL url= new URL(blogUrl);
                HttpURLConnection conn=(HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                String cookieHeader="CHANNELI_SESSID="+sessid;
                cookieHeader+=";CHANNELI_DEVICE="+"android";
                conn.setRequestProperty("Cookie",cookieHeader);
                conn.setUseCaches(true);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                String result=sb.toString();
                return getBlogs(result);

            } catch (Exception e) {
                e.printStackTrace();
                return "error";
            }
        }
        @Override
        protected void onPostExecute(String result) {

            if (getActivity()==null)
                return;

            dialog.dismiss();
            if (result.equals("success")){
                cardArrayAdapter.refresh();
                items.clear();
                refreshing=false;
            }
            else if (result.equals("error")){
                resume=true;
                if (visible==true)
                    getActivity().getSupportFragmentManager().beginTransaction()
                        .replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();
                Toast.makeText(getContext(), "Please Check your Network Connection", Toast.LENGTH_SHORT).show();
            }
            else
                Toast.makeText(getContext(), "Sorry! Unable to load articles", Toast.LENGTH_SHORT).show();
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
                    SimpleDateFormat inputDate=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                    SimpleDateFormat outputDate=new SimpleDateFormat("d MMM, yyyy");
                    try {
                        Date input=inputDate.parse(model.date);
                        model.date=outputDate.format(input);
                    } catch (ParseException e) {
                        e.printStackTrace();
                    }
                    model.id = Integer.parseInt(object.getString("id"));
                    model.group_username=object.getString("group_username");
                    model.slug=object.getString("slug");
                    model.student=object.getBoolean("student");
                    if (model.student)
                        model.group_username="students";
                    model.setCategory();
                    if (object.has("thumbnail"))
                        model.imageurl=object.getString("thumbnail");
                    else
                        model.imageurl=null;

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
            if (items.size()==0 ) {
                listView.removeFooterView(tv);
                if (cardList.size()==0){
                    listView.addHeaderView(noblog);
                }
                Toast.makeText(getContext(), "No More Blogs", Toast.LENGTH_SHORT).show();
            }
            else {
                listView.removeHeaderView(noblog);
                this.cardList.addAll(items);
                if (listView.getFooterViewsCount()==0)
                    listView.addFooterView(tv);
                notifyDataSetChanged();
            }

        }
        @Override
        public void clear(){
            this.cardList.clear();
            if (listView.getFooterViewsCount()==0)
                listView.addFooterView(tv);
            notifyDataSetChanged();
            super.clear();
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
            final BlogCardViewHolder viewHolder;
            int screen_width=getActivity().getWindowManager().getDefaultDisplay().getWidth();
            if (row == null) {
                LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                row = inflater.inflate(R.layout.list_blog_card, parent, false);
                row.getLayoutParams().height=screen_width;
                viewHolder = new BlogCardViewHolder();
                viewHolder.img= (ImageView) row.findViewById(R.id.blog_img);
                viewHolder.topic= (TextView) row.findViewById(R.id.topic);
                viewHolder.date= (TextView) row.findViewById(R.id.date);
                viewHolder.description= (TextView) row.findViewById(R.id.description);
                viewHolder.dp= (ImageView) row.findViewById(R.id.blog_dp);
                viewHolder.category= (TextView) row.findViewById(R.id.category);
                viewHolder.group= (TextView) row.findViewById(R.id.group);
            } else {
                viewHolder = (BlogCardViewHolder)row.getTag();
            }
            final BlogModel card = getItem(position);

            viewHolder.id=card.id;
            viewHolder.topic.setText(card.topic);
            viewHolder.description.setText(card.desc);
            viewHolder.group.setText(card.group);
            viewHolder.date.setText(card.date);
            viewHolder.category.setText(card.category);
            viewHolder.blogUrl=BlogUrl+card.group_username+"/"+card.slug;

            int dpHolder;
            if (card.student)
                dpHolder = R.drawable.ic_person_black_24dp;
            else
                dpHolder = R.drawable.ic_group_black_24dp;

            imageDownloader.getImage(hostURL + card.dpurl,viewHolder.dp
                    ,(int) getResources().getDimension(R.dimen.roundimage_length),(int) getResources().getDimension(R.dimen.roundimage_length),dpHolder);

            if (card.imageurl!=null) {
                row.findViewById(R.id.card_middle).setVisibility(View.GONE);
                row.findViewById(R.id.img_layout).setVisibility(View.VISIBLE);
                imageDownloader.getImage(hostURL + card.imageurl
                        , viewHolder.img,screen_width,screen_width,R.drawable.loading);
            }
            else {
                row.findViewById(R.id.img_layout).setVisibility(View.GONE);
                row.findViewById(R.id.card_middle).setVisibility(View.VISIBLE);

            }
            View.OnClickListener rowClickListener=new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    getActivity().getSupportFragmentManager().beginTransaction()
                            .replace(R.id.container, new BlogWebView(viewHolder.blogUrl)).addToBackStack(null).commit();

                }
            };
            row.setOnClickListener(rowClickListener);

            if (card.student)
                row.findViewById(R.id.card_bottom).setOnClickListener(rowClickListener);

            else {
                row.findViewById(R.id.card_bottom).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        if (!refreshing) {
                            getFragmentManager().beginTransaction()
                                    .replace(R.id.container, new GroupBlogList(card.group_username, card.group)).addToBackStack(null).commit();

                        }
                    }
                });
            }

            row.setTag(viewHolder);
            return row;
        }

    }

    @TargetApi(Build.VERSION_CODES.JELLY_BEAN_MR1)
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater)
    {
        flag=false;
        menu.clear();
        inflater.inflate(R.menu.menu_blogs,menu);
        final MenuItem item=menu.findItem(R.id.filter_spinner);
        Spinner spinner= (Spinner) MenuItemCompat.getActionView(item);
        ArrayAdapter<CharSequence> filters=ArrayAdapter.createFromResource(getContext(),R.array.filters, R.layout.spinner_item);
        filters.setDropDownViewResource(R.layout.spinner_dropdown_item);
        spinner.setAdapter(filters);
        spinner.setGravity(Gravity.RIGHT);
        spinner.setBackground(getResources().getDrawable(R.drawable.spinner_bg));
        spinner.setPopupBackgroundDrawable(getResources().getDrawable(R.drawable.spinner_dropdown_background));
        spinner.setPadding(0,0,(int) getResources().getDimension(R.dimen.spinner_padding),0);
        spinner.setSelection(spinnerPos);
        spinner.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                flag=true;
                return false;
            }
        });

        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                spinnerPos=position;
                if (flag || resume) {
                    if (isConnected()){
                        cardArrayAdapter.clear();
                        switch (position) {
                            case 1:
                                url = BlogUrl + "iitr/";
                                blogsCount = 0;
                                new LoadBlogTask().execute();
                                break;
                            case 2:
                                url = BlogUrl + "groups/";
                                blogsCount = 0;
                                new LoadBlogTask().execute();
                                break;
                            case 3:
                                url= BlogUrl + "students/";
                                blogsCount =0;
                                new LoadBlogTask().execute();
                                break;
                            default:
                                url = BlogUrl;
                                blogsCount = 0;
                                new LoadBlogTask().execute();
                                break;
                        }
                        flag = false;
                        resume=false;
                    }
                    else
                        getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new NetworkErrorFragment()).addToBackStack(null).commit();

                }

            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });
    }
    @Override
    public void onResume(){
        visible=true;
        super.onResume();
    }
    @Override
    public void onPause(){
        visible=false;
        super.onPause();
    }

}
