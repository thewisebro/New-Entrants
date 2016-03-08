package models;

public class BlogModel {
    public String topic;
    public String shortInfo;
    public String group;
    public String date;
    public String blogText;
    public String imageurl;
    public String blogurl;
    public String groupurl;
    public int id;

    public void copy(BlogModel model){
        this.blogText=model.blogText;
        this.group=model.group;
        this.date=model.date;
        this.imageurl=model.imageurl;
        this.shortInfo=model.shortInfo;
        this.topic=model.topic;
        this.id=model.id;
        this.blogurl=model.blogurl;
        this.groupurl=model.groupurl;
    }

}
