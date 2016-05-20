package img.myapplication;

import android.graphics.Bitmap;
import android.support.v4.util.LruCache;

/**
 * Created by Ankush on 18-05-2016.
 */
public final class BitmapCacheUtil {
    private static LruCache<String,Bitmap> bitmapCache;
    private BitmapCacheUtil(){}

    public static LruCache<String,Bitmap> getCache(){
        if (bitmapCache==null)
            setCache();
        return bitmapCache;
    }
    private static int getCacheSize(){
        final int maxMemory = (int) (Runtime.getRuntime().maxMemory() / 1024);
        final int cacheSize=maxMemory/4;
        return cacheSize;
    }

    private static void setCache(){
        bitmapCache = new LruCache<String, Bitmap>(getCacheSize()) {
            @Override
            protected int sizeOf(String key, Bitmap bitmap) {
                return bitmap.getByteCount() / 1024;
            }
        };
    }
}
