var loaded_scripts_apps = [];

var apps_scripts = {
  'home':[
    '/static/js/prettydate.js',
    '/static/js/feeds/feeds.js'
  ],
  'notices':[
    '/static/js/notices/base.js'
  ],
  'events':[
    '/static/js/events/events.js'
  ],
  'helpcenter':[
    '/static/js/prettydate.js',
    '/static/js/helpcenter/helpcenter.js'
  ]
}

function load_app(app, callback){
  if(!(app in apps_scripts) || $.inArray(app,loaded_scripts_apps)>-1){
    callback();
    return;
  }
  var scripts = apps_scripts[app];
  var deferred = new $.Deferred(), pipe = deferred;

  $.each(scripts , function(i, val){
    pipe = pipe.pipe(function(){
      return  $.cachedScript(val);
    });
  });

  pipe = pipe.pipe(function(){
    loaded_scripts_apps.push(app);
  });

  if(callback)
    pipe = pipe.pipe(callback);
  deferred.resolve();
}
