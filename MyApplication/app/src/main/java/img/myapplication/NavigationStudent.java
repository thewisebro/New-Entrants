package img.myapplication;

import android.app.Activity;
import android.app.AlarmManager;
import android.app.AlertDialog;
import android.app.PendingIntent;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.support.v4.app.Fragment;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;

import features.BlogsList;
import features.JuniorConnectLoading;
import features.StudentUpdateFragment;
import models.StudentModel;


public class NavigationStudent extends ActionBarActivity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {
    private int fragmentCount=0;
    private MySQLiteHelper db;
    public StudentModel student;
    private NavigationDrawerFragment mNavigationDrawerFragment;
    private int mCurrentPosition=-1;
    private CharSequence mTitle;
    private boolean lock=false;
    private boolean updated=false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        setContentView(R.layout.activity_navigation);
        setDrawerOnTop();

        db=new MySQLiteHelper(this);
        student=db.getStudent();

        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        mNavigationDrawerFragment.set(2,getIntent().getBooleanExtra("first_time",true));
        mNavigationDrawerFragment.setUp(R.id.navigation_drawer, (DrawerLayout) findViewById(R.id.drawer_layout));

        checkforUpdate();
    }
    public boolean get_update_status(){ return this.updated;}
    public void set_updated(){ this.updated=true;}
    public void reset_updated(){this.updated=false;}
    public void checkforUpdate() {
        if (student.town==null || "".equals(student.town)
               || student.state==null || "".equals(student.state)
                || student.email==null || "".equals(student.email)
                || student.mobile==null || "".equals(student.mobile)){
            StudentUpdateFragment fragment=new StudentUpdateFragment();
            lock=true;
            fragment.lock=true;
            getSupportFragmentManager().beginTransaction().replace(R.id.container,fragment).commit();
        }
    }
    public void  setDrawerOnTop(){
        // Inflate the "decor.xml"
        LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        DrawerLayout drawer = (DrawerLayout) inflater.inflate(R.layout.drawer, null); // "null" is important.

        // HACK: "steal" the first child of decor view
        ViewGroup decor = (ViewGroup) getWindow().getDecorView();
        View child = decor.getChildAt(0);
        decor.removeView(child);
        FrameLayout container = (FrameLayout) drawer.findViewById(R.id.container_drawer); // This is the container we defined just now.
        container.addView(child);
        //drawer.setPadding(0,getStatusBarHeight(),0,0);
        (drawer.findViewById(R.id.navigation_drawer)).setPadding(0,getStatusBarHeight(),0,0);
        // Make the drawer replace the first child
        decor.addView(drawer);
    }
    public int getStatusBarHeight() {
        int result = 0;
        int resourceId = getResources().getIdentifier("status_bar_height", "dimen", "android");
        if (resourceId > 0) {
            result = getResources().getDimensionPixelSize(resourceId);
        }
        return result;
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
        final Intent intent = new Intent(this, Login.class);
        final AlertDialog.Builder dialog=new AlertDialog.Builder(this);
        dialog.setTitle("Logout");
        dialog.setMessage("Are you sure you want to Logout?");
        dialog.setPositiveButton("YES", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                db.logoutStudent();
                startActivity(intent);
                finish();
            }
        });
        dialog.setNegativeButton("NO", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });

        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                dialog.show();
            }
        }, 250);
    }

    public void loadFragment(final Fragment fragment){
        if (fragment == null)
            return;
        if (fragmentCount!=0) {
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    getSupportFragmentManager().beginTransaction().replace(R.id.container, fragment).addToBackStack(null).commit();
                }
            }, 250);
        }
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
            logout();
    }
    @Override
    public void onNavigationDrawerItemSelected(int position) {
        Fragment fragment = null;
        mCurrentPosition=position;

            switch(position) {
                case 0: fragment = new BlogsList();
                    break;
                case 1: fragment=new JuniorConnectLoading();
                    break;
                case 2:fragment= new StudentUpdateFragment();
                    break;
                case 4: logout();
                    break;
                default: fragment=new AboutFragment();
            }

        loadFragment(fragment);
    }
    public void setActionBarTitle(String title) {
        getSupportActionBar().setTitle(title);
    }

    public void restoreActionBar() {
        ActionBar actionBar = getSupportActionBar();
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_STANDARD);
        actionBar.setDisplayShowTitleEnabled(true);
        actionBar.setShowHideAnimationEnabled(true);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        if (!mNavigationDrawerFragment.isDrawerOpen()) {

            getMenuInflater().inflate(R.menu.global, menu);
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
    private void  setAlarm(){
        PendingIntent pIntent=PendingIntent.getService(this,0,new Intent(this,NotificationService.class),0);
        AlarmManager am=(AlarmManager) getSystemService(ALARM_SERVICE);
        am.cancel(pIntent);
        am.setInexactRepeating(AlarmManager.ELAPSED_REALTIME_WAKEUP, SystemClock.elapsedRealtime(),
                AlarmManager.INTERVAL_HALF_DAY, pIntent);
    }
    private void cancelAlarm(){
        PendingIntent pIntent=PendingIntent.getService(this,0,new Intent(this,NotificationService.class),0);
        AlarmManager am=(AlarmManager) getSystemService(ALARM_SERVICE);
        am.cancel(pIntent);
    }

    @Override
    public void onResume(){
        super.onResume();
        cancelAlarm();

    }
    @Override
    public void onPause(){
        super.onPause();
        setAlarm();
    }

}
