package features;


import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTabHost;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import img.myapplication.R;

/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class SConnectTabFragment extends Fragment {


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_sconnect_tab, container, false);

        FragmentTabHost mTabHost = (FragmentTabHost)view.findViewById(R.id.my_tabhost);
        mTabHost.setup(getActivity(), getChildFragmentManager(), R.layout.fragment_sconnect_tab);

        mTabHost.addTab(mTabHost.newTabSpec("pending").setIndicator("ALL REQUESTS"),
                SConnectPendingFragment.class, null);
        mTabHost.addTab(mTabHost.newTabSpec("accepted").setIndicator("ACCEPTED"),
                SConnectAcceptFragment.class, null);

        return view;
    }


}
