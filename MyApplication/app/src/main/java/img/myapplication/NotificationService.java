package img.myapplication;

import android.annotation.TargetApi;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.os.AsyncTask;
import android.os.Build;
import android.os.IBinder;
import android.os.PowerManager;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import models.JuniorModel;
import models.NewEntrantModel;
import models.SeniorModel;
import models.StudentModel;

public class NotificationService extends Service {

    private PowerManager.WakeLock mWakeLock;
    private MySQLiteHelper db;
    public NotificationService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        throw new UnsupportedOperationException("Not yet implemented");
    }
    @Override
    public void onStart(Intent intent, int startId) {
        handleIntent(intent);
    }
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        handleIntent(intent);
        return START_NOT_STICKY;
    }
    @Override
    public void onDestroy() {
        super.onDestroy();
        mWakeLock.release();
    }
    private void handleIntent(Intent intent){
        PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
        mWakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "Check for update");
        mWakeLock.acquire();

        ConnectivityManager cm = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
        if (!cm.getBackgroundDataSetting()) {
            stopSelf();
            return;
        }
        db=new MySQLiteHelper(getApplicationContext());
        if (db.loggedSenior()){
            Log.d("service","before updatejuniors execution");
            new updateJuniorsList().execute();
        }
        else if (db.loggedEntrant()) {
            Log.d("service","before updateseniors execution");
            new updateSeniorsList().execute();
        }
    }
    private class updateJuniorsList extends AsyncTask<Void, Void, String> {
        private StudentModel student;
        private String pendingURL;
        @Override
        protected void onPreExecute(){
            student=db.getStudent();
            String appURL = getString(R.string.app);
            pendingURL = appURL + "/pending/";
        }
        @Override
        protected String doInBackground(Void... params) {
            try {
                HttpURLConnection conn=(HttpURLConnection) new URL(pendingURL).openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie", "CHANNELI_SESSID="+student.sess_id);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                return sb.toString();
            } catch (Exception e) {
                e.printStackTrace();
                return "error";
            }
        }
        @Override
        protected void onPostExecute(String result) {
            if (!(result.equals("error"))){
                try {
                    JSONObject jsonObject=new JSONObject(result);
                    if ("success".equals(jsonObject.getString("status"))){
                        JSONArray jArray=jsonObject.getJSONArray("requests");
                        int len=jArray.length();
                        if (len>0){
                            showNotification("senior");
                            db.deletePendingJuniors();
                            for(int i=0; i<len;i++){

                                JSONObject object=jArray.getJSONObject(i);
                                JuniorModel model= new JuniorModel();
                                model.name=object.getString("name");
                                model.town=object.getString("hometown");
                                model.state=(new JSONObject(object.getString("state"))).getString("name");
                                model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                                model.username=object.getString("username");
                                model.description=object.getString("description");
                                model.status="pending";
                                db.addJunior(model);
                            }
                        }
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            Log.d("service","onpostexecute jconnect");
            stopSelf();
        }
    }
    private class updateSeniorsList extends AsyncTask<Void, Void, String> {
        private String acceptedURL;
        private NewEntrantModel entrant;
        @Override
        protected void onPreExecute(){
            entrant=db.getEntrant();
            String hostURL = getString(R.string.host);
            acceptedURL = hostURL + "/new_entrants/accepted/";
        }
        @Override
        protected String doInBackground(Void... params) {
            try {
                HttpURLConnection conn= (HttpURLConnection) new URL(acceptedURL).openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(10000);
                conn.setRequestProperty("Cookie","CHANNELI_SESSID="+entrant.sess_id);
                BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(conn.getInputStream()));
                StringBuilder sb=new StringBuilder();
                String line = "";
                while((line = bufferedReader.readLine()) != null)
                    sb.append(line + '\n');
                return sb.toString();
            } catch (Exception e) {
                return "error";
            }
        }
        @Override
        protected void onPostExecute(String result) {
            if (!(result.equals("error"))){
                try {
                    JSONObject jObject = new JSONObject(result);
                    if ("success".equals(jObject.getString("status"))){
                        JSONArray jArray=jObject.getJSONArray("students");
                        int len=jArray.length();
                        if (len>db.getAcceptedSeniorsCount()){
                            showNotification("junior");
                            for(int i=0; i<len;i++){
                                JSONObject object=jArray.getJSONObject(i);
                                SeniorModel model= new SeniorModel();
                                model.name=object.getString("name");
                                model.town=object.getString("hometown");
                                model.state=(new JSONObject(object.getString("state"))).getString("name");
                                model.branch=(new JSONObject(object.getString("branch"))).getString("name");
                                model.fblink=object.getString("fb_link");
                                model.contact=object.getString("contact");
                                model.email=object.getString("email");
                                model.dp_link=object.getString("dp_link");
                                model.year=object.getInt("year");
                                db.addSenior(model);
                            }
                        }
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            Log.d("service","onpostexecute sconnect");
            stopSelf();
        }
    }

    @TargetApi(Build.VERSION_CODES.JELLY_BEAN)
    public void showNotification(String from){

        String title=null;
        String msg=null;
        int tag=R.string.app_name;
        if (from.equals("senior")){
            title=getString(R.string.senior_notify_title);
            msg=getString(R.string.senior_notify_msg);
        }
        else if(from.equals("junior")) {
            title=getString(R.string.junior_notify_title);
            msg=getString(R.string.junior_notify_msg);
        }

        NotificationManager mNM = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        PendingIntent actionIntent= PendingIntent.getActivity(getApplicationContext(),0
                ,new Intent(getApplicationContext(),Login.class),0);
        Notification notification = new Notification.Builder(this)
                .setSmallIcon(R.mipmap.ic_launcher)  // the status icon
                .setWhen(System.currentTimeMillis())  // the time stamp
                .setContentTitle(title)  // the label of the entry
                .setContentText(msg)  // the contents of the entry
                .setContentIntent(actionIntent)  // The intent to send when the entry is clicked
                .setAutoCancel(true)
                .build();

        // Send the notification.
        mNM.notify(tag, notification);
    }
}
