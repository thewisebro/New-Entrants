package img.myapplication;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;



public class BlogsFragment extends Fragment {
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState ){
        View view=inflater.inflate(R.layout.fragment_blogs, container, false);
        MySQLiteHelper db= new MySQLiteHelper(getContext());
        db.displayBlog(view,0);
        return view;
    }
}
