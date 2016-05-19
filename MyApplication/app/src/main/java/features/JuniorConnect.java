package features;


import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTabHost;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TabHost;

import img.myapplication.NavigationStudent;
import img.myapplication.R;

/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class JuniorConnect extends Fragment {

    FragmentTabHost mTabHost;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ((NavigationStudent)getActivity()).setActionBarTitle("Junior Connect");
        setHasOptionsMenu(true);
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_junior_connect, container, false);
        mTabHost = (FragmentTabHost)view.findViewById(R.id.my_jtabhost);
        mTabHost.setup(getActivity(), getChildFragmentManager(), R.layout.fragment_junior_connect);

        mTabHost.addTab(mTabHost.newTabSpec("pending").setIndicator("Pending"),
                JuniorConnectPending.class, null);
        mTabHost.addTab(mTabHost.newTabSpec("accepted").setIndicator("Accepted"),
                JuniorConnectAccepted.class, null);
        setTabColor();
        mTabHost.setOnTabChangedListener(new TabHost.OnTabChangeListener() {
            @Override
            public void onTabChanged(String tabId) {
                setTabColor();
            }
        });
        return view;
    }
    private void setTabColor(){
        for (int i = 0; i < mTabHost.getTabWidget().getChildCount(); i++) {
            mTabHost.getTabWidget().getChildAt(i).setBackgroundColor(getResources().getColor(R.color.tab_unselected)); //unselected
        }
        mTabHost.getTabWidget().getChildAt(mTabHost.getCurrentTab()).setBackgroundColor(getResources().getColor(R.color.tab_selected)); // selected

    }
    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        menu.clear();
        inflater.inflate(R.menu.menu_connect, menu);
    }
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {

        switch (item.getItemId()) {
            case R.id.list_update:
                getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container, new JuniorConnectLoading()).commit();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }
}