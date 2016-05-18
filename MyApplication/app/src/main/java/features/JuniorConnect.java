package features;


import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTabHost;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import img.myapplication.NavigationStudent;
import img.myapplication.R;

/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class JuniorConnect extends Fragment {

    private String sess_id;
    public JuniorConnect(String sess_id) {
        this.sess_id=sess_id;
        // Required empty public constructor
    }

    

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        ((NavigationStudent)getActivity()).setActionBarTitle("Junior Connect");
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_junior_connect, container, false);
        FragmentTabHost mTabHost = (FragmentTabHost)view.findViewById(R.id.my_jtabhost);
        mTabHost.setup(getActivity(), getChildFragmentManager(), R.layout.fragment_junior_connect);

        Bundle arg = new Bundle();
        arg.putString("sess_id", sess_id);
        mTabHost.addTab(mTabHost.newTabSpec("pending").setIndicator("Pending"),
                JuniorConnectPending.class, arg);
        mTabHost.addTab(mTabHost.newTabSpec("accepted").setIndicator("Accepted"),
                JuniorConnectAccepted.class, arg);
        return view;
    }


}
