package features;


import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import img.myapplication.R;
import models.StudentModel;


@SuppressLint("ValidFragment")
public class StudentProfileFragment extends Fragment {



    private StudentModel profile;
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){

        View myView= inflater.inflate(R.layout.fragment_student_profile, container, false);

        TextView name=(TextView) myView.findViewById(R.id.name);
        TextView enr_no=(TextView) myView.findViewById(R.id.enr_no);
        TextView year=(TextView) myView.findViewById(R.id.year);
        //TextView branch=(TextView) getActivity().findViewById(R.id.branch);
        //TextView state=(TextView) getActivity().findViewById(R.id.state);
        TextView town=(TextView) myView.findViewById(R.id.town);
        TextView mobile=(TextView) myView.findViewById(R.id.mobile);
        TextView email=(TextView) myView.findViewById(R.id.email);

        name.setText(profile.name);
        enr_no.setText(profile.enr_no);
        year.setText(profile.year);
        town.setText(profile.town);
        mobile.setText(profile.mobile);
        email.setText(profile.email);

        return myView;
    }
    public StudentProfileFragment(StudentModel student){
        profile=student;
    }
}
