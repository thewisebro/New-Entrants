package img.myapplication;


import android.app.Activity;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import java.net.HttpURLConnection;
import java.net.URL;


/**
 * A simple {@link Fragment} subclass.
 */
public class NetworkErrorFragment extends Fragment {

    private String appURL="http://192.168.121.187:8080/new_entrants/";


    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getActivity().getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected()){
            try {
                HttpURLConnection connection= (HttpURLConnection) new URL(appURL).openConnection();
                connection.setConnectTimeout(5000);
                connection.setReadTimeout(5000);
                int rcode=connection.getResponseCode();
                if (rcode== HttpURLConnection.HTTP_OK || rcode==HttpURLConnection.HTTP_ACCEPTED)
                    return true;
                else {
                    if (rcode==HttpURLConnection.HTTP_SERVER_ERROR){
                        Toast.makeText(getContext(), "SERVER-SIDE NETWORK ERROR!", Toast.LENGTH_SHORT).show();
                        return false;
                    }
                    else{
                        Toast.makeText(getContext(), "NETWORK ERROR", Toast.LENGTH_SHORT).show();
                        return false;
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(getContext(), "NETWORK ERROR", Toast.LENGTH_SHORT).show();
                return false;

            }
        }
        else
            Toast.makeText(getContext(), "NOT CONNECTED", Toast.LENGTH_SHORT).show();
        return false;
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_network_error, container, false);
        Button bt= (Button) view.findViewById(R.id.bt_try);
        bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (isConnected()){
                    getActivity().getSupportFragmentManager().beginTransaction().replace(R.id.container,new OpeningFragment()).commit();
                }
            }
        });
        return view;
    }


}
