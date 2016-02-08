package img.myapplication;

public class BlogModel {
    public String topic;
    public String shortInfo;
    //public String author;
    // public String category;
    public String group;
    public String date;
    public String blogText;

    //public String imageurl;

    public void copy(BlogModel model){
        this.blogText=model.blogText;
        this.group=model.group;
        this.date=model.date;
        //this.imageurl=model.imageurl;
        this.shortInfo=model.shortInfo;
        this.topic=model.topic;
    }

}
