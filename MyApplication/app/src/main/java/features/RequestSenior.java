package features;

import android.app.Activity;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;

import img.myapplication.R;


/**
 * A simple {@link Fragment} subclass.
 */
public class RequestSenior extends Fragment {


    public RequestSenior() {
    }
    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        if(!isConnected()){
            return inflater.inflate(R.layout.fragment_network_error,container,false);
        }
        View view= inflater.inflate(R.layout.fragment_request_senior, container, false);
        final RadioGroup rg= (RadioGroup) view.findViewById(R.id.requestOptions);
        final RadioButton state= (RadioButton) view.findViewById(R.id.rd_state);
        final RadioButton lang= (RadioButton) view.findViewById(R.id.rd_language);
        final RadioButton branch= (RadioButton) view.findViewById(R.id.rd_branch);
        Button bt= (Button) view.findViewById(R.id.rqstBtn);
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int selectedId=rg.getCheckedRadioButtonId();
                if (selectedId==state.getId()){
                    request("state");
                }
                else if (selectedId==branch.getId()){
                    request("branch");
                }
                else if (selectedId==lang.getId()){
                    request("language");
                }
            }
            private void request(String option){

                try {
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        return view;
    }


}
