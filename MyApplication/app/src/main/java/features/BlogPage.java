package features;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import img.myapplication.R;
import models.BlogModel;

/**
 * A simple {@link Fragment} subclass.
 */
public class BlogPage extends Fragment {
    private BlogModel blog;
    public BlogPage(BlogModel model){
        this.blog=model;
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view= inflater.inflate(R.layout.fragment_blog_page, container, false);

        TextView topic= (TextView) view.findViewById(R.id.topic);
        //TextView shortInfo= (TextView) view.findViewById(R.id.shortInfo);
        TextView date= (TextView) view.findViewById(R.id.date);
        TextView blogText= (TextView) view.findViewById(R.id.blogText);
        TextView group= (TextView) view.findViewById(R.id.group);
       // TextView topic= (TextView) view.findViewById(R.id.topic);
       // TextView topic= (TextView) view.findViewById(R.id.topic);

        topic.setText(blog.topic);
        //shortInfo.setText(blog.shortInfo);
        blogText.setText(blog.blogText);
        date.setText(blog.date);
        group.setText(blog.group);
        //author.setText(blog.author);
        return view;
    }


}
