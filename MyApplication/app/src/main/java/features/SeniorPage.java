package features;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import img.myapplication.R;
import models.SeniorModel;


/**
 * A simple {@link Fragment} subclass.
 */
@SuppressLint("ValidFragment")
public class SeniorPage extends Fragment {
    private SeniorModel senior;

    public SeniorPage(SeniorModel model) {
        this.senior=model;
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_senior_page, container, false);
        TextView name= (TextView) view.findViewById(R.id.name);
        TextView year= (TextView) view.findViewById(R.id.year);
        TextView branch= (TextView) view.findViewById(R.id.branch);

        name.setText(senior.name);
        year.setText(senior.year);
        branch.setText(senior.branchname);

        return view;
    }


}
