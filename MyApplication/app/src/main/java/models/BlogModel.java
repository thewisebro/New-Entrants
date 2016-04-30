package models;

import java.util.List;

public class BlogModel {
    public String topic;
    public String desc;
    public String group;
    public String group_username;
    public String date;
    public String imageurl;
    public String slug;
    public String dpurl;
    public String content;
    public String category;
    public List<String> urls;
    public int id;

    public void setCategory(){
        if (group_username.equals("iitr"))
            category="From the Institute";
        else
            category="From the Groups";
    }

}
