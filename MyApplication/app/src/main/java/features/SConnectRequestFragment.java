package features;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.Map;

import img.myapplication.R;

public class SConnectRequestFragment extends Fragment {
    private Map<String,String> params;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_sconnect_request, container, false);
        params= (Map<String, String>) getArguments().getSerializable("userParams");


        return view;
    }


}
