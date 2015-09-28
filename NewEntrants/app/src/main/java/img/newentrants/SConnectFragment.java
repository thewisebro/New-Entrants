package img.newentrants;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.view.LayoutInflaterCompat;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;


public class SConnectFragment extends Fragment {
    public int position;
    public SConnectFragment(){
        position = 0;
    }


    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View tabView;
        switch(position){

            case 1: tabView=inflater.inflate(R.layout.fragment_senior_connect_accepted, container, false);
                break;
            default: tabView=inflater.inflate(R.layout.fragment_senior_connect_request, container, false);
                break;
        }
        return tabView;
    }
}