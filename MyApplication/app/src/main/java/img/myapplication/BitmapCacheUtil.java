package img.myapplication;

import android.graphics.Bitmap;
import android.support.v4.util.LruCache;

/**
 * Created by Ankush on 18-05-2016.
 */
public final class BitmapCacheUtil {
    private static LruCache<String,Bitmap> bitmapCache;
    private BitmapCacheUtil(){}

    public static void setCache(){
        int maxMemory = (int) (Runtime.getRuntime().maxMemory() / 1024);
        int cacheSize=maxMemory/4;
        bitmapCache = new LruCache<String, Bitmap>(cacheSize) {
            @Override
            protected int sizeOf(String key, Bitmap bitmap) {
                return bitmap.getByteCount() / 1024;
            }
        };

    }
    public static Bitmap getBitmap(String key){
        return bitmapCache.get(key);
    }
    public static void putBitmap(String key, Bitmap value){
        bitmapCache.put(key, value);
    }
}
