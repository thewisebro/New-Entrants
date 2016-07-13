package img.myapplication;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;


/**
 * A simple {@link Fragment} subclass.
 */
public class NetworkErrorFragment extends Fragment {

    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        menu.clear();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        if (getActivity() instanceof Navigation) {
            ((Navigation) getActivity()).getSupportActionBar().show();
            ((Navigation) getActivity()).setActionBarTitle("Blogs");
        }
        else if (getActivity() instanceof NavigationStudent) {
            ((NavigationStudent) getActivity()).getSupportActionBar().show();
            ((NavigationStudent) getActivity()).setActionBarTitle("Blogs");
        }
        else if (getActivity() instanceof NavigationAudience) {
            ((NavigationAudience) getActivity()).getSupportActionBar().show();
            ((NavigationAudience) getActivity()).setActionBarTitle("Blogs");
        }

        setHasOptionsMenu(true);
        View view= inflater.inflate(R.layout.fragment_network_error, container, false);
        Button bt= (Button) view.findViewById(R.id.bt_try);
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
