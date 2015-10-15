package img.myapplication;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


public class ProfileFragment extends Fragment {

    private User_Model profile;
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){

        View myView= inflater.inflate(R.layout.fragment_profile, container, false);

        TextView name=(TextView) myView.findViewById(R.id.name);
        TextView enr=(TextView) myView.findViewById(R.id.enr);
        //TextView branch=(TextView) getActivity().findViewById(R.id.branch);
        //TextView state=(TextView) getActivity().findViewById(R.id.state);
        TextView mobile=(TextView) myView.findViewById(R.id.number);
        TextView email=(TextView) myView.findViewById(R.id.email);

        name.setText(profile.Name);
        enr.setText(profile.Enr_No);
        //branch.setText(profile.Branch);
        //state.setText(profile.State);
        mobile.setText(profile.Mobile);
        email.setText(profile.Email);

        return myView;
    }
    public ProfileFragment(User_Model user){
        profile=user;
    }
}
