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
  this.events = {

    // handlers for sound events as they're started/stopped/played

    play: function() {
       $('#'+sound.id).find('.play_icon i').removeClass('icon-play').addClass('icon-pause');
     //  console.log("--------------"+sound.id); 
    },

    stop: function() {
      $('#'+sound.id).find('.play_icon i').removeClass('icon-pause').addClass('icon-play');

    },

    pause: function() {
    },

    resume: function() {
    },

    finish: function() {
       $("#songLoaded").css('width', '0');
       $("#musicBlueSlider").css('width','0');
       $("#ui-sliderlarge-handle").css('left','0');
       $("#timePlayed").html(0+':'+"00");
       
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
             $($("#queue_content").children('div')[0]).addClass("qselected");
             temp.removeClass("qselected");
             var a = $("#queue_content").find(".qselected").attr("id");
             var k = a.slice(5,a.length);
             in_queue = true;//song is in the queue 
             play(parseInt(k));

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
          var seconds = Math.round(this.position/1000);
          var min=Math.round(seconds/60);
          var sec=Math.round(seconds%60);

          var tseconds= Math.round(this.duration/1000);
          var tmin = Math.round(tseconds/60);
          var tsec=Math.round(tseconds%60);
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
        self.playShuffle();
        return;
      }
      $("#queue_content").find(".qselected").removeClass("qselected");
      //console.log(a);
      $('#queue_content div:nth-child('+index+')').addClass("qselected");
      in_queue=true;
      play(song_random);

  }

  this.play_url = function(idback,urlback){


          $this = $(this);
          //check if sound is currently playing

          if(self.currentSound){//check if sound exist and is playing
            if(idback==sound.id){
               console.log('playing sound found state toggled');
              // sound.togglePause();
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
        //change icon to pause 
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
      elm.prev().addClass("qselected");
      elm.removeClass("qselected");
      in_queue = true;//song is in the queue 
      play(parseInt(k));
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
      elm.next().addClass("qselected");
      elm.removeClass("qselected");
      in_queue=true;//defines that the song is in the queue 
      play(parseInt(k));
      }
      else{
             var temp = $("queue_content").find(".qselected");
             $($("#queue_content").children('div')[0]).addClass("qselected");
             temp.removeClass("qselected");
             var a = $("#queue_content").find(".qselected").attr("id");
             var k = a.slice(5,a.length);
             in_queue = true;//song is in the queue 
             play(parseInt(k));
      }
     }
    });
    //mute button
    $('#volumeicons').on('click',function(){

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
          $("#shufflepic").html("<span>0</span>");
          self.shuffle=false;
        }
        else{ 
          $("#shufflepic").html("<span>1</span>");
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
                }
                else if (value <= 65) {
                    volume.removeClass().addClass( "icon-volume-down" );
                }
                else {
                    volume.removeClass().addClass( "icon-volume-up" );
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
            //$("#musicSlider").css('width',$(this).slider('value'));

          },

          stop: function(){
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
     self.loopSetting=1;
     //change css 
      $("#looppic").html("<span>1</span>");
     // self.loopSound(self.currentSound);
         }
     else if(self.loopSetting==1){
      //single song loop
      //switch to next state 2
      self.loopSetting=2;
      //change css
      $("#looppic").html("<span>2</span>");
     }
     else if(self.loopSetting==2){
     //full playlist loop
    //switch  to next state 0
      self.loopSetting=0;
     //change css
      $("#looppic").html("<span>0</span>");
     }
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
  url:'/static/swf/jukebox/',
  // optional: enable MPEG-4/AAC support (requires flash 9)
  flashVersion: 9
});

// ----

soundManager.onready(function() {
  // soundManager.createSound() etc. may now be called
  Jukebox = new Player();
});
