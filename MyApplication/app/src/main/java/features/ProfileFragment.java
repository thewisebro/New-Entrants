package features;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;

import img.myapplication.R;
import models.NewEntrantModel;
import models.StudentModel;


@SuppressLint("ValidFragment")
public class ProfileFragment extends Fragment {

    private StudentModel student;
    private NewEntrantModel entrant;
    private String category;
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){

        View myView= inflater.inflate(R.layout.fragment_profile, container, false);

        state= (Spinner) findViewById(R.id.new_state);
        ArrayAdapter<CharSequence> stateList=ArrayAdapter.createFromResource(this,R.array.states,android.R.layout.simple_spinner_item);
        stateList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        state.setAdapter(stateList);

        branch= (Spinner) findViewById(R.id.new_branch);
        ArrayAdapter<CharSequence> branchList=ArrayAdapter.createFromResource(this,R.array.branches,android.R.layout.simple_spinner_item);
        branchList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        branch.setAdapter(branchList);

        return myView;
    }
    public ProfileFragment(Object user,String category){
        if (category.equals("entrant"))
            entrant= (NewEntrantModel) user;
        else
            student= (StudentModel) user;
        this.category=category;
    }
}
