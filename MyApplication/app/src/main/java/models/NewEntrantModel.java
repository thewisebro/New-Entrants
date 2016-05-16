package models;

import java.io.Serializable;

/**
 * Created by ankush on 10/30/15.
 */
public class NewEntrantModel implements Serializable {
    public String id;
    public String name;
    public String username;
    public String password;
    public String town;
    public String state;
    public String statecode;
    public String branchname;
    public String branchcode;
    public String mobile;
    public String email;
    public String fb_link;
    public Boolean phone_privacy;
    public Boolean profile_privacy;
    public String sess_id;
    public String category;
    public boolean valid;
}
