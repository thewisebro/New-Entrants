package img.myapplication;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;


public class EditInfoFragment extends Fragment {
    private User_Model user;
    private MySQLiteHelper db;
    private EditText et_email;
    private EditText et_number;
    private EditText et_name;
    private EditText et_enr;

    public EditInfoFragment(User_Model arg){
        user=arg;
    }
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        db=new MySQLiteHelper(getContext());
        View view= inflater.inflate(R.layout.fragment_edit_info, container, false);
        et_name=(EditText) view.findViewById(R.id.edit_name);
        et_enr=(EditText) view.findViewById(R.id.edit_enr);
        et_email=(EditText) view.findViewById(R.id.edit_email);
        et_number=(EditText) view.findViewById(R.id.edit_number);
        et_name.setText(user.Name);
        et_enr.setText(user.Enr_No);
        et_email.setText(user.Email);
        et_number.setText(user.Mobile);

        return view;
    }
    public void update(){
        et_email=(EditText) getView().findViewById(R.id.edit_email);
        et_number=(EditText) getView().findViewById(R.id.edit_number);
        user.Email=et_email.getText().toString();
        user.Mobile=et_number.getText().toString();
        db.updateUser(user);
    }
}
