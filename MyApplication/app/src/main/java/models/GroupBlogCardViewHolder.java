package models;

import android.widget.ImageView;
import android.widget.TextView;

import features.GroupBlogList;

/**
 * Created by Ankush on 30-04-2016.
 */
public class GroupBlogCardViewHolder {
    public TextView topic;
    public TextView description;
    public TextView group;
    public  TextView date;
    public ImageView img;
    public ImageView dp;
    public String blogUrl;
    public TextView category;
    public int id;
    public GroupBlogList.ImageLoadTask loaddp;
    public GroupBlogList.ImageLoadTask loadimg;
}
