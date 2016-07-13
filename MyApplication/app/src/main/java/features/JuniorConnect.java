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
import android.widget.TextView;

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
        ((NavigationStudent) getActivity()).getSupportActionBar().show();
        ((NavigationStudent)getActivity()).setActionBarTitle(getString(R.string.title_jconnect));
        setHasOptionsMenu(true);
        View view= inflater.inflate(R.layout.fragment_junior_connect, container, false);
        mTabHost = (FragmentTabHost)view.findViewById(R.id.my_jtabhost);
        mTabHost.setup(getActivity(), getChildFragmentManager(), R.layout.fragment_junior_connect);

        mTabHost.addTab(mTabHost.newTabSpec("pending").setIndicator(getTabView("Pending")),
                JuniorConnectPending.class, null);
        mTabHost.addTab(mTabHost.newTabSpec("accepted").setIndicator(getTabView("Accepted")),
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
    private TextView getTabView(String title){
        TextView view= (TextView) LayoutInflater.from(getContext()).inflate(R.layout.tabview,null);
        view.setText(title);
        return view;
    }
    private void setTabColor(){
        for(int i=0;i<mTabHost.getTabWidget().getChildCount();i++) {
            TextView tab= (TextView) mTabHost.getTabWidget().getChildTabViewAt(i);
            tab.setTextColor(getResources().getColor(R.color.blue_grey_300));
        }
        TextView currentTab= (TextView) mTabHost.getTabWidget().getChildTabViewAt(mTabHost.getCurrentTab());
        currentTab.setTextColor(getResources().getColor(R.color.yellow_700));
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