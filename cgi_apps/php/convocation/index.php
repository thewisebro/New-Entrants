<?php
    session_start();
    include("connection.php");
    $dbconn = getConnection();
?>
<!doctype html>
<html>

<head>
	    <meta http-equiv="Content-type" content="text/html"  charset="utf-8">
	    <link rel="stylesheet" href="css/basic.css" type="text/css" />
	    <link rel="stylesheet" href="css/galleriffic-2.css" type="text/css" />
	    <script type="text/javascript" src="js/jquery-1.3.2.js"></script>
	    <script type="text/javascript" src="js/jquery.galleriffic.js"></script>
	    <script type="text/javascript" src="js/jquery.opacityrollover.js"></script>
<script type="text/javascript">
	document.write('<style>.noscript { display: block; }</style>');
	function home_page(){
		window.location = "index.php";
	}
</script>
</head>
<body>
 <div id="page">
	<div id="container">
	<div id="topbar">
	<div id="heading" style="width=800px; float:left; font-size:30pt;">
	<p onClick=home_page() style="cursor:pointer"><span>Convocation 2013</span></p>
	</div>
	<div id="login" style="width=100px; float:right; ">
	<?php
            if(isset($_SESSION['loggedin']) && ($_SESSION['loggedin'] == true))
	    {
	?>
	<span>Welcome Admin &nbsp;<a href="logout.php">Logout</a></span><p>
	<span><a href="upload.php">Upload Photo</a>&nbsp; &nbsp; <a href="delete.php">Delete Photo</a></span>
	<?php
	    }
	?>
	</div>
	<div style="clear:both;"></div>
	</div>
		<div id="gallery" class="content">
		         <div id="controls" class="controls"></div>
			<div class="slideshow-container">
				<div id="loading" class="loader"></div>
				<div id="slideshow" class="slideshow"></div>
			</div>
		<div id="caption" class="caption-container"></div>
		</div>
	<div id="thumbs" class="navigation">
    	<ul class="thumbs noscript">
     			<?php 
	$query1="Select old_location from convo13_photos; ";
     
     	$result1=pg_query($dbconn,$query1);
	while ($val=pg_fetch_row($result1))
	{
     ?>
	    
		<li>
	               <a class="thumb" name="optionalCustomIdentifier" href="<?php echo $val[0];  ?>" title="<?php echo $val[0]; ?>">
		       		<img width="81px" height="81px" src="<?php echo $val[0]; ?>" /></a> 
		</li>
	    <?php
	    }
	    ?>
	    
        </ul>
	</div>
 	<div style="clear: both;"></div>
      </div>
</div>
<script type="text/javascript">
			jQuery(document).ready(function($) {
				// We only want these styles applied when javascript is enabled
				$('div.navigation').css({'width' : '300px', 'float' : 'left'});
				$('div.content').css('display', 'block');

				// Initially set opacity on thumbs and add
				// additional styling for hover effect on thumbs
				var onMouseOutOpacity = 0.67;
				$('#thumbs ul.thumbs li').opacityrollover({
					mouseOutOpacity:   onMouseOutOpacity,
					mouseOverOpacity:  1.0,
					fadeSpeed:         'fast',
					exemptionSelector: '.selected'
				});
				
				// Initialize Advanced Galleriffic Gallery
				var gallery = $('#thumbs').galleriffic({
					delay:                     2500,
					numThumbs:                 15,
					preloadAhead:              10,
					enableTopPager:            true,
					enableBottomPager:         true,
					maxPagesToShow:            7,
					imageContainerSel:         '#slideshow',
					controlsContainerSel:      '#controls',
					captionContainerSel:       '#caption',
					loadingContainerSel:       '#loading',
					renderSSControls:          true,
					renderNavControls:         true,
					playLinkText:              'Play Slideshow',
					pauseLinkText:             'Pause Slideshow',
					prevLinkText:              '&lsaquo; Previous Photo',
					nextLinkText:              'Next Photo &rsaquo;',
					nextPageLinkText:          'Next &rsaquo;',
					prevPageLinkText:          '&lsaquo; Prev',
					enableHistory:             false,
					autoStart:                 false,
					syncTransitions:           true,
					defaultTransitionDuration: 900,
					onSlideChange:             function(prevIndex, nextIndex) {
						// 'this' refers to the gallery, which is an extension of $('#thumbs')
						this.find('ul.thumbs').children()
							.eq(prevIndex).fadeTo('fast', onMouseOutOpacity).end()
							.eq(nextIndex).fadeTo('fast', 1.0);
					},
					onPageTransitionOut:       function(callback) {
						this.fadeTo('fast', 0.0, callback);
					},
					onPageTransitionIn:        function() {
						this.fadeTo('fast', 1.0);
					}
				});
			});
		</script>
</body>
</html>
