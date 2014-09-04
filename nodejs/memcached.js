var pickle = require('jpickle');
//var qs = require('querystring');
//var utf8 = require('utf8');
//var punycode = require('punycode');
var Memcached = require('memcached');
Memcached.config.poolSize = 25;
var memcached = new Memcached('127.0.0.1:11211');

function fetch(key){
  memcached.get(key, function(err, data){
    if(err)
      console.error(err);
    console.dir(data);
    //var encode_str = punycode.encode(data);
    //console.log(encode_str);
    //var base64data = new Buffer(data, 'binary').toString('base64');
    var buf = new Buffer(data, 'base64');
    console.log(buf);
    //var safe_str = data.toString();
    //console.log(data.toString());
    //var safe_str = qs.escape(data);
    //console.log(safe_str);
    pickle.loads(buf, function(original){
      console.log(original);
    });
    memcached.end();
  });
}

fetch(':1:django.contrib.sessions.cached_dbk4440080cg8utlp4i6kzrcbx117wa1vx');

