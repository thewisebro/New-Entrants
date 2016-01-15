package img.myapplication;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;


public class EditInfoFragment extends Fragment {
    private NewEntrantModel user;
    private MySQLiteHelper db;
    private EditText et_email;
    private EditText et_number;
    private EditText et_name;
    private EditText et_town;

    public EditInfoFragment(NewEntrantModel arg){
        user=arg;
    }

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){

        db=new MySQLiteHelper(getContext());
        View view= inflater.inflate(R.layout.fragment_edit_info, container, false);
        et_name=(EditText) view.findViewById(R.id.edit_name);
        et_town=(EditText) view.findViewById(R.id.enr_no);
        et_email=(EditText) view.findViewById(R.id.edit_email);
        et_number=(EditText) view.findViewById(R.id.edit_number);

        et_name.setText(user.name);
        //et_town.setText(user.town);
        et_email.setText(user.email);
        et_number.setText(user.mobile);

        Spinner state= (Spinner) view.findViewById(R.id.edit_state);
        ArrayAdapter<CharSequence> stateList=ArrayAdapter.createFromResource(getContext(),R.array.states,android.R.layout.simple_spinner_item);
        stateList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        state.setAdapter(stateList);
        Spinner branch= (Spinner) view.findViewById(R.id.edit_branch);
        ArrayAdapter<CharSequence> branchList=ArrayAdapter.createFromResource(getContext(),R.array.branches,android.R.layout.simple_spinner_item);
        branchList.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        branch.setAdapter(branchList);

        return view;
    }

}
