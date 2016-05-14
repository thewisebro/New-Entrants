package img.myapplication;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;


/**
 * A simple {@link Fragment} subclass.
 */
public class NetworkErrorFragment extends Fragment {

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        if (getActivity() instanceof Navigation)
            ((Navigation) getActivity()).setActionBarTitle("Blogs");
        else if (getActivity() instanceof NavigationStudent)
            ((NavigationStudent)getActivity()).setActionBarTitle("Blogs");
        View view= inflater.inflate(R.layout.fragment_network_error, container, false);
        Button bt= (Button) view.findViewById(R.id.bt_try);
        Toast.makeText(getContext(),"Check Network Connection",Toast.LENGTH_SHORT).show();
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (getActivity().getSupportFragmentManager().getBackStackEntryCount()!=0){
                    getActivity().getSupportFragmentManager().popBackStack();
                }
            }
        });
        return view;
    }


}
