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

import features.BlogsList;
import features.EntrantUpdateFragment;
import features.SConnectRequestFragment;
import features.SConnectTabFragment;
import models.NewEntrantModel;


public class Navigation extends ActionBarActivity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {
    private int fragmentCount;
    public NewEntrantModel entrant;
    private NavigationDrawerFragment mNavigationDrawerFragment;
    private int mCurrentPosition;
    private CharSequence mTitle;
    private MySQLiteHelper db;
    private boolean updated=false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        setContentView(R.layout.activity_navigation);
        db=new MySQLiteHelper(this);
        entrant=db.getEntrant();
        mCurrentPosition=-1;
        fragmentCount=0;
        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        mNavigationDrawerFragment.set(1);

        mNavigationDrawerFragment.setUp(R.id.navigation_drawer, (DrawerLayout) findViewById(R.id.drawer_layout));
    }

 public boolean isConnected(){
     ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
     NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
     if (networkInfo != null && networkInfo.isConnected())
         return true;
     else
         return false;
 }

    public boolean get_update_status(){ return this.updated;}
    public void set_updated(){ this.updated=true;}
    public void reset_updated(){this.updated=false;}
    public void logout(){
        db.deleteEntrant();
        Intent intent=new Intent(this, Login.class);
        startActivity(intent);
        finish();
    }

    public void sendRequest(View view){
        loadFragment(new SConnectRequestFragment());
    }
    @Override
    public void onNavigationDrawerItemSelected(int position) {
        Fragment fragment = null;
        mCurrentPosition=position;

            switch (position) {
                case -1:
                    fragment = new OpeningFragment();
                    break;
                case 1:
                    fragment = new SConnectTabFragment();
                    break;
                case 2:
                    fragment=new SConnectRequestFragment();
                    break;
                case 4:
                    logout();
                    break;
                case 3:
                    fragment = new EntrantUpdateFragment();
                    break;
                default:
                    fragment = new BlogsList();
                    break;
            }

       loadFragment(fragment);

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
    public void setActionBarTitle(String title) {
        getSupportActionBar().setTitle(title);
    }
    public void getPageTitle(){

        String[] mTitleArray = getResources().getStringArray(R.array.entrantstabs);
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
