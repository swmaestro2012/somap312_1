/*Touch Device Detection*/	

  function isTouchDevice(){
	  try{
		  document.createEvent("TouchEvent");
		  //return true;
	  }catch(e){
		  //return false;
	  }
  }
  function touchScroll(id){
	  if(isTouchDevice()){ //if touch events exist...
		  var el=document.getElementById(id);
		  var scrollStartPos=0;

		  document.getElementById(id).addEventListener("touchstart", function(event) {
			  scrollStartPos=this.scrollTop+event.touches[0].pageY;
			  event.preventDefault();
		  },false);

		  document.getElementById(id).addEventListener("touchmove", function(event) {
			  this.scrollTop=scrollStartPos-event.touches[0].pageY;
			  event.preventDefault();
		  },false);
	  }
  }


$(document).ready(function(){


(function(a,b,c){if(c in b&&b[c]){var d,e=a.location,f=/^(a|html)$/i;a.addEventListener("click",function(a){d=a.target;while(!f.test(d.nodeName))d=d.parentNode;"href"in d&&(d.href.indexOf("http")||~d.href.indexOf(e.host))&&(a.preventDefault(),e.href=d.href)},!1)}})(document,window.navigator,"standalone")
	
	  var isiPhone = navigator.userAgent.toLowerCase().indexOf("iphone");
	  var isiPad = navigator.userAgent.toLowerCase().indexOf("ipad");
	  var isiPod = navigator.userAgent.toLowerCase().indexOf("ipod");
	  var isiAndroid = navigator.userAgent.toLowerCase().indexOf("android");
	
	  if(isiPhone > -1)
	  {
		  $('.ipod-detected').hide();
		  $('.ipad-detected').hide();
		  $('.iphone-detected').show();
		  $('.android-detected').hide();
	  }
	  if(isiPad > -1)
	  {
		  $('.ipod-detected').hide();
		  $('.ipad-detected').show();
		  $('.iphone-detected').hide();
		  $('.android-detected').hide();
	  }
	  if(isiPod > -1)
	  {
		  $('.ipod-detected').show();
		  $('.ipad-detected').hide();
		  $('.iphone-detected').hide();
		  $('.android-detected').hide();
	  }   
	  
	  if(isiAndroid > -1)
	  {
		  $('.ipod-detected').hide();
		  $('.ipad-detected').hide();
		  $('.iphone-detected').hide();
		  $('.android-detected').show();
	  }  
	

	  $(".header").swipe( {
		swipeLeft:function(event, direction, distance, duration, fingerCount) {
		  $('.content').css('position', 'absolute');
		  $('.content').animate({
				marginLeft: "0px",
		  }, 150 );
		  $('.deploy-nav').show();
		  $('.hide-nav').hide();
		},
		  swipeRight:function(event, direction, distance, duration, fingerCount) {
		  $('.content').css('position', 'fixed');
		  $('.content').animate({
				marginLeft: "180px",
		  }, 150 );	
		  $('.deploy-nav').hide();
		  $('.hide-nav').show();
		},
		threshold:10
	  });
	  
	  $(".sidebar-header").swipe( {
		swipeLeft:function(event, direction, distance, duration, fingerCount) {
		  $('.content').css('position', 'absolute')  
		  $('.content').animate({
				marginLeft: "0px",
		  }, 150 );	
		  $('.deploy-nav').show();
		  $('.hide-nav').hide();
		},
		  swipeRight:function(event, direction, distance, duration, fingerCount) {
		  $('.content').css('position', 'fixed')
		  $('.content').animate({
				marginLeft: "180px",
		  }, 150 );	
		  $('.deploy-nav').hide();
		  $('.hide-nav').show();
		},
		threshold:10
	  });
	  
	  $('.content').click(function(){
		  $('.content').css('position', 'absolute')
		  $('.content').animate({
				marginLeft: "0px",
		  }, 150 );
		  //$('.sidebar').hide(800);
		  $('.deploy-nav').show();
		  $('.hide-nav').hide();	
	  });
  
	  $('.deploy-nav').click(function(){
		  $('.content').css('position', 'fixed')
		  $('.content').animate({
				marginLeft: "180px",
		  }, 150 );
		  //$('.sidebar').show();
		  $('.deploy-nav').hide();
		  $('.hide-nav').show();
		  return false;
	  });
  
	  $('.hide-nav').click(function(){
		  $('.content').css('position', 'fixed')
		  $('.content').animate({
				marginLeft: "0px",
		  }, 150 );
		  //$('.sidebar').show();
		  $('.deploy-nav').show();
		  $('.hide-nav').hide();
		  return false;
	  });	

	
	$('#sub-menu-one').click(function(){$('.sub-menu-one').toggle(200); return false;});
	$('#sub-menu-two').click(function(){$('.sub-menu-two').toggle(200); return false;});
	$('#sub-menu-three').click(function(){$('.sub-menu-three').toggle(200); return false;});
	$('#sub-menu-four').click(function(){$('.sub-menu-four').toggle(200); return false;});
	$('#sub-menu-five').click(function(){$('.sub-menu-five').toggle(200);});
	$('#sub-menu-six').click(function(){$('.sub-menu-six').toggle(200); return false;});
	$('#sub-menu-seven').click(function(){$('.sub-menu-seven').toggle(200); return false;});
	$('#sub-menu-eight').click(function(){$('.sub-menu-eight').toggle(200); return false;});
	$('#sub-menu-nine').click(function(){$('.sub-menu-nine').toggle(200); return false;});
	$('#sub-menu-ten').click(function(){$('.sub-menu-ten').toggle(200); return false;});
	
	$('.image-slider').roundabout({
		minScale: 0.2,
		autoplay:true,
		autoplayDuration:2000,
		minOpacity:0,
		responsive:true,
		duration: 500
	});


	$('.header-notification').delay(5000).animate({
		  height: "0px",
		  paddingBottom:"0px",
		  marginBottom:"5px",
		  paddingTop:"0px",
	}, 500 ).hide(500);	
	
	
	
	$('.checkbox').click(function(){
		$(this).toggleClass('selected-checkbox');
		return false;
	});
	
	$('.checkbox2').click(function(){
		$(this).toggleClass('selected-checkbox2');
		return false;
	});
	
	$('.radiobox').click(function(){
		$(this).toggleClass('selected-radiobox');
		return false;
	});
	
	$('.radiobox2').click(function(){
		$(this).toggleClass('selected-radiobox2');
		return false;
	});
	


	$(".notification-quit-red").click(function(){
	  $(".notification-box-red").fadeOut(150);
	  return false;
	});
	
	$(".notification-quit-green").click(function(){
	  $(".notification-box-green").fadeOut(150);
	  return false;
	});
	
	$(".notification-quit-yellow").click(function(){
	  $(".notification-box-yellow").fadeOut(150);
	  return false;
	});
	
	$(".notification-quit-blue").click(function(){
	  $(".notification-box-blue").fadeOut(150);
	  return false;
	});
	
	
	$('.toggle-deploy').click(function(){
		$('.toggle-content').show(200);
		$('.toggle-close').show();
		$('.toggle-deploy').hide();
	});
	
	
	$('.toggle-close').click(function(){
		$('.toggle-content').hide(200);
		$('.toggle-close').hide();
		$('.toggle-deploy').show();
	});	
	
	var myPhotoSwipe = $("#gallery a, #gallery2 a").photoSwipe({ enableMouseWheel: false , enableKeyboard: false });

});














