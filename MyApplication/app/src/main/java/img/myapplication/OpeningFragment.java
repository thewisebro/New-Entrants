package img.myapplication;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.method.LinkMovementMethod;
import android.text.method.ScrollingMovementMethod;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


public class OpeningFragment extends Fragment {

    private int type;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        if (getActivity() instanceof Navigation) {
            ((Navigation) getActivity()).setActionBarTitle("About");
            type=1;
        }
        else if (getActivity() instanceof NavigationStudent) {
            ((NavigationStudent) getActivity()).setActionBarTitle("About");
            type=2;
        }
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_opening, container, false);
        TextView link= (TextView) view.findViewById(R.id.link);
        link.setMovementMethod(LinkMovementMethod.getInstance());
        TextView desc= (TextView) view.findViewById(R.id.app_desc);
        desc.setMovementMethod(new ScrollingMovementMethod());
        if (type==1) {
            desc.setText(getString(R.string.desc_junior));
        }
        else {
            desc.setText(getString(R.string.desc_senior));
        }
        return view;
    }


}
