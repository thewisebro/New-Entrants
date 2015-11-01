package img.myapplication;

/**
 * Created by ankush on 11/1/15.
 */
public class SeniorModel {
    public String name;
    public String branch;
    public String year;
    public void copy(SeniorModel model){
        this.name=model.name;
        this.year=model.year;
        this.branch=model.branch;
    }
}
