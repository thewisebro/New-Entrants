package models;

/**
 * Created by ankush on 11/1/15.
 */
public class SeniorModel {
    public String name;
<<<<<<< HEAD
    public String branchname;
    public String branchcode;
    public String hometown;
    public String year;
    public String state;
    public String fb_link;
    public String email;
    public String mobile;
=======
    public String branch;
    public String year;
    public String state;
    public void copy(SeniorModel model){
        this.name=model.name;
        this.year=model.year;
        this.branch=model.branch;
    }
>>>>>>> 50782eb17d1d54b622a4c31b082817173c845682
}
