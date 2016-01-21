package img.myapplication;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

/**
 * A simple {@link Fragment} subclass.
 */
public class ConnectFragment extends Fragment {

    SectionsPagerAdapter mSectionsPagerAdapter;
    ViewPager mViewPager;

    private int pos;
    public ConnectFragment(int i){
        pos=i;
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_connect,container,false);
        mSectionsPagerAdapter = new SectionsPagerAdapter(getFragmentManager());
        mViewPager = (ViewPager) view.findViewById(R.id.pager);
        mViewPager.setAdapter(mSectionsPagerAdapter);
        mViewPager.setCurrentItem(pos);

        return view;
    }

    public class SectionsPagerAdapter extends FragmentPagerAdapter {

        public SectionsPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public android.support.v4.app.Fragment getItem(int position) {
            android.support.v4.app.Fragment fragment = new TabbedContentFragment(position);
            return fragment;
        }

        @Override
        public int getCount() {
            return 2;
        }

        @Override
        public CharSequence getPageTitle(int position) {

            switch (position) {
                case 0:
                    return "Senior Connect";
                case 1:
                    return "Peer Connect";

            }
            return null;
        }
    }

    public static class TabbedContentFragment extends android.support.v4.app.Fragment {


        public int position;
        public TabbedContentFragment(int i) {
            position=i;
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {
            View pageView;
            switch(position) {

                case 1: pageView = inflater.inflate(R.layout.fragment_pconnect, container, false);
                    break;
                default: pageView = inflater.inflate(R.layout.fragment_sconnect, container, false);
                    break;

            }


            return pageView;
        }
    }


}
