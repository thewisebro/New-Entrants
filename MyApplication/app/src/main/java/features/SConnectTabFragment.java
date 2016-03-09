package features;


import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTabHost;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TabHost;
import android.widget.Toast;

import java.io.Serializable;
import java.util.Map;

import img.myapplication.R;

/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class SConnectTabFragment extends Fragment {

    private FragmentTabHost mTabHost;

private Map<String,String> userParams;
    public SConnectTabFragment(Map<String,String> params){
        this.userParams=params;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_sconnect_tab, container, false);

        FragmentTabHost mTabHost = (FragmentTabHost)view.findViewById(R.id.my_tabhost);
        mTabHost.setup(getActivity(), getChildFragmentManager(), R.layout.fragment_sconnect_tab);

        Bundle arg = new Bundle();
        arg.putSerializable("userParams", (Serializable) userParams);
        mTabHost.addTab(mTabHost.newTabSpec("request").setIndicator("Request"),
                SConnectFragment.class, arg);
        mTabHost.addTab(mTabHost.newTabSpec("accepted").setIndicator("Accepted"),
                SConnectAcceptFragment.class, null);

        mTabHost.setOnTabChangedListener(new TabHost.OnTabChangeListener() {
            @Override
            public void onTabChanged(String tabId) {
                Toast.makeText(getActivity(), "selected " + tabId, Toast.LENGTH_SHORT).show();
            }
        });

        return view;
    }


}
