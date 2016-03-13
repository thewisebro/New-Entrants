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

import java.util.HashMap;
import java.util.Map;

import features.BlogPage;
import features.BlogsFragment;
import features.JuniorConnect;
import features.ProfileFragment;
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
    private Map<String,String> userParams;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        setContentView(R.layout.activity_navigation);
        db=new MySQLiteHelper(this);
        student=db.getStudent();
        userParams=new HashMap<String,String>();
        userParams.put("sess_id",student.sess_id);
        userParams.put("category", "student");

        mCurrentPosition=-1;
        fragmentCount=0;
        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        mNavigationDrawerFragment.set(2);
        mNavigationDrawerFragment.setUp(R.id.navigation_drawer, (DrawerLayout) findViewById(R.id.drawer_layout));


        if(!isConnected()){
            Toast.makeText(getApplicationContext(), "NOT CONNECTED", Toast.LENGTH_SHORT).show();
        }
    }
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }
    public void TryAgain(){
        if (isConnected()){
            getSupportFragmentManager().beginTransaction().replace(R.id.container,new OpeningFragment()).commit();
        }
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
    }
    @Override
    public void onNavigationDrawerItemSelected(int position) {
        Fragment fragment = null;
        mCurrentPosition=position;

        if (isConnected()){
            switch(position) {
                case -1: fragment = new OpeningFragment();
                    break;
                case 1:fragment = new BlogsFragment();
                    break;
                case 2: fragment=new JuniorConnect(userParams.get("sess_id"));
                    break;
                case 3: logout();
                    break;
                default:fragment=new ProfileFragment(student,student.category);

            }
        }
        else {
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
