<<<<<<< HEAD
package features;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import img.myapplication.R;


/**
 * A simple {@link Fragment} subclass.
 */
public class ConnectFragment extends Fragment {


    public ConnectFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_connect, container, false);
        ViewPager viewPager= (ViewPager) view.findViewById(R.id.pager);
        viewPager.setAdapter(new FragmentPagerAdapter(getChildFragmentManager()) {
            @Override
            public Fragment getItem(int position) {
                Fragment fragment=null;
                if (position==0)
                    fragment=new RequestsFragment();
                else
                    fragment=new AcceptedFragment();
                return fragment;
            }

            @Override
            public int getCount() {
                return 2;
            }
        });
        return view;
    }


}
=======
package features;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import img.myapplication.R;


/**
 * A simple {@link Fragment} subclass.
 */
public class ConnectFragment extends Fragment {


    public ConnectFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_connect, container, false);
        ViewPager viewPager= (ViewPager) view.findViewById(R.id.pager);
        viewPager.setAdapter(new FragmentPagerAdapter(getChildFragmentManager()) {
            @Override
            public Fragment getItem(int position) {
                Fragment fragment=null;
                if (position==0)
                    fragment=new RequestsFragment();
                else
                    fragment=new AcceptedFragment();
                return fragment;
            }

            @Override
            public int getCount() {
                return 2;
            }
        });
        return view;
    }


}
>>>>>>> 50782eb17d1d54b622a4c31b082817173c845682
