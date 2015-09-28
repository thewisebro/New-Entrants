package img.newentrants;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;



public class PConnectFragment extends Fragment {

    public int position;
    public PConnectFragment(){
        position = 0;
    }


    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View tabView;
        switch(position){

            case 1: tabView=inflater.inflate(R.layout.fragment_peer_connect_request, container, false);
                break;
            default: tabView=inflater.inflate(R.layout.fragment_peer_connect, container, false);
                break;
        }
        return tabView;
    }


}
