package img.myapplication;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


public class ProfileFragment extends Fragment {

    private StudentModel profile;
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){

        View myView= inflater.inflate(R.layout.fragment_profile, container, false);

        TextView name=(TextView) myView.findViewById(R.id.name);
        TextView enr=(TextView) myView.findViewById(R.id.enr);
        //TextView branch=(TextView) getActivity().findViewById(R.id.branch);
        //TextView state=(TextView) getActivity().findViewById(R.id.state);
        TextView mobile=(TextView) myView.findViewById(R.id.number);
        TextView email=(TextView) myView.findViewById(R.id.email);

        name.setText(profile.name);
        enr.setText(profile.enr_no);
        //branch.setText(profile.Branch);
        //state.setText(profile.State);
        mobile.setText(profile.mobile);
        email.setText(profile.email);

        return myView;
    }
    public ProfileFragment(StudentModel user){
        profile=user;
    }
}
