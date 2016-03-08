package features;


import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.Map;

import img.myapplication.R;

/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class SConnectTabFragment extends Fragment {

private Map<String,String> userParams;
    public SConnectTabFragment(Map<String,String> params){
        this.userParams=params;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_sconnect_tab, container, false);
        ViewPager pager= (ViewPager) view.findViewById(R.id.pager);
        pager.setAdapter(new FragmentPagerAdapter(getFragmentManager()) {
            @Override
            public Fragment getItem(int position) {
                Fragment fragment=null;
                if (position==1)
                    fragment=new SConnectAcceptFragment();
                else
                    fragment=new SConnectFragment(userParams);
                return fragment;
            }

            @Override
            public int getCount() {
                return 2;
            }
            @Override
            public CharSequence getPageTitle(int position) {
                String title=null;
                if (position==0)
                    title="Request";
                else
                    title="Accept";
                return title;
            }
        });

        return view;
    }


}
