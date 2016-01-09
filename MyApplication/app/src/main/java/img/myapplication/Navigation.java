package img.myapplication;

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


public class Navigation extends ActionBarActivity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {

    private NewEntrantModel entrant;
    private NavigationDrawerFragment mNavigationDrawerFragment;
    private int mCurrentPosition;
    private CharSequence mTitle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);
        mCurrentPosition=-1;
        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        mNavigationDrawerFragment.set(1);
       // mTitle = getTitle();
        entrant=(NewEntrantModel) getIntent().getSerializableExtra("entrant");
        mNavigationDrawerFragment.setUp(R.id.navigation_drawer, (DrawerLayout) findViewById(R.id.drawer_layout));
    }
    public void logout(){

    }
    public void displayBlog(View view){
       // Toast.makeText(this, "Invalid valid email address", Toast.LENGTH_SHORT).show();
       BlogCardViewHolder viewHolder=(BlogCardViewHolder) view.getTag();
       getSupportFragmentManager().beginTransaction().replace(R.id.container,new BlogPage(viewHolder.model)).commit();
    }
    public void displayPeer(View view){
        PeerCardViewHolder viewHolder=(PeerCardViewHolder) view.getTag();
        getSupportFragmentManager().beginTransaction().replace(R.id.container,new PeerPage(viewHolder.model)).commit();
    }
    public void displaySenior(View view){
        SeniorCardViewHolder viewHolder=(SeniorCardViewHolder) view.getTag();
        getSupportFragmentManager().beginTransaction().replace(R.id.container,new SeniorPage(viewHolder.model)).commit();
    }
    public void requestSenior(View view){
        getSupportFragmentManager().beginTransaction().replace(R.id.container,new RequestSenior()).commit();
    }
    public void request(View view){

    }
    @Override
    public void onNavigationDrawerItemSelected(int position) {
        Fragment fragment = null;
        mCurrentPosition=position;
        //FragmentManager fragmentManager = getSupportFragmentManager();
        switch(position) {
            case -1: fragment = new OpeningFragment();
                break;
            case 1:fragment = new BlogsFragment();
                 break;
            case 2:fragment = new PConnectFragment();
                break;
            case 3:fragment = new SConnectFragment();
                break;

            case 5: logout();
                break;
            default: fragment=new EditInfoFragment(entrant);
                break;
        }
       getSupportFragmentManager().beginTransaction().replace(R.id.container, fragment).commit();


    }
    public void update(View view) {
        MySQLiteHelper db = new MySQLiteHelper(this);


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
