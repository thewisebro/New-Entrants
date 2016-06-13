package img.myapplication;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.method.LinkMovementMethod;
import android.text.method.ScrollingMovementMethod;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


public class OpeningFragment extends Fragment {

    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        menu.clear();
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        setHasOptionsMenu(true);

        View view= inflater.inflate(R.layout.fragment_opening, container, false);
        TextView link= (TextView) view.findViewById(R.id.link);
        link.setMovementMethod(LinkMovementMethod.getInstance());
        TextView desc= (TextView) view.findViewById(R.id.app_desc);
        desc.setMovementMethod(new ScrollingMovementMethod());

        if (getActivity() instanceof Navigation) {
            ((Navigation) getActivity()).setActionBarTitle(getString(R.string.title_about));
            desc.setText(getString(R.string.desc_junior));
        }
        else if (getActivity() instanceof NavigationStudent) {
            ((NavigationStudent) getActivity()).setActionBarTitle(getString(R.string.title_about));
            desc.setText(getString(R.string.desc_senior));
        }
        else if (getActivity() instanceof NavigationAudience) {
            ((NavigationAudience) getActivity()).setActionBarTitle(getString(R.string.title_about));
            desc.setText(getString(R.string.desc_senior));
        }
        return view;
    }


}
