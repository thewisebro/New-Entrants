function Player() {
  var self = this;
  var sm = soundManager; // soundManager instance
  var isIE = (navigator.userAgent.match(/msie/i));
  var sound;
  var checkmute = 0;
  var prevVolume;
  var duration=null;
  this.prevSound = null;
  this.currentSound = null;
  this.nextSound = null;
  this.loopSetting=0;//default 
  this.shuffle=false;
  this.shuffle_stack = 0; // count for stack overflow of playShuffle
  this.events = {

    // handlers for sound events as they're started/stopped/played

    play: function() {
       $('#'+sound.id).find('.play_icon img').attr("src","/static_jb/images/jukebox/icon_new_pause.png")
     //  console.log("--------------"+sound.id); 
      if( $('#slider').slider("value")<5){sound.setVolume( $('#slider').slider(0));}
        else{sound.setVolume( $('#slider').slider("value"));}
       
       $('#'+sound.id).find('.faint').animate({'opacity':'1'},300);
       $('#'+sound.id).find('.play_icon').animate({'opacity':'1'},300);
        $("#bLeftPlay").find("img").attr("src","/static_jb/images/jukebox/icon_new_pause.png");
        var id_play = sound.id.split('_')[1];
        // document.title=songs_url[id_play].song +'-'+ songs_url[id_play].artists[0].artist;
      
    },

    stop: function() {
      $('#'+sound.id).find('.play_icon img').attr("src","/static_jb/images/jukebox/icon_new_play.png");
      
       $('#'+sound.id).find('.faint').attr('style','');
       $('#'+sound.id).find('.play_icon').attr('style','');
        // document.title='Jukebox';

    },

    pause: function() 
           {
        $("#bLeftPlay").find("img").attr("src","/static_jb/images/jukebox/icon_new_play.png");
        // document.title='Jukebox';
    },

    resume: function() {

        $("#bLeftPlay").find("img").attr("src","/static_jb/images/jukebox/icon_new_pause.png");
        var id_play = sound.id.split('_')[1];
        // document.title=songs_url[id_play].song +'-'+ songs_url[id_play].artists[0].artist;
    },

    finish: function() {
       $("#songLoaded").css('width', '0');
       $("#musicBlueSlider").css('width','0');
       $("#ui-sliderlarge-handle").css('left','0');
       $("#timePlayed").html(0+':'+"00");
        // document.title='Jukebox';
       
       // $("#bLeftPlay").find("img").attr("src","/static_jb/images/jukebox/icon_new_play.png");
      // $("#bLeftPlay img").click();
      // $('#'+sound.id).find('.faint').attr('style','');
      // $('#'+sound.id).find('.play_icon').attr('style','');
      // $('#'+sound.id).find('.play_icon i').removeClass('icon-pause').addClass('icon-play');
       //check for looping
        //check for shuffle on
       if(self.shuffle && self.shuffle != 1){//if shuffle
         self.playShuffle();
       }
       else{//else shuffle
       if(self.loopSetting==0){
         if((($("#queue_content").find(".qselected").next().length>0))){
             $('#bLeftRight img').click();
         }
       }
       else if(self.loopSetting==1){
            sound.play();
       }
       else{
         //alert("sadsadsad");
          if(($("#queue_content").find(".qselected").next().length>0)){
              $("#bLeftRight img").click();
          }
          else{
         
             var temp = $("queue_content").find(".qselected");
             in_queue = true;//song is in the queue 
             $($("#queue_content").children('div')[0]).addClass("qselected").click();
             temp.removeClass("qselected");
             //var a = $("#queue_content").find(".qselected").attr("id");
             //var k = a.slice(5,a.length);
             //play(parseInt(k));

          }
       }
       }//else shuffle
    },
    loading:function(){
      //  soundManager._writeDebug(this.id + ': loading ' + this.bytesLoaded + ' / ' + this.bytesTotal);
        //soundManager._writeDebug('position = ' + this.position);

       // var duuration = this.duration;
        var seekbarPositionLoaded =  (this.bytesLoaded/this.bytesTotal)* ($("#musicSlider").width());//min
      // console.log("seekbarLoaded:"+seekbarPositionLoaded);
      //   $("#musicBlueSlider").css('width', ((this.position/this.duration) *  ($("#musicSlider").width()))); 
       // $("#ui-sliderlarge-handle").animate({left: ((this.position/this.duration) *($("#musicSlider").width()))});
         $("#songLoaded").css('width',seekbarPositionLoaded + 'px');


       // console.log("sadsadsadsad"+pars+":::duration=="+this.duration);
    },
    whileplaying: function(){
       $("#musicBlueSlider").css('width', ((this.position/this.duration) *  ($("#musicSlider").width())));
        $("#ui-sliderlarge-handle").css('left', ((this.position/this.duration) *($("#musicSlider").width())));
          var seconds = this.position/1000;
          var min=Math.floor(seconds/60);
          var sec=Math.floor(seconds%60);

          var tseconds=this.duration/1000;
          var tmin = Math.floor(tseconds/60);
          var tsec=Math.floor(tseconds%60);
          function leftzero(n){
                return n > 9 ? "" + n: "0" + n;
          }
         $("#timePlayed").text(min+':'+leftzero(sec));
         $("#totalTime").text(tmin+':'+leftzero(tsec));

      }

  }


  this.playShuffle = function(){
      //shuffle songs from list

      var index = Math.floor(Math.random()*queue.length);
      var song_random = queue[index];
      if(song_random == song_playing){
        this.shuffle_stack++;
        if(this.shuffle_stack < 5)
        {
          self.playShuffle();
          return;
        }
      }
      $("#queue_content").find(".qselected").removeClass("qselected");
      //console.log(a);
      in_queue=true;
      index += 1; // nth child starts from 1 not 0
      $('#queue_content div.qitem:nth-child('+index+')').addClass("qselected").click();   // bug solved by adding 'qitem'
      console.log('index  '+index);
      this.shuffle_stack = 0; //to reset shuffle_stack
      /*play(song_random);*/

  }

  this.play_url = function(idback,urlback){


          $this = $(this);
          //check if sound is currently playing

          if(self.currentSound){//check if sound exist and is playing
            if(idback==sound.id){
             //  console.log('playing sound found state toggled');
              console.log('  idback  '+idback);
              //sound.togglePause();
            }
            else{
              //the clicked div is some other sound 
              //stop and unload it

              sound.stop();
              sound.unload();
             // sound.destruct();
              //the sound will not be destroyed it will start from there only
              //+++++maybe we can use destruct here .. doubt .. if it loads the sound again 
              //CHECK LATER sound.destroy()
              sound = soundManager.createSound({
               id:idback,
               url:urlback,
               autoLoad: true,
               onplay:self.events.play,
               onstop:self.events.stop,
               onpause:self.events.pause,
               onresume:self.events.resume,
               onfinish:self.events.finish,
               whileloading:self.events.loading,
               whileplaying:self.events.whileplaying,
            });

            // tack on some custom data if needed
            sound._data = {};
            //create a check if sound is playable or not 
            sound.play();
            //set the currentSound to id of the sound currently playing
            self.currentSound=sound.id;
            }
          }
          else{
            sound = soundManager.createSound({
               id:idback,
               url:urlback,
               autoLoad: true,
               onplay:self.events.play,
               onstop:self.events.stop,
               onpause:self.events.pause,
               onresume:self.events.resume,
               onfinish:self.events.finish,
               whileloading:self.events.loading,
               whileplaying:self.events.whileplaying,
            });

            // tack on some custom data if needed
            sound._data = {};
            //create a check if sound is playable or not 
            sound.play();
            //set the currentSound to id of the sound currently playing
            self.currentSound=sound.id;

          }//outer else
  }

  this.handleClick = function(e) {
   /* 
      $(document).on("click",".song",function(){
           $this = $(this);
          //not checked if right click
          //check if sound is currently playing 
          id_div_clicked = $this.attr('id');

          if(self.currentSound){//check if sound exist and is playing
            if(id_div_clicked==sound.id){
               console.log('playing sound found state toggled');
               sound.togglePause();
            }
            else{
              //the clicked div is some other sound 
              //stop and unload it

              sound.stop();
              sound.unload();
             // sound.destruct();
              //the sound will not be destroyed it will start from there only
              //+++++maybe we can use destruct here .. doubt .. if it loads the sound again 
              //CHECK LATER sound.destroy()
              sound = soundManager.createSound({
               id:$this.attr('id'),
               url:'http://www.woo55.pk/adata/10430/01.%20A%20Light%20That%20Never%20Comes%20(Linkin%20Park%20%20Steve%20Aoki)%20-%20(www.SongsLover.com).mp3',
               onplay:self.events.play,
               onstop:self.events.stop,
               onpause:self.events.pause,
               onresume:self.events.resume,
               onfinish:self.events.finish,
               whileloading:self.events.loading,
            });

            // tack on some custom data if needed
            sound._data = {};
            //create a check if sound is playable or not 
            sound.play();
            //set the currentSound to id of the sound currently playing
            self.currentSound=sound.id;
            }
           
          }
          else{
            sound = soundManager.createSound({
               id:$this.attr('id'),
               url:'http://www.woo55.pk/adata/9434/01%20Avicii%20-%20Wake%20Me%20Up%20(www.SongsLover.com).mp3',
               onplay:self.events.play,
               onstop:self.events.stop,
               onpause:self.events.pause,
               onresume:self.events.resume,
               onfinish:self.events.finish,
              whileloading:self.events.loading,
            });

            // tack on some custom data if needed
            sound._data = {};
            //create a check if sound is playable or not 
            sound.play();
            //set the currentSound to id of the sound currently playing
            self.currentSound=sound.id;

          }//outer else

      });//documenton click
*/
    //on click events on the bottom bar
    //PLAY PAUSE NEXT PREV
    $('#bLeftPlay img').on('click',function(){
      if(self.currentSound){//check if sound obj exists
        sound.togglePause();
      // change icon to pause
       if(sound.paused){
               
       $('#'+sound.id).find('.play_icon img').attr("src","/static_jb/images/jukebox/icon_new_play.png");
       }
       else{
       
       $('#'+sound.id).find('.play_icon img').attr("src","/static_jb/images/jukebox/icon_new_pause.png");
       } 
        
      
        }
    });

    $('#bLeftLeft img').on('click',function(){
     if(self.shuffle){
           self.playShuffle();
     }
     else{
      if(self.currentSound && ($("#queue_content").find(".qselected").prev().length>0)){//check if sound obj exists
       var a = $("#queue_content").find(".qselected").prev().attr("id");
      //console.log(a);
      var k = a.slice(5,a.length);
      var elm = $("#queue_content").find(".qselected");
      in_queue = true;//song is in the queue 
      elm.prev().addClass("qselected").click();
      elm.removeClass("qselected");
   //   play(parseInt(k));
     }
      }
    });

    $('#bLeftRight img').on('click',function(){
     if(self.shuffle){
           self.playShuffle();
     }
     else{
      if(self.currentSound &&  ($("#queue_content").find(".qselected").next().length>0)){//check if sound obj exists
      var a = $("#queue_content").find(".qselected").next().attr("id");
      console.log(a);
      var k = a.slice(5,a.length);
      var elm = $("#queue_content").find(".qselected");
      in_queue=true;//defines that the song is in the queue 
      elm.next().addClass("qselected").click();
      elm.removeClass("qselected");
     // play(parseInt(k));
      }
      else{
             var temp = $("queue_content").find(".qselected");
             in_queue = true;//song is in the queue 
             $($("#queue_content").children('div')[0]).addClass("qselected").click();
             temp.removeClass("qselected");
             //var k = a.slice(5,a.length);
            // play(parseInt(k));
      }
     }
    });
    //mute button
    $('#volumeicons').on('click',function(){
      volume = $('#volumeicons i');
       if(sound){
        sound.toggleMute();
        }
       if(volume.hasClass( "icon-volume-down" ) || volume.hasClass("icon-volume-up"))
        { volume.removeClass().addClass( "icon-volume-off" ); 

             prevVolume = $('#slider').slider("value");
             $('#slider').slider( "value", 0 );
             if(sound){
              sound.setVolume($('#slider').slider("value"));
              console.log('value set to');
              console.log($('#slider').slider("value"));
              }
              checkmute=1;
        }
        else{
             volume.removeClass().addClass( "icon-volume-up" );
             if(prevVolume){$('#slider').slider( "value", prevVolume );}
             else{$('#slider').slider( "value", 100 );}
             if(sound){
              sound.setVolume( $('#slider').slider("value"));
              console.log('value set to');
              console.log($('#slider').slider("value"));
             }
             checkmute=0;
        }
    });
    
    $("#shufflepic").on("click",function(){
        if(self.shuffle){
           $("#shufflepic").find('img').attr("src","/static_jb/images/jukebox/shufflepic.png");
          self.shuffle=false;
        }
        else{ 
          $("#shufflepic").find('img').attr("src","/static_jb/images/jukebox/shufflepicwhite.png");
          self.shuffle=true;
        }
        
        })
    //volume slider
    $('#slider').slider({
          slide: function(event, ui) {

                volume = $('#volumeicons i');
               var value = $(this).slider('value');
                if(value <= 5) {
                    volume.removeClass().addClass( "icon-volume-off" );
                    if(sound){
                       sound.toggleMute();
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                    checkmute=1;
                }
                else if (value <= 65) {
                    volume.removeClass().addClass( "icon-volume-down" );
                    if(checkmute && sound){
                      checkmute=0;
                      sound.toggleMute();

                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                }
                else {
                    volume.removeClass().addClass( "icon-volume-up" );
                    if(checkmute && sound){
                      checkmute=0;
                      sound.toggleMute();
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                }

            },
            stop: function( event, ui ) {
                var value = $(this).slider('value');
                volume = $('#volumeicons i');
                console.log(value);
                if(value <= 5) { 
                    volume.removeClass().addClass( "icon-volume-off" );
                    if(sound){
                      sound.toggleMute();
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                    checkmute=1;
                }
                else if (value <= 65) {
                    volume.removeClass().addClass( "icon-volume-down" );
                    if(checkmute && sound){
                      checkmute=0;
                      sound.toggleMute();
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                }
                else {
                    volume.removeClass().addClass( "icon-volume-up" );
                    if(checkmute && sound){
                      checkmute=0;
                      sound.toggleMute();
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
               }
            }

    });
    //music slider
    $('#musicSlider').slider({

          slide: function(event, ui) {
          //  $("#musicBlueSlider").css('width',$(this).slider('value'));
          sound.pause();
          },

          stop: function(){
          sound.play();
          console.log("pos"+sound.position);
          console.log("duration"+sound.duration);
         console.log(sound.setPosition(($(this).slider("value")/(100)*(sound.duration))));
         // sound.setPosition(($(this).slider("value")/($(this).width())*(sound.duration)));
        //  console.log($(this).slider("value"))
          }
    });

   //looping
    $("#looppic").on("click",function(){
     if(self.loopSetting==0){
      //setting 0 is default , no looping
      //switch to next state 1
      $("#looppic span").html("1");
     self.loopSetting=1;
     //change css 
      $("#looppic").find('img').attr("src","/static_jb/images/jukebox/looppicwhite.png");
     // self.loopSound(self.currentSound);
         }
     else if(self.loopSetting==1){
      //single song loop
      //switch to next state 2
      self.loopSetting=2;
      //change css
      $("#looppic span").html("");
     }
     else if(self.loopSetting==2){
     //full playlist loop
    //switch  to next state 0
      self.loopSetting=0;
      $("#looppic span").html("");
     //change css
      // $("#looppic").html("<span>0</span>");
      $("#looppic").find('img').attr("src","/static_jb/images/jukebox/looppic.png");
     }
    });

    // keyboard

 // keyboardjs
    KeyboardJS.on('space',function(){
      if(!select){
        $('bLeftPlay').click();
      }
    });

    KeyboardJS.on('ctrl > up',function(){
      r = $('#slider').slider('value') + 10 ;
      $('#slider').slider( "value",r );
      var value = $('#slider').slider('value');
                volume = $('#volumeicons i');
                console.log(value);
                if(value <= 5) { 
                    volume.removeClass().addClass( "icon-volume-off" );
                    if(sound){
                      sound.toggleMute();
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                    checkmute=1;
                }
                else if (value <= 65) {
                    volume.removeClass().addClass( "icon-volume-down" );
                    if(checkmute && sound){
                      checkmute=0;
                      sound.toggleMute();
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                }
                else {
                    volume.removeClass().addClass( "icon-volume-up" );
                    if(checkmute && sound){
                      checkmute=0;
                      sound.toggleMute();
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
               }
            
    });

     KeyboardJS.on('ctrl > down',function(){
      r = $('#slider').slider('value') - 10 ;
      $('#slider').slider( "value",r );

       var value = $('#slider').slider('value');
                volume = $('#volumeicons i');
                console.log(value);
                if(value <= 5) { 
                    volume.removeClass().addClass( "icon-volume-off" );
                    if(sound){
                      sound.toggleMute();
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                    checkmute=1;
                }
                else if (value <= 65) {
                    volume.removeClass().addClass( "icon-volume-down" );
                    if(checkmute && sound){
                      checkmute=0;
                      sound.toggleMute();
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
                }
                else {
                    volume.removeClass().addClass( "icon-volume-up" );
                    if(checkmute && sound){
                      checkmute=0;
                      sound.toggleMute();
                    }
                    if(sound){
                      sound.setVolume(value);
                      console.log('value set to');
                      console.log(value);
                    }
               }
    });

    KeyboardJS.on('ctrl + right',function(){
      inc = $('#musicSlider').width()*0.10;
      c = $("#musicBlueSlider").width() + inc;
      $('bLeftPlay').click();
      $("#musicBlueSlider").width(c);
      $('bLeftPlay').click();


    });

  }//handle click

  this.stopSound = function(oSound) {
   
  }

  this.init = function() {
    //jukebox started
    sm._writeDebug('Jukebox.init()');
    self.handleClick();
      
  }

  this.init();
 //this.handleClick();
}

var Jukebox = null;

soundManager.setup({
  // disable or enable debug output
  debugMode: false,
  // use HTML5 audio for MP3/MP4, if available
  preferFlash: false,
  useFlashBlock: true,
  // path to directory containing SM2 SWF
  url:'/static_jb/swf/jukebox/',
  // optional: enable MPEG-4/AAC support (requires flash 9)
  flashVersion: 9
});

// ----

soundManager.onready(function() {
  // soundManager.createSound() etc. may now be called
  Jukebox = new Player();
});






//  this.position change
