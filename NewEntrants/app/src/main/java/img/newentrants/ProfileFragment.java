package img.newentrants;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;



public class ProfileFragment extends Fragment {
    private static final String ARG_SECTION_NUMBER = "section_number";
    public ProfileFragment(){

    }
    public static ProfileFragment newInstance(int position){
        ProfileFragment fragment = new ProfileFragment();
        Bundle args = new Bundle();
        args.putInt(ARG_SECTION_NUMBER, position+1);
        fragment.setArguments(args);
        return fragment;
    }

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){

        return inflater.inflate(R.layout.fragment_profile, container, false);
    }
}
