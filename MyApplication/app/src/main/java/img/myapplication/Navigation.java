package img.myapplication;

import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;


public class Navigation extends ActionBarActivity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {


    private NavigationDrawerFragment mNavigationDrawerFragment;
    private int mCurrentPosition;
    private CharSequence mTitle;
    private String Enr_No;
    public class USER_DATA{
        public String name;
        public String enr;
        public String email;
        public String mobile;

    };
    public USER_DATA user;
    private Cursor result;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);

        Intent intent_call= getIntent();
        Enr_No=intent_call.getStringExtra("EXTRA_ENR");
        SQLiteDatabase db= openOrCreateDatabase("Entrants_Data", MODE_PRIVATE, null);
        result=db.rawQuery("select * from Entrants where Enr_No='"+Enr_No+"';",null);
        user=null;
      /*  if (result.moveToFirst()){
            user.name=result.getString(result.getColumnIndex("Name"));
            user.enr=result.getString(result.getColumnIndex("Enr_No"));
            user.email=result.getString(result.getColumnIndex("Email"));
            user.mobile=result.getString(result.getColumnIndex("Mobile_No"));
        }*/
        mCurrentPosition=-1;
        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
       // mTitle = getTitle();

        mNavigationDrawerFragment.setUp(R.id.navigation_drawer, (DrawerLayout) findViewById(R.id.drawer_layout));
    }

    @Override
    public void onNavigationDrawerItemSelected(int position) {
        Fragment fragment;
        mCurrentPosition=position;
        FragmentManager fragmentManager = getSupportFragmentManager();
        switch(position) {
            case -1: fragment = new OpeningFragment();
                break;
            case 1:fragment = new BlogsFragment();
                 break;
            case 3:fragment = new SConnectFragment();
                break;
            case 2:fragment = new PConnectFragment();
                break;
            case 4 :fragment= new EditInfoFragment();
                break;

            default: fragment=new ProfileFragment(result);
                break;
        }
       fragmentManager.beginTransaction().replace(R.id.container, fragment).commit();


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
