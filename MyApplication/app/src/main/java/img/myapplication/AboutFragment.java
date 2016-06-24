package img.myapplication;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;

public class AboutFragment extends Fragment {
    private ViewPager pager;
    private ImageButton prevImage;
    private ImageButton nextImage;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view= inflater.inflate(R.layout.fragment_about, container, false);
        prevImage= (ImageButton) view.findViewById(R.id.prevIMG);
        nextImage= (ImageButton) view.findViewById(R.id.nextIMG);
        SwipeImageAdapter pagerAdapter=null;
        PageChangeListener pageChangeListener=null;
        if (getActivity() instanceof Navigation) {
            int[] imageId={R.drawable.p01_welcome,R.drawable.p02_articles,R.drawable.p03_senior_connect};
            pagerAdapter=new SwipeImageAdapter(imageId);
            pageChangeListener=new PageChangeListener(imageId.length);
        }
        else if (getActivity() instanceof NavigationStudent) {
            int[] imageId={R.drawable.p01_welcome,R.drawable.p02_articles,R.drawable.p04_junior_connect};
            pagerAdapter=new SwipeImageAdapter(imageId);
            pageChangeListener=new PageChangeListener(imageId.length);
        }
        else if (getActivity() instanceof NavigationAudience) {
            ((NavigationAudience) getActivity()).setActionBarTitle(getString(R.string.title_about));
            int[] imageId={R.drawable.p01_welcome,R.drawable.p02_articles};
            pagerAdapter=new SwipeImageAdapter(imageId);
            pageChangeListener=new PageChangeListener(imageId.length);
        }
        pager= (ViewPager) view.findViewById(R.id.pager);
        prevImage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                pager.setCurrentItem(pager.getCurrentItem() - 1);
            }
        });
        nextImage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                pager.setCurrentItem(pager.getCurrentItem() + 1);
            }
        });
        pager.setOnPageChangeListener(pageChangeListener);
        pager.setAdapter(pagerAdapter);
        return view;
    }
    private class PageChangeListener implements ViewPager.OnPageChangeListener {
        private int length;
        public PageChangeListener(int length){
            this.length=length;
        }
        @Override
        public void onPageScrolled(int position, float positionOffset, int positionOffsetPixels) {

        }

        @Override
        public void onPageSelected(int position) {
            prevImage.setVisibility(View.VISIBLE);
            nextImage.setVisibility(View.VISIBLE);
            if (position==0) {
                prevImage.setVisibility(View.GONE);
            }
            else if (position==length-1){
                nextImage.setVisibility(View.GONE);
            }
        }

        @Override
        public void onPageScrollStateChanged(int state) {

        }
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
