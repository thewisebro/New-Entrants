var loaded_scripts_apps = [];

var apps_scripts = {
  'home':[
    '/static/js/prettydate.js',
    '/static/handlebars/feeds/templates.js',
    '/static/js/feeds/feeds.js'
  ],
  'notifications':[
    '/static/js/prettydate.js',
    '/static/js/notifications/base.js'
  ],
  'forum':[
    '/static/js/forum/base.js'
  ],
  'notices':[
    '/static/handlebars/notices/templates.js',
    '/static/js/notices/constants.js',
    '/static/js/notices/jquery.simplePagination.js',
    '/static/js/notices/base.js',
    '/static/js/notices/date.js',
  ],
  'events':[
    '/static/js/events/events.js'
  ],
  'news':[
    //'/static/js/news/jquery-ias.min.js',
    '/static/js/news/jquery-ui.js',
    '/static/js/news/highcharts.js',
    '/static/js/news/draggable-points-master/draggable-points.js',
    '/static/js/news/news.js'
  ],
  'helpcenter':[
    '/static/handlebars/helpcenter/templates.js',
    '/static/js/prettydate.js',
    '/static/js/helpcenter/helpcenter.js'
  ],
  'settings':[
    '/static/handlebars/utilities/templates.js',
    '/static/js/utilities/base.js'
  ],
  'groups':[
    '/static/handlebars/groups/templates.js',
    '/static/js/groups/base.js',
    '/static/js/groups/activity.js',
  ]
};

function load_app(app, callback){
  if(!(app in apps_scripts) || $.inArray(app,loaded_scripts_apps)>-1){
    callback();
    return;
  }
  var scripts = apps_scripts[app];

  var wrapped_callback = function(){
    loaded_scripts_apps.push(app);
    if(callback)callback();
  };

  load_scripts_in_pipe(scripts, wrapped_callback);
}
