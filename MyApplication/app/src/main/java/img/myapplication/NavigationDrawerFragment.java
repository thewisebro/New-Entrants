package img.myapplication;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.preference.PreferenceManager;
import android.support.v4.app.Fragment;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBarDrawerToggle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import models.DrawerItemModel;
import models.NewEntrantModel;
import models.StudentModel;

public class NavigationDrawerFragment extends Fragment {
    private static final String STATE_SELECTED_POSITION = "selected_navigation_drawer_position";

    private static final String PREF_USER_LEARNED_DRAWER = "navigation_drawer_learned";

    private NavigationDrawerCallbacks mCallbacks;

    private ActionBarDrawerToggle mDrawerToggle;

    private DrawerLayout mDrawerLayout;
    private RelativeLayout mDrawerProfileView;
    private ListView mDrawerListView;
    private View mFragmentContainerView;

    private int mCurrentSelectedPosition = -1;
    private boolean mFromSavedInstanceState;
    private boolean mUserLearnedDrawer;
    private int type;

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
        LinearLayout DrawerLayout=(LinearLayout) inflater.inflate(R.layout.fragment_navigation_drawer, container, false);
        mDrawerProfileView= (RelativeLayout) DrawerLayout.findViewById(R.id.profile_view);
        mDrawerListView = (ListView) DrawerLayout.findViewById(R.id.drawer_list);
        //mDrawerListView= (ListView) inflater.inflate(R.layout.navigation_drawer,container,false);
        mDrawerListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, final int position, long id) {
                selectItem(position);

            }
        });
        DrawerLayout.setFitsSystemWindows(true);
        return DrawerLayout;
    }
    public void setProfileView()    {
        String name=null;
        String state=null;
        String branchcode=null;
        String branchname=null;

        MySQLiteHelper db=new MySQLiteHelper(getContext());
        if (type==1){
            NewEntrantModel model=db.getEntrant();
            name=model.name;
            state=model.state;
            ((ImageView) mDrawerProfileView.findViewById(R.id.profile_picture)).setVisibility(View.GONE);
            ((TextView)mDrawerProfileView.findViewById(R.id.name)).setText(name);
            ((TextView)mDrawerProfileView.findViewById(R.id.info)).setText(state);
        }
        else {
            StudentModel model=db.getStudent();
            name=model.name;
            branchcode=model.branchcode;
            branchname=model.branchname;
            if (model.profile_img!=null){
                ((ImageView) mDrawerProfileView.findViewById(R.id.profile_picture))
                        .setImageBitmap(BitmapFactory.decodeByteArray(model.profile_img,0,model.profile_img.length));
            }
            ((TextView)mDrawerProfileView.findViewById(R.id.name)).setText(name);
            ((TextView)mDrawerProfileView.findViewById(R.id.info)).setText(branchcode + ", " + branchname);
        }



    }
    public void set(int type){
       this.type=type;
        //Profile
        setProfileView();
        //List items
        DrawerItemAdapter adapter=new DrawerItemAdapter(getContext(),R.layout.drawer_item);
        ArrayList<DrawerItemModel> arrayList=new ArrayList<DrawerItemModel>();
        String[] tabs=null;
        int[] drawables=null;
        if(type==2) {
            drawables=new int[]{R.drawable.ic_chrome_reader_mode_black_24dp,R.drawable.ic_person_black_24dp ,
                    R.drawable.ic_info_black_24dp,R.drawable.ic_power_settings_new_black_24dp};
            tabs = getResources().getStringArray(R.array.studenttabs);
        }
        if(type==1){
            drawables=new int[]{R.drawable.ic_chrome_reader_mode_black_24dp,R.drawable.ic_group_black_24dp,
                    R.drawable.ic_group_add_black_24dp,R.drawable.ic_info_black_24dp,
                    R.drawable.ic_power_settings_new_black_24dp};
            tabs=getResources().getStringArray(R.array.entrantstabs);
        }

        for (int i=0;i<drawables.length;i++){
            DrawerItemModel model=new DrawerItemModel();
            model.drawable=drawables[i];
            model.string=tabs[i];
            adapter.add(model);
        }

        mDrawerListView.setAdapter(adapter);
        mDrawerListView.setItemChecked(mCurrentSelectedPosition, true);
    }

    public class DrawerItemAdapter extends ArrayAdapter<DrawerItemModel> {

        private List<DrawerItemModel> list = new ArrayList<DrawerItemModel>();

        public DrawerItemAdapter(Context context, int textViewResourceId) {
            super(context, textViewResourceId);
        }

        @Override
        public void add(DrawerItemModel object) {
            list.add(object);
            super.add(object);
        }

        @Override
        public int getCount() {
            return this.list.size();
        }

        @Override
        public DrawerItemModel getItem(int index) {
            return this.list.get(index);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View row = convertView;
            ViewHolder viewHolder;
            if (row == null) {
                LayoutInflater inflater = (LayoutInflater) this.getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                row = inflater.inflate(R.layout.drawer_item, parent, false);
                viewHolder = new ViewHolder();
                viewHolder.drawerIcon= (ImageView) row.findViewById(R.id.drawer_icon);
                viewHolder.drawerItem= (TextView) row.findViewById(R.id.drawer_list_text);

            } else {
                viewHolder = (ViewHolder)row.getTag();
            }
            final DrawerItemModel model = getItem(position);
            viewHolder.drawerIcon.setImageDrawable(getResources().getDrawable(model.drawable));
            viewHolder.drawerItem.setText(model.string);

            row.setTag(viewHolder);
            return row;
        }


        private class ViewHolder {
            public ImageView drawerIcon;
            public TextView drawerItem;
        }
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
        actionBar.setHomeAsUpIndicator(R.drawable.ic_drawer);
        mDrawerToggle=new ActionBarDrawerToggle(
                getActivity(),
                mDrawerLayout,
                R.string.navigation_drawer_open,
                R.string.navigation_drawer_close
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
            public void onDrawerSlide(View drawerView, float slideOffset){

                super.onDrawerSlide(drawerView,slideOffset);
            }
            @Override
            public void onDrawerStateChanged(int newState){
                super.onDrawerStateChanged(newState);
                if (type==1){
                    Navigation activity= (Navigation) getActivity();
                    if (activity.get_update_status()) {
                        setProfileView();
                        activity.reset_updated();
                    }
                }
                else {
                    NavigationStudent activity= (NavigationStudent) getActivity();
                    if (activity.get_update_status()) {
                        setProfileView();
                        activity.reset_updated();
                    }
                }
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
                //getActionBar().hide();
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
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    mCallbacks.onNavigationDrawerItemSelected(mCurrentSelectedPosition);
                }
            }, 250);
            //mCallbacks.onNavigationDrawerItemSelected(position);
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
        //actionBar.setTitle(R.string.app_name);
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
