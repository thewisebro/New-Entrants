package img.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.support.v4.app.ActionBarDrawerToggle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;


public class NavigationStudent extends ActionBarActivity {

    private StudentModel student;
    private NavigationDrawerFragment mNavigationDrawerFragment;
    private int mCurrentPosition;
    private CharSequence mTitle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation_student);
        mCurrentPosition=-1;
        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        // mTitle = getTitle();
        student=(StudentModel) getIntent().getSerializableExtra("user");
        mNavigationDrawerFragment.setUp(R.id.navigation_drawer, (DrawerLayout) findViewById(R.id.drawer_layout));
    }
    public void logout(){
        Intent intent=new Intent(this, Login.class);
        startActivity(intent);
        finish();
    }
    public void displayBlog(View view){

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
            case 2:fragment = new RequestsFragment();
                break;
            case 3:fragment=new EditStudent(student);
            case 4: logout();
                break;
            default: fragment=new StudentProfile(student);
                break;
        }
        getSupportFragmentManager().beginTransaction().replace(R.id.container, fragment).commit();


    }
    public void update(View view) {
        MySQLiteHelper db = new MySQLiteHelper(this);


        EditText et_email = (EditText) findViewById(R.id.edit_email);
        EditText et_number = (EditText) findViewById(R.id.edit_number);

        user.Email = et_email.getText().toString();
        user.Mobile = et_number.getText().toString();

        if(db.updateUser(user)>0){
            Toast.makeText(getApplicationContext(), "Updated", Toast.LENGTH_SHORT).show();
        }
        else if(db.updateUser(user)==0){
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

    public static class NavigationDrawerFragment extends Fragment {
        private static final String STATE_SELECTED_POSITION = "selected_navigation_drawer_position";

        private static final String PREF_USER_LEARNED_DRAWER = "navigation_drawer_learned";

        private NavigationDrawerCallbacks mCallbacks;

        private ActionBarDrawerToggle mDrawerToggle;

        private DrawerLayout mDrawerLayout;
        private ListView mDrawerListView;
        private View mFragmentContainerView;

        private int mCurrentSelectedPosition = -1;
        private boolean mFromSavedInstanceState;
        private boolean mUserLearnedDrawer;

        public NavigationDrawerFragment() {
        }

        @Override
        public void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(getActivity());
            mUserLearnedDrawer = sp.getBoolean(PREF_USER_LEARNED_DRAWER, false);

            if (savedInstanceState != null) {
                mCurrentSelectedPosition = savedInstanceState.getInt(STATE_SELECTED_POSITION);
                mFromSavedInstanceState = true;
            }

            selectItem(mCurrentSelectedPosition);
        }

        @Override
        public void onActivityCreated(Bundle savedInstanceState) {
            super.onActivityCreated(savedInstanceState);
            setHasOptionsMenu(true);
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {
            mDrawerListView = (ListView) inflater.inflate(
                    R.layout.fragment_navigation_drawer, container, false);
            mDrawerListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    selectItem(position);

                }
            });
            mDrawerListView.setAdapter(new ArrayAdapter<String>(
                    getActionBar().getThemedContext(),
                    android.R.layout.simple_list_item_activated_1,
                    android.R.id.text1,
                    getResources().getStringArray(R.array.tabs)
            ));
            mDrawerListView.setItemChecked(mCurrentSelectedPosition, true);
            return mDrawerListView;
        }

        public boolean isDrawerOpen() {
            return mDrawerLayout != null && mDrawerLayout.isDrawerOpen(mFragmentContainerView);
        }

        public void setUp(int fragmentId, DrawerLayout drawerLayout) {
            mFragmentContainerView = getActivity().findViewById(fragmentId);
            mDrawerLayout = drawerLayout;

            mDrawerLayout.setDrawerShadow(R.drawable.drawer_shadow, GravityCompat.START);

            ActionBar actionBar = getActionBar();
            actionBar.setDisplayHomeAsUpEnabled(true);
            actionBar.setHomeButtonEnabled(true);

            mDrawerToggle = new ActionBarDrawerToggle(
                    getActivity(),                    /* host Activity */
                    mDrawerLayout,                    /* DrawerLayout object */
                    R.drawable.ic_drawer,             /* nav drawer image to replace 'Up' caret */
                    R.string.navigation_drawer_open,  /* "open drawer" description for accessibility */
                    R.string.navigation_drawer_close  /* "close drawer" description for accessibility */
            ) {
                @Override
                public void onDrawerClosed(View drawerView) {
                    super.onDrawerClosed(drawerView);
                    if (!isAdded()) {
                        return;
                    }

                    getActivity().supportInvalidateOptionsMenu(); // calls onPrepareOptionsMenu()
                }

                @Override
                public void onDrawerOpened(View drawerView) {
                    super.onDrawerOpened(drawerView);
                    if (!isAdded()) {
                        return;
                    }

                    if (!mUserLearnedDrawer) {

                        mUserLearnedDrawer = true;
                        SharedPreferences sp = PreferenceManager
                                .getDefaultSharedPreferences(getActivity());
                        sp.edit().putBoolean(PREF_USER_LEARNED_DRAWER, true).apply();
                    }

                    getActivity().supportInvalidateOptionsMenu(); // calls onPrepareOptionsMenu()
                }
            };

            if (!mUserLearnedDrawer && !mFromSavedInstanceState) {
                mDrawerLayout.openDrawer(mFragmentContainerView);
            }

            mDrawerLayout.post(new Runnable() {
                @Override
                public void run() {
                    mDrawerToggle.syncState();
                }
            });

            mDrawerLayout.setDrawerListener(mDrawerToggle);
        }

        private void selectItem(int position) {
            mCurrentSelectedPosition = position;

            if (mDrawerListView != null) {
                mDrawerListView.setItemChecked(position, true);
            }
            if (mDrawerLayout != null) {
                mDrawerLayout.closeDrawer(mFragmentContainerView);
            }
            if (mCallbacks != null) {
                mCallbacks.onNavigationDrawerItemSelected(position);
            }
        }

        @Override
        public void onAttach(Activity activity) {
            super.onAttach(activity);
            try {
                mCallbacks = (NavigationDrawerCallbacks) activity;
            } catch (ClassCastException e) {
                throw new ClassCastException("Activity must implement NavigationDrawerCallbacks.");
            }
        }

        @Override
        public void onDetach() {
            super.onDetach();
            mCallbacks = null;
        }

        @Override
        public void onSaveInstanceState(Bundle outState) {
            super.onSaveInstanceState(outState);
            outState.putInt(STATE_SELECTED_POSITION, mCurrentSelectedPosition);
        }

        @Override
        public void onConfigurationChanged(Configuration newConfig) {
            super.onConfigurationChanged(newConfig);

            mDrawerToggle.onConfigurationChanged(newConfig);
        }

        @Override
        public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {

            if (mDrawerLayout != null && isDrawerOpen()) {
                inflater.inflate(R.menu.global, menu);
                showGlobalContextActionBar();
            }
            super.onCreateOptionsMenu(menu, inflater);
        }

        @Override
        public boolean onOptionsItemSelected(MenuItem item) {
            if (mDrawerToggle.onOptionsItemSelected(item)) {
                return true;
            }


            return super.onOptionsItemSelected(item);
        }

        private void showGlobalContextActionBar() {
            ActionBar actionBar = getActionBar();
            actionBar.setDisplayShowTitleEnabled(true);
            actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_STANDARD);
            actionBar.setTitle(R.string.app_name);
        }

        private ActionBar getActionBar() {
            return ((ActionBarActivity) getActivity()).getSupportActionBar();
        }

        public static interface NavigationDrawerCallbacks {
            /**
             * Called when an item in the navigation drawer is selected.
             */
            void onNavigationDrawerItemSelected(int position);
        }
    }

}
