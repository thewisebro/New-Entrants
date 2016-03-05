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
import android.widget.EditText;
import android.widget.Toast;

import java.util.HashMap;
import java.util.Map;

import features.BlogPage;
import features.BlogsFragment;
import features.EditInfoFragment;
import features.PConnectFragment;
import features.PeerPage;
import features.RequestSenior;
import features.SConnectFragment;
import features.SeniorPage;
import models.BlogCardViewHolder;
import models.NewEntrantModel;
import models.PeerCardViewHolder;
import models.SeniorCardViewHolder;


public class Navigation extends ActionBarActivity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {
    private int fragmentCount;
    public NewEntrantModel entrant;
    private NavigationDrawerFragment mNavigationDrawerFragment;
    private int mCurrentPosition;
    private CharSequence mTitle;
    private MySQLiteHelper db;
    public Map<String,String> userParams;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        setContentView(R.layout.activity_navigation);
        mCurrentPosition=-1;
        fragmentCount=0;
        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        mNavigationDrawerFragment.set(1);
        db=new MySQLiteHelper(this);
        entrant=db.getEntrant();
        userParams=new HashMap<String,String>();
        userParams.put("state",entrant.state);
        userParams.put("branchcode",entrant.branchcode);
        userParams.put("category","entrant");
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
    public void logout(){
        db.deleteEntrant();
        db.deleteBlogs();
        db.deleteSeniors();
        Intent intent=new Intent(this, Login.class);
        startActivity(intent);
        finish();
    }
    public void displayBlog(View view){
       BlogCardViewHolder viewHolder=(BlogCardViewHolder) view.getTag();
        loadFragment(new BlogPage(viewHolder.blogUrl));
    }
    public void displayPeer(View view){
        PeerCardViewHolder viewHolder=(PeerCardViewHolder) view.getTag();
        loadFragment(new PeerPage(viewHolder.model));
    }
    public void displaySenior(View view){
        SeniorCardViewHolder viewHolder=(SeniorCardViewHolder) view.getTag();
        loadFragment(new SeniorPage(viewHolder.model));
    }
    public void requestSenior(View view){
        loadFragment(new RequestSenior());
    }
    public void TryAgain(){
        if (isConnected()){
            getSupportFragmentManager().beginTransaction().replace(R.id.container,new OpeningFragment()).commit();
        }
    }
    @Override
    public void onNavigationDrawerItemSelected(int position) {
        Fragment fragment = null;
        mCurrentPosition=position;
        //if (isConnected()){
            switch(position) {
                case -1: fragment = new OpeningFragment();
                    break;
                case 1:fragment = new BlogsFragment();
                    break;
                case 2:fragment = new PConnectFragment();
                    break;
                case 3:fragment = new SConnectFragment(userParams);
                    break;

                case 4: logout();
                    break;
                default: fragment=new EditInfoFragment(entrant);
                    break;
            }

       /*else {
            fragment= new NetworkErrorFragment();
        }*/

       loadFragment(fragment);


    }
    public void loadFragment(Fragment fragment){
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
    public void update(View view) {
        EditText et_email = (EditText) findViewById(R.id.edit_email);
        EditText et_number = (EditText) findViewById(R.id.edit_number);

        entrant.email = et_email.getText().toString();
        entrant.mobile = et_number.getText().toString();

        if(db.updateEntrant(entrant)>0){
            Toast.makeText(getApplicationContext(), "Updated", Toast.LENGTH_SHORT).show();
        }
        else if(db.updateEntrant(entrant)==0){
            Toast.makeText(getApplicationContext(),"No update", Toast.LENGTH_SHORT).show();
        }
    }
    public void getPageTitle(){

        String[] mTitleArray = getResources().getStringArray(R.array.tabs);
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

       if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }



}
