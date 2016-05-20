package tinyfold.tinyfold;

import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Bitmap;
import android.support.v4.util.LruCache;
import android.text.TextUtils;
import android.util.Log;
import android.widget.ImageView;

import com.android.volley.Cache;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.ImageLoader;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.Map;

public class Singleton  {
    private static Singleton instance;
    private static Context context;
    private RequestQueue requestQueue;
    private ImageLoader imageLoader;
    public final static String TAG= Singleton.class.getSimpleName();
    private ImageLoader.ImageCache bitmapCache;

    private Singleton(Context cntxt){        //no external instances can be created
        context=cntxt;
        requestQueue=getRequestQueue();
        bitmapCache=new imageCache();
        imageLoader=new ImageLoader(requestQueue,bitmapCache);
    }
    public static synchronized Singleton getInstance(Context cntxt){
        if (instance==null){
            instance=new Singleton(cntxt);
        }
        return instance;
    }
    private RequestQueue getRequestQueue(){
        if (requestQueue==null)
            requestQueue= Volley.newRequestQueue(context.getApplicationContext());
        return requestQueue;
    }
    public <T> void addToRequestQueue(Request<T> req) {
        req.setTag(TAG);
        getRequestQueue().add(req);
    }
    public <T> void addToRequestQueue(Request<T> req, String tag) {
        req.setTag(TextUtils.isEmpty(tag) ? TAG : tag);
        getRequestQueue().add(req);
    }
    public void cancelPendingRequest(Object tag) {
        if (requestQueue != null) {
            requestQueue.cancelAll(tag);
        }
    }
    public void cancelAllPendingRequests(){
        if (requestQueue!=null)
            requestQueue.cancelAll(new RequestQueue.RequestFilter() {
                @Override
                public boolean apply(Request<?> request) {
                    return true;
                }
            });
    }
    public ImageLoader getImageLoader(){
        return imageLoader;
    }
    public void requestBitmap(String url, ImageView view){
        imageLoader.get(url,ImageLoader.getImageListener(view,R.drawable.img_error,R.drawable.img_error));
    }
    public JSONObject jsonObjectRequest(String url){
        ProgressDialog dialog=new ProgressDialog(context.getApplicationContext());
        dialog.setMessage("Requesting...");
        dialog.show();

        final JSONObject[] output = new JSONObject[1];

        JsonObjectRequest request= new JsonObjectRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.d(TAG, response.toString());
                        dialog.dismiss();
                        output[0] =response;
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        dialog.dismiss();
                        //Toast.makeText(context.getApplicationContext(),"Error: "+error.getMessage(),Toast.LENGTH_SHORT).show();
                        VolleyLog.d(TAG, "Error: " + error.getMessage());
                    }
                });
        addToRequestQueue(request, "JSONObject Request");
        return output[0];
    }
    public JSONArray jsonArrayRequest(String url){
        ProgressDialog dialog=new ProgressDialog(context.getApplicationContext());
        dialog.setMessage("Requesting...");
        dialog.show();

        final JSONArray[] output = new JSONArray[1];

        JsonArrayRequest request= new JsonArrayRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        Log.d(TAG, response.toString());
                        dialog.dismiss();
                        output[0] =response;
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        dialog.dismiss();
                        //Toast.makeText(context.getApplicationContext(),"Error: "+error.getMessage(),Toast.LENGTH_SHORT).show();
                        VolleyLog.d(TAG, "Error: " + error.getMessage());
                    }
                });
        addToRequestQueue(request, "JSONArray Request");
        return output[0];
    }
    public void postRequest(String url, Map<String,String> params){
        ProgressDialog dialog=new ProgressDialog(context.getApplicationContext());
        dialog.setMessage("Requesting...");
        dialog.show();

        JsonObjectRequest request= new JsonObjectRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.d(TAG, response.toString());
                        dialog.dismiss();
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        dialog.dismiss();
                        //Toast.makeText(context.getApplicationContext(),"Error: "+error.getMessage(),Toast.LENGTH_SHORT).show();
                        VolleyLog.d(TAG, "Error: " + error.getMessage());
                    }
                }){
                @Override
                protected Map<String,String> getParams(){
                    return  params;
                }
        };
        addToRequestQueue(request, "POST Request");
    }
    public void loadFromCache(String url){
        Cache cache= requestQueue.getCache();
        Cache.Entry entry=cache.get(url);
        if (entry!=null){
            try {
                String data=new String(entry.data,"UTF-8");
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
        else {

        }
    }

    private class imageCache implements ImageLoader.ImageCache {

        private LruCache<String, Bitmap> cache;

        public imageCache(){
            int maxMemory = (int) (Runtime.getRuntime().maxMemory() / 1024);
            int cacheSize = maxMemory / 8;
            cache=new LruCache<String,Bitmap>(cacheSize){
                @Override
                protected int sizeOf(String key, Bitmap bitmap) {
                    return bitmap.getByteCount() / 1024;
                }
            };
        }
        @Override
        public Bitmap getBitmap(String url) {
            return cache.get(url);
        }
        @Override
        public void putBitmap(String url, Bitmap bitmap) {
            cache.put(url, bitmap);
        }
    }
}
