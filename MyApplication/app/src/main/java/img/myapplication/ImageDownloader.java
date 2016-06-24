package img.myapplication;

import android.annotation.TargetApi;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.os.Build;
import android.widget.ImageView;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.ref.WeakReference;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by Ankush on 14-05-2016.
 */
public class ImageDownloader {

    Context context;
    public ImageDownloader(Context cxt){
        context=cxt;
    }

    public void getImage(String url, ImageView imageView, int ht, int wt,int placeHolder){
        if (cancelPotentialDownload(url, imageView)) {
            final ImageLoadTask task=new ImageLoadTask(url,imageView,ht,wt,true);
            final AsyncDrawable asyncDrawable = new AsyncDrawable(task,placeHolder);
            imageView.setImageDrawable(asyncDrawable);
            task.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
        }
    }

    public void loadImage(String url, ImageView imageView, int ht, int wt){
        new ImageLoadTask(url,imageView,ht,wt,false)
                .executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
    }
    private class ImageLoadTask extends AsyncTask<Void, Void, Bitmap> {

        private boolean flag;
        private String url;
        private final WeakReference<ImageView> imageViewReference;
        private int ht;
        private int wt;

        public ImageLoadTask(String url, ImageView imageView, int h,int w, boolean b) {
            this.url = url;
            imageViewReference = new WeakReference<ImageView>(imageView);
            ht=h;
            wt=w;
            flag=b;
        }

        private int getInSampleSize(BitmapFactory.Options options){

            final int height = options.outHeight;
            final int width = options.outWidth;
            int inSampleSize = 1;

            if (height > ht || width > wt) {

                final int halfHeight = height / 2;
                final int halfWidth = width / 2;

                while ((halfHeight / inSampleSize) > ht
                        && (halfWidth / inSampleSize) > wt) {
                    inSampleSize *= 2;
                }
            }
            return inSampleSize;
        }
        private HttpURLConnection getConnection(){
            HttpURLConnection connection = null;
            try {
                connection = (HttpURLConnection) new URL(url)
                        .openConnection();
                connection.setDoInput(true);
                connection.setUseCaches(true);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return connection;
        }
        private Bitmap loadImage(){
            InputStream input=null;
            Bitmap bitmap=null;
            BitmapFactory.Options options=new BitmapFactory.Options();
            try {
                input= new BufferedInputStream(getConnection().getInputStream());
                input.mark(input.available());
                options.inJustDecodeBounds=true;
                BitmapFactory.decodeStream(input, null, options);
                options.inSampleSize=getInSampleSize(options);
                options.inJustDecodeBounds = false;
                input.reset();
                bitmap=BitmapFactory.decodeStream(input,null,options);
            } catch (IOException e) {
                e.printStackTrace();
                if (input!=null){
                    options.inJustDecodeBounds=false;
                    options.inPreferredConfig= Bitmap.Config.RGB_565;
                    options.inSampleSize=8;
                    try {
                        input=new BufferedInputStream(getConnection().getInputStream());
                        bitmap=BitmapFactory.decodeStream(input,null,options);
                    } catch (IOException e1) {
                        e1.printStackTrace();
                    }
                }
            }
            return bitmap;
        }
        private Bitmap image(){
            Bitmap bitmap=BitmapCacheUtil.getCache().get(url);
            if (bitmap==null){
                bitmap=loadImage();
                if (bitmap!=null)
                    BitmapCacheUtil.getCache().put(url,bitmap);
            }
            return bitmap;
        }

        @Override
        protected Bitmap doInBackground(Void... params) {
            return image();
        }

        @TargetApi(Build.VERSION_CODES.JELLY_BEAN)
        @Override
        protected void onPostExecute(Bitmap result) {
            if (isCancelled()) {
                result = null;
            }
            if (imageViewReference != null) {
                ImageView imageView = imageViewReference.get();
                if (result!=null){
                    if (flag){
                        ImageLoadTask task= getImageLoaderTask(imageView);
                        if (this == task) {
                            imageView.setImageBitmap(result);
                        }
                    }
                    else
                        imageView.setImageBitmap(result);
                }
            }
        }

    }
    class AsyncDrawable extends BitmapDrawable {
        private final WeakReference<ImageLoadTask> imageLoadTaskReference;

        public AsyncDrawable(ImageLoadTask task,int placeHolder) {
            super(context.getResources(),BitmapFactory.decodeResource(context.getResources(),placeHolder));
            imageLoadTaskReference=
                    new WeakReference<ImageLoadTask>(task);
        }

        public ImageLoadTask getImageLoadTask() {
            return imageLoadTaskReference.get();
        }
    }
    private static boolean cancelPotentialDownload(String url, ImageView imageView) {
        ImageLoadTask imageLoaderTask = getImageLoaderTask(imageView);

        if (imageLoaderTask != null) {
            String bitmapUrl = imageLoaderTask.url;
            if ((bitmapUrl == null) || (!bitmapUrl.equals(url))) {
                imageLoaderTask.cancel(true);
            } else {
                // The same URL is already being downloaded.
                return false;
            }
        }
        return true;
    }
    private static ImageLoadTask getImageLoaderTask(ImageView imageView) {
        if (imageView != null) {
            Drawable drawable = imageView.getDrawable();
            if (drawable instanceof AsyncDrawable) {
                AsyncDrawable downloadedDrawable = (AsyncDrawable)drawable;
                return downloadedDrawable.getImageLoadTask();
            }
        }
        return null;
    }

}
