package models;

import android.widget.ImageView;
import android.widget.TextView;

import features.BlogsList;

/**
 * Created by ankush on 10/31/15.
 */
public class BlogCardViewHolder {
    public  TextView topic;
    public TextView description;
    public TextView group;
    public  TextView date;
    public ImageView img;
    public ImageView dp;
    public String blogUrl;
    public TextView category;
    public int id;
    public BlogsList.ImageLoadTask loaddp;
    public BlogsList.ImageLoadTask loadimg;
}
