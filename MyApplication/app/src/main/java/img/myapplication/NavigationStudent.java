package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import java.net.HttpURLConnection;
import java.net.URL;

import features.BlogPage;
import features.BlogsFragment;
import features.JuniorConnect;
import features.StudentUpdateFragment;
import models.BlogCardViewHolder;
import models.StudentModel;


public class NavigationStudent extends ActionBarActivity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {
    private int fragmentCount;
    private MySQLiteHelper db;
    public StudentModel student;
    private NavigationDrawerFragment mNavigationDrawerFragment;
    private int mCurrentPosition;
    private CharSequence mTitle;
    private boolean lock=false;
    private boolean updated=false;
    private String appURL="http://192.168.121.187:8080/new_entrants/";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        setContentView(R.layout.activity_navigation);
        db=new MySQLiteHelper(this);
        student=db.getStudent();

        mCurrentPosition=-1;
        fragmentCount=0;
        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        mNavigationDrawerFragment.set(2);
        mNavigationDrawerFragment.setUp(R.id.navigation_drawer, (DrawerLayout) findViewById(R.id.drawer_layout));

        checkforUpdate();
    }
    public boolean get_update_status(){ return this.updated;}
    public void set_updated(){ this.updated=true;}
    public void reset_updated(){this.updated=false;}
    public void checkforUpdate() {
        if ("".equals(student.town) || "".equals(student.state) || "".equals(student.email) || "".equals(student.mobile)){
            StudentUpdateFragment fragment=new StudentUpdateFragment();
            lock=true;
            fragment.lock=true;
            getSupportFragmentManager().beginTransaction().replace(R.id.container,fragment).commit();
        }
    }
/*    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }*/
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected()){
            try {
                HttpURLConnection connection= (HttpURLConnection) new URL(appURL).openConnection();
                connection.setConnectTimeout(5000);
                connection.setReadTimeout(5000);
                int rcode=connection.getResponseCode();
                if (rcode== HttpURLConnection.HTTP_OK || rcode==HttpURLConnection.HTTP_ACCEPTED)
                    return true;
                else {
                    if (rcode==HttpURLConnection.HTTP_SERVER_ERROR){
                        Toast.makeText(getApplicationContext(), "SERVER-SIDE NETWORK ERROR!", Toast.LENGTH_SHORT).show();
                        return false;
                    }
                    else{
                        Toast.makeText(getApplicationContext(), "NETWORK ERROR", Toast.LENGTH_SHORT).show();
                        return false;
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(getApplicationContext(), "NETWORK ERROR", Toast.LENGTH_SHORT).show();
                return false;

            }
        }
        else
            Toast.makeText(getApplicationContext(), "NOT CONNECTED", Toast.LENGTH_SHORT).show();
        return false;
    }
    public void logout(){
        db.deleteStudent();
        Intent intent=new Intent(this, Login.class);
        startActivity(intent);
        finish();
    }
    public void displayBlog(View view){
        BlogCardViewHolder viewHolder=(BlogCardViewHolder) view.getTag();
        loadFragment(new BlogPage(viewHolder.blogUrl));
    }
    public void loadFragment(Fragment fragment){
        if (fragment == null)
            return;
        if (fragmentCount!=0)
            getSupportFragmentManager().beginTransaction().replace(R.id.container, fragment).addToBackStack(null).commit();
        else
            getSupportFragmentManager().beginTransaction().replace(R.id.container,fragment).commit();
        fragmentCount++;
    }
    @Override
    public void onBackPressed(){
        if (getSupportFragmentManager().getBackStackEntryCount()!=0){
            getSupportFragmentManager().popBackStack();
        }
        else
            return;
    }
    @Override
    public void onNavigationDrawerItemSelected(int position) {
        Fragment fragment = null;
        mCurrentPosition=position;

        if (isConnected()){
            switch(position) {
                case -1: fragment = new OpeningFragment();
                    break;
                case 0:fragment = new BlogsFragment();
                    break;
                case 1: fragment=new JuniorConnect(student.sess_id);
                    break;
                case 3: logout();
                    break;
                default: fragment= new StudentUpdateFragment();

            }
        }
        else {
            if (position==3)
                logout();
            else
                fragment=new NetworkErrorFragment();
        }
        loadFragment(fragment);
    }

    public void getPageTitle(){

        String[] mTitleArray = getResources().getStringArray(R.array.studenttabs);
        mTitle=mTitleArray[mCurrentPosition];
    }

    public void restoreActionBar() {
        if(mCurrentPosition != -1)
            getPageTitle();
        else mTitle="Welcome";
        ActionBar actionBar = getSupportActionBar();
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_STANDARD);
        actionBar.setDisplayShowTitleEnabled(true);
        actionBar.setTitle(mTitle);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        if (!mNavigationDrawerFragment.isDrawerOpen()) {

            getMenuInflater().inflate(R.menu.navigation, menu);
            restoreActionBar();
            return true;
        }
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {

        int id = item.getItemId();

        return super.onOptionsItemSelected(item);
    }



}
