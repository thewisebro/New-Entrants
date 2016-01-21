package img.myapplication;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;


/**
 * A simple {@link Fragment} subclass.
 */
public class PeerPage extends Fragment {
    private PeerModel peer;

    public PeerPage(PeerModel model) {
        peer=model;
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_peer_page, container, false);

        TextView name= (TextView) view.findViewById(R.id.name);
        TextView town= (TextView) view.findViewById(R.id.town);
        TextView state= (TextView) view.findViewById(R.id.state);

        name.setText(peer.name);
        town.setText(peer.town);
        state.setText(peer.state);

        return view;
    }


}
