package img.myapplication;

import android.app.Activity;
import android.content.Intent;
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


public class NavigationStudent extends ActionBarActivity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {
    private int fragmentCount;
    public StudentModel student;
    private NavigationDrawerFragment mNavigationDrawerFragment;
    private int mCurrentPosition;
    private CharSequence mTitle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);
        mCurrentPosition=-1;
        fragmentCount=0;
        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        mNavigationDrawerFragment.set(2);
        mNavigationDrawerFragment.setUp(R.id.navigation_drawer, (DrawerLayout) findViewById(R.id.drawer_layout));
        // mTitle = getTitle();
        student=(StudentModel) getIntent().getSerializableExtra("user");

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
        Intent intent=new Intent(this, LoginActivity.class);
        startActivity(intent);
        finish();
    }
    public void displayBlog(View view){
        BlogCardViewHolder viewHolder=(BlogCardViewHolder) view.getTag();
        loadFragment(new BlogPage(viewHolder.model));
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
    @Override
    public void onNavigationDrawerItemSelected(int position) {
        Fragment fragment = null;
        mCurrentPosition=position;
        //FragmentManager fragmentManager = getSupportFragmentManager();
        if (isConnected()){
            switch(position) {
                case -1: fragment = new OpeningFragment();
                    break;
                case 1:fragment = new BlogsFragment();
                    break;
                case 2: fragment=new RequestsFragment();
                    break;
                case 3: logout();
                    break;
                default:fragment=new ProfileFragment(student);

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

        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }



}
