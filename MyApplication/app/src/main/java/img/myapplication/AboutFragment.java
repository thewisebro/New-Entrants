package img.myapplication;


import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import android.support.v7.app.ActionBarActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

public class AboutFragment extends Fragment {
    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        ((ActionBarActivity)getActivity()).getSupportActionBar().hide();
    }
    @Override
    public void onDestroyView(){
        super.onDestroyView();
        ((ActionBarActivity)getActivity()).getSupportActionBar().show();
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_about, container, false);
        SwipeImageAdapter pagerAdapter=null;
        if (getActivity() instanceof Navigation) {
            int[] imageId={R.drawable.img_error};
            pagerAdapter=new SwipeImageAdapter(imageId);
        }
        else if (getActivity() instanceof NavigationStudent) {
            int[] imageId={R.drawable.img_error};
            pagerAdapter=new SwipeImageAdapter(imageId);
        }
        else if (getActivity() instanceof NavigationAudience) {
            ((NavigationAudience) getActivity()).setActionBarTitle(getString(R.string.title_about));
            int[] imageId={R.drawable.img_error};
            pagerAdapter=new SwipeImageAdapter(imageId);
        }
        ViewPager pager= (ViewPager) view.findViewById(R.id.pager);
        pager.setAdapter(pagerAdapter);
        return view;
    }
    private class SwipeImageAdapter extends android.support.v4.view.PagerAdapter {
        private int[] imageID;

        public SwipeImageAdapter(int[] imageId) {
            this.imageID=imageId;
        }

        @Override
        public Object instantiateItem(ViewGroup container, int position) {
            LayoutInflater inflater = LayoutInflater.from(getContext());
            View view = inflater.inflate(R.layout.swipe_image_layout, container, false);
            ImageView img = (ImageView) view.findViewById(R.id.swipeImage);
            img.setImageResource(imageID[position]);
            ((ViewPager)container).addView(view);
            return view;
        }

        @Override
        public int getCount() {
            return imageID.length;
        }

        @Override
        public boolean isViewFromObject(View view, Object object) {
            return view==((View) object);
        }

        @Override
        public void destroyItem(ViewGroup container, int position, Object object) {
            ((ViewPager) container).removeView((View) object);

        }

    }
}
