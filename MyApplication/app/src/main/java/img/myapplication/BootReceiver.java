package img.myapplication;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class BootReceiver extends BroadcastReceiver {
    public BootReceiver() {
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        PendingIntent pIntent=PendingIntent.getService(context,0,new Intent(context,NotificationService.class),0);
        AlarmManager am=(AlarmManager) context.getSystemService(context.ALARM_SERVICE);
        am.cancel(pIntent);
        am.setInexactRepeating(AlarmManager.ELAPSED_REALTIME_WAKEUP, System.currentTimeMillis(),
                AlarmManager.INTERVAL_HALF_DAY,pIntent);

    }
}
