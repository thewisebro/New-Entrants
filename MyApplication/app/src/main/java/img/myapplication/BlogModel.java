package img.myapplication;

public class BlogModel {
    public String topic;
    public String shortInfo;
    public String author;
    public String category;
    public String date;
    public String blogText;

    public String imageurl;

    public void copy(BlogModel model){
        this.author=model.author;
        this.blogText=model.blogText;
        this.category=model.category;
        this.date=model.date;
        this.imageurl=model.imageurl;
        this.shortInfo=model.shortInfo;
        this.topic=model.topic;
    }

}
