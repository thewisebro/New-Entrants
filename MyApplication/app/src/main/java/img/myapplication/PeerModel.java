package img.myapplication;

/**
 * Created by ankush on 11/1/15.
 */
public class PeerModel {
    public String name;
    public String town;
    public String state;
    public void copy(PeerModel model){
        this.name=model.name;
        this.town=model.town;
        this.state=model.state;
    }
}

