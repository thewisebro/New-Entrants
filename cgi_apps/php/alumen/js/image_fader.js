// =======================================
 // set the following variables
 // =======================================

 // Set slideShowSpeed (milliseconds)
 var slideShowSpeed = 4000

 // Duration of crossfade (seconds)
 var crossFadeDuration = 1

 // Specify the image files
 var Pic = new Array() // don't touch this
 // to add more images, just continue
 // the pattern, adding to the array below

 Pic[0] = 'images/1.jpg'
 Pic[1] = 'images/2.jpg'
 Pic[2] = 'images/3.jpg'
 Pic[3] = 'images/4.jpg'
 Pic[4] = 'images/5.jpg'
 Pic[5] = 'images/6.jpg'
 Pic[6] = 'images/7.jpg'
 Pic[7] = 'images/8.jpg'
 Pic[8] = 'images/9.jpg'
 Pic[9] = 'images/10.jpg'

 // =======================================
 // do not edit anything below this line
 // =======================================

 var t
 var j = 0
 var p = Pic.length

 var preLoad = new Array()
 for (i = 0; i < p; i++){
    preLoad[i] = new Image()
       preLoad[i].src = Pic[i]
       }

       function runSlideShow(){
          if (document.all){
                document.images.SlideShow.style.filter="blendTrans(duration=2)"
                document.images.SlideShow.style.filter="blendTrans(duration=crossFadeDuration)"
                document.images.SlideShow.filters.blendTrans.Apply()      
          }
         document.images.SlideShow.src = preLoad[j].src
         if (document.all){
                  document.images.SlideShow.filters.blendTrans.Play()
        }
         j = j + 1
          if (j > (p-1)) j=0
       t = setTimeout('runSlideShow()', slideShowSpeed)
      }
window.onload=initializePage();
 
