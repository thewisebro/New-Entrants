package img.myapplication;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.provider.BaseColumns;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;

public class ProfileFragment extends Fragment {
    Cursor user;

    public ProfileFragment(Cursor result) {
        user=result;
    }


    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View myView=inflater.inflate(R.layout.fragment_profile, container, false);


            EditText et_Name=(EditText) myView.findViewById(R.id.name);
            EditText et_Enr=(EditText) myView.findViewById(R.id.enr);
            EditText et_Email=(EditText) myView.findViewById(R.id.email);
            EditText et_Mobile=(EditText) myView.findViewById(R.id.number);
           /* et_Name.setText(user.getString(user.getColumnIndex("Name")));
            et_Enr.setText(user.getString(user.getColumnIndex("Enr_No")));
            et_Email.setText(user.getString(user.getColumnIndex("Email")));
            et_Mobile.setText(user.getString(user.getColumnIndex("Mobile_No")));*/
       

        return myView;
    }

}

