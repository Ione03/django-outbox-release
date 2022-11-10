/* -------------------------------------
		CUSTOM FUNCTION WRITE HERE
-------------------------------------- */
jQuery(document).on('ready', function() {
	"use strict";
	/* -------------------------------------
			COLLAPSE MENU SMALL DEVICES
	-------------------------------------- */
	function collapseMenu(){
		jQuery('.menu-item-has-children, .menu-item-has-mega-menu').prepend('<span class="tg-dropdowarrow"><i class="fa  fa-angle-right"></i></span>');
		jQuery('.menu-item-has-children span, .menu-item-has-mega-menu span').on('click', function() {
			jQuery(this).next().next().slideToggle(300);
			jQuery(this).parent('.menu-item-has-children, .menu-item-has-mega-menu').toggleClass('tg-open');
		});
	}
	collapseMenu();
	/* -------------------------------------
			SHOW CURRENT DATE
	-------------------------------------- */
	var now = moment().format("dddd, MMM Do, YYYY");
	jQuery('#tg-datebox').append(now);
	/* -------------------------------------
			CHANGE LANGUAGES DATA
	-------------------------------------- */
	jQuery('.tg-languageslist').on("click", "li", function () {
		var currentHTML = this.innerHTML;
		jQuery('#tg-languages').empty();
		jQuery('#tg-languages').append(currentHTML);
	});
	/* -------------------------------------
			OPEN HEADER SEARCH
	-------------------------------------- */
	jQuery('#tg-btnsearch').on('click', function () {
		jQuery('.tg-searchbox form').animate({width: 'toggle'}, {duration: 1000});
	});
	/* -------------------------------------
			MAP CLUSTERING
	-------------------------------------- */
	if(jQuery('#tg-campuseslocation').length > 0 ){
		education_init_map_script('tg-campuseslocation');
	}
	/* -------------------------------------
			MAGA MENU
	-------------------------------------- */
	function hoverIn() {
		var a = jQuery(this);
		var nav = a.closest('#tg-navigation');
		var mega = a.find('.mega-menu');
		var offset = rightSide(nav) - leftSide(a);
		mega.width(Math.min(rightSide(nav), columns(mega)*325));
		mega.css('left', Math.min(0, offset - mega.width()));
	}
	function hoverOut() {}
	function columns(mega) {
		var columns = 0;
		mega.children('.mega-menu-row').each(function () {
			columns = Math.max(columns, jQuery(this).children('.mega-menu-col').length);
		});
		return columns;
	}
	function leftSide(elem) {
		return elem.offset().left;
	}
	function rightSide(elem) {
		return elem.offset().left + elem.width();
	}
	jQuery('#tg-navigation .menu-item-has-mega-menu').hover(hoverIn, hoverOut);
	/* -------------------------------------
			HOME SLIDER
	-------------------------------------- */
	var _tg_homeslider = jQuery('#tg-homeslider');
	_tg_homeslider.owlCarousel({
		items: 1,
		margin: 0,
		nav: true,
		loop: true,
		dots: false,
		//autoplay: true,
		animateIn: 'fadeIn',
		animateOut: 'fadeOut',
		navText: [
			'<i class="fa fa-angle-left"></i>',
			'<i class="fa fa-angle-right"></i>'
		],
		navClass: [
			'tg-btnroundprev tg-btnprev',
			'tg-btnroundnext tg-btnnext'
		]
	});
	/* -------------------------------------
			TICKER SLIDER
	-------------------------------------- */
	var _tg_ticker = jQuery('#tg-ticker');
	_tg_ticker.owlCarousel({
		items: 1,
		margin: 0,
		nav: true,
		loop: true,
		dots: false,
		autoplay: true,
		animateIn: 'fadeIn',
		animateOut: 'fadeOut',
		navText: [
			'<i class="fa fa-angle-left"></i>',
			'<i class="fa fa-angle-right"></i>',
		],
		navClass: [
			'tg-btnsquareprev tg-btnprev',
			'tg-btnsquarenext tg-btnnext'
		]
	});
	/* ---------------------------------------
			MEGA MENU TABS SLIDER
	--------------------------------------- */
	/*var owl = jQuery(".tg-navtabslider");
	owl.owlCarousel({
		itemsCustom : [
				[0, 2],
				[320, 1],
				[639, 2],
				[992, 3],
				[1200, 4],
				[1360, 4],
		],
		pagination: false,
		navigation : true,
		navigationText: [
			'<span class="tg-btnarrowprev"><i class="lnr lnr-arrow-left"></i></span>',
			'<span class="tg-btnarrownext"><i class="lnr lnr-arrow-right"></i></span>'
		],
	});*/
	
	
	/* -------------------------------------
			LATEST NEWS SLIDER
	-------------------------------------- */
	var _tg_navtabslider = jQuery('.tg-navtabslider');
	_tg_navtabslider.owlCarousel({
		nav: true,
		loop: true,
		dots: false,
		responsiveClass:true,
		navText: [
			'<i class="icon-arrow-left"></i>',
			'<i class="icon-arrow-right"></i>',
		],
		navClass: [
			'tg-btnsimpleprev tg-btnprev',
			'tg-btnsimplenext tg-btnnext'
		],
		responsive : {
			0 : {
				items:1,
				nav:true,
			},
			640 : {
				items:2,
				nav:true,
			},
			768 : {
				items:2,
				nav:true,
			},
			992 : {
				items:3,
				nav:true,
			},
			1200 : {
				items:4,
				nav:true,
			}
		}
	});
	
	
	/* -------------------------------------
			PRETTY PHOTO GALLERY
	-------------------------------------- */
	jQuery("a[data-rel]").each(function () {
		jQuery(this).attr("rel", jQuery(this).data("rel"));
	});
	jQuery("a[data-rel^='prettyPhoto']").prettyPhoto({
		animation_speed: 'normal',
		theme: 'dark_square',
		slideshow: 3000,
		autoplay_slideshow: false,
		social_tools: false
	});
	/* -------------------------------------
			LATEST NEWS SLIDER
	-------------------------------------- */
	var _tg_latestnewsslider = jQuery('#tg-latestnewsslider');
	_tg_latestnewsslider.owlCarousel({
		margin: 30,
		nav: true,
		loop: true,
		dots: false,
		responsiveClass:true,
		navText: [
			'<i class="icon-arrow-left"></i>',
			'<i class="icon-arrow-right"></i>',
		],
		navClass: [
			'tg-btnsimpleprev tg-btnprev',
			'tg-btnsimplenext tg-btnnext'
		],
		responsive : {
			0 : {
				items:1,
				nav:true,
			},
			480 : {
				items:2,
				nav:true,
			},
			768 : {
				items:2,
				nav:true,
			},
			992 : {
				items:3,
				nav:true,
			}
		}
	});
	/* -------------------------------------
	 AFFILIATIONS AND CERTIFICATIONS SLIDER
	-------------------------------------- */
	var _tg_affiliationscertificationsslider = jQuery('#tg-affiliationscertificationsslider');
	_tg_affiliationscertificationsslider.owlCarousel({
		margin: 0,
		nav: true,
		loop: true,
		dots: false,
		responsiveClass:true,
		navText: [
			'<i class="icon-arrow-left"></i>',
			'<i class="icon-arrow-right"></i>',
		],
		navClass: [
			'tg-btnsimpleprev tg-btnprev',
			'tg-btnsimplenext tg-btnnext'
		],
		responsive : {
			0 : {
				items:2,
				nav:true,
			},
			480 : {
				items:3,
				nav:true,
			},
			768 : {
				items:4,
				nav:true,
			},
			992 : {
				items:5,
				nav:true,
			}
		}
	});
	/* -------------------------------------
			Google Map
	-------------------------------------- */
	var _tg_campuslocation = jQuery(".tg-campuslocation");
	_tg_campuslocation.gmap3({
		marker: {
			address: "1600 Elizabeth St, Melbourne, Victoria, Australia",
			options: {
				title: "Campus Name",
				icon: "images/campuslocationmarker.png",
			}
		},
		map: {
			options: {
				zoom: 16,
				scrollwheel: false,
				disableDoubleClickZoom: true,
			}
		}
	});
	/* -------------------------------------
			TICKER SLIDER
	-------------------------------------- */
	var _tg_campusslider = jQuery('.tg-campusslider');
	_tg_campusslider.owlCarousel({
		items: 1,
		margin: 0,
		nav: true,
		loop: true,
		dots: false,
		autoplay: true,
		navText: [
			'<i class="icon-arrow-left"></i>',
			'<i class="icon-arrow-right"></i>',
		],
		navClass: [
			'tg-btnsimpleprev tg-btnprev',
			'tg-btnsimplenext tg-btnnext'
		]
	});
	/* -------------------------------------
			COURSE GALLERY SLIDER
	-------------------------------------- */
	var _tg_coursegalleryslider = jQuery("#tg-coursegalleryslider");
	var _tg_coursegallerynav = jQuery("#tg-coursegallerynav");
	var slidesPerPage = 9;
	var syncedSecondary = true;
	_tg_coursegalleryslider.owlCarousel({
		items : 1,
		nav: true,
		loop: true,
		autoplay: true,
		slideSpeed : 2000,
		navText: [
			'<i class="fa fa-angle-left"></i>',
			'<i class="fa fa-angle-right"></i>'
		],
		navClass: [
			'tg-btnroundprev tg-btnprev',
			'tg-btnroundnext tg-btnnext'
		],
		responsiveRefreshRate : 200,
	}).on('changed.owl.carousel', syncPosition);
	_tg_coursegallerynav.on('initialized.owl.carousel', function () {
		_tg_coursegallerynav.find(".owl-item").eq(0).addClass("current");
	})
	.owlCarousel({
		margin: 10,
		smartSpeed: 200,
		slideSpeed: 500,
		items: slidesPerPage,
		slideBy: slidesPerPage,
		responsiveRefreshRate: 100,
		responsiveClass:true,
		responsive : {
			0 : {
				items:3,
			},
			480 : {
				items:5,
			},
			768 : {
				items:5,
			},
			992 : {
				items:7,
			},
			1200 : {
				items:9,
			}
		}
	}).on('changed.owl.carousel', syncPosition2);
	function syncPosition(el) {
		var count = el.item.count-1;
		var current = Math.round(el.item.index - (el.item.count/2) - .5);
		if(current < 0) {
			current = count;
		}
		if(current > count) {
			current = 0;
		}
		_tg_coursegallerynav.find(".owl-item").removeClass("current").eq(current).addClass("current");
		var onscreen = _tg_coursegallerynav.find('.owl-item.active').length - 1;
		var start = _tg_coursegallerynav.find('.owl-item.active').first().index();
		var end = _tg_coursegallerynav.find('.owl-item.active').last().index();
		if (current > end) {
			_tg_coursegallerynav.data('owl.carousel').to(current, 100, true);
		}
		if (current < start) {
			_tg_coursegallerynav.data('owl.carousel').to(current - onscreen, 100, true);
		}
	}
	function syncPosition2(el) {
		if(syncedSecondary) {
			var number = el.item.index;
			_tg_coursegalleryslider.data('owl.carousel').to(number, 100, true);
		}
	}
	_tg_coursegallerynav.on("click", ".owl-item", function(e){
		e.preventDefault();
		var number = jQuery(this).index();
		_tg_coursegalleryslider.data('owl.carousel').to(number, 300, true);
	});
	/* -------------------------------------
			EVENT COUNTER
	-------------------------------------- */
	if (jQuery('#tg-eventcounter').length > 0 ) {
		var _tg_eventcounter = jQuery('#tg-eventcounter');
		_tg_eventcounter.countdown('2018/02/02', function(event) {
			var $this = jQuery(this).html(event.strftime(
				'<div class="tg-counterbox tg-day"><span>%-D</span><span>Days</span></div>' + '<div class="tg-counterbox tg-hours"><span>%H</span><span>hours</span></div>' + '<div class="tg-counterbox tg-minutes"><span>%M</span><span>Minutes</span></div>' + '<div class="tg-counterbox tg-Seconds"><span>%S</span><span>Seconds</span></div>'
			));
		});
	}
	/* -------------------------------------
			Google Map
	-------------------------------------- */
	var _tg_eventlocation = jQuery(".tg-eventlocation");
	_tg_eventlocation.gmap3({
		marker: {
			address: "1600 Elizabeth St, Melbourne, Victoria, Australia",
			options: {
				title: "Event Detail",
				icon: "images/locationmarker.png",
			}
		},
		map: {
			options: {
				zoom: 16,
				scrollwheel: false,
				disableDoubleClickZoom: true,
			}
		}
	});
	/* -------------------------------------
			ADDMISSION SLIDER
	-------------------------------------- */
	var _tg_addmissionslider = jQuery('#tg-addmissionslider');
	_tg_addmissionslider.owlCarousel({
		items: 1,
		margin: 0,
		nav: true,
		loop: true,
		dots: false,
		autoplay: true,
		navText: [
			'<i class="fa fa-angle-left"></i>',
			'<i class="fa fa-angle-right"></i>'
		],
		navClass: [
			'tg-btnroundprev tg-btnprev',
			'tg-btnroundnext tg-btnnext'
		]
	});
	/* --------------------------------------
			THEME COLLAPSE
	-------------------------------------- */
	if(jQuery('#tg-coursesemestercollapse').length > 0 ){
		var _openAll = new jQueryCollapse(
			jQuery('#tg-coursesemestercollapse'),{
				open: function() {this.slideDown('slow');},
				close: function() {this.slideUp('slow')},
			}
		);
		_openAll.open();
	}
	if(jQuery('#tg-programsofferedcollapse').length > 0 ){
		var _closeAll = new jQueryCollapse(
			jQuery('#tg-programsofferedcollapse'),{
				open: function() {this.slideDown('slow');},
				close: function() {this.slideUp('slow')},
				accordion: true,
			}
		);
		_closeAll.close();
	}
	var _elements = jQuery('[id="tg-facultiescollapse"],[id="tg-departmentscollapse"], [id="tg-faqscollapse"]');
	if(_elements.hasClass('tg-themecollapse')){
		var _openFirst = new jQueryCollapse(
			jQuery('.tg-themecollapse'),{
				open: function() {this.slideDown('slow');},
				close: function() {this.slideUp('slow')},
				accordion: true,
			}
		);
		_openFirst.close();
		_openFirst.open(0);
	}
	/* -------------------------------------
			FACULTY SLIDER
	-------------------------------------- */
	var _tg_otherfacultyslider = jQuery('#tg-otherfacultyslider');
	_tg_otherfacultyslider.owlCarousel({
		margin: 30,
		nav: true,
		loop: true,
		dots: false,
		navText: [
			'<i class="icon-arrow-left"></i>',
			'<i class="icon-arrow-right"></i>',
		],
		navClass: [
			'tg-btnsimpleprev tg-btnprev',
			'tg-btnsimplenext tg-btnnext'
		],
		responsiveClass:true,
		responsive : {
			0 : {
				items:1,
			},
			480 : {
				items:2,
			},
			568 : {
				items:3,
			},
			768 : {
				items:2,
			},
			992 : {
				items:4,
			}
		}
	});
	/* ---------------------------------------
			GALLERY FILTERABLE
	-------------------------------------- */
	var $container = jQuery('.tg-galleryfilterable');
	var $optionSets = jQuery('.tg-optionset');
	var $optionLinks = $optionSets.find('a');
	function doIsotopeFilter() {
		if (jQuery().isotope) {
			var isotopeFilter = '';
			$optionLinks.each(function () {
				var selector = jQuery(this).attr('data-filter');
				var link = window.location.href;
				var firstIndex = link.indexOf('filter=');
				if (firstIndex > 0) {
					var id = link.substring(firstIndex + 7, link.length);
					if ('.' + id == selector) {
						isotopeFilter = '.' + id;
					}
				}
			});
			//$(window).load(function () {
				$container.isotope({
					//itemSelector: '.tg-productitem',
					filter: isotopeFilter
				});
			//});
			$optionLinks.each(function () {
				var $this = jQuery(this);
				var selector = $this.attr('data-filter');
				if (selector == isotopeFilter) {
					if (!$this.hasClass('tg-active')) {
						var $optionSet = $this.parents('.option-set');
						$optionSet.find('.tg-active').removeClass('tg-active');
						$this.addClass('tg-active');
					}
				}
			});
			$optionLinks.on('click', function () {
				var $this = jQuery(this);
				var selector = $this.attr('data-filter');
				$container.isotope({itemSelector: '.tg-project', filter: selector});
				if (!$this.hasClass('tg-active')) {
					var $optionSet = $this.parents('.tg-optionset');
					$optionSet.find('.tg-active').removeClass('tg-active');
					$this.addClass('tg-active');
				}
				return false;
			});
		}
	}
	var isotopeTimer = window.setTimeout(function () {
		window.clearTimeout(isotopeTimer);
		doIsotopeFilter();
	}, 1000);
	/*--------------------------------------
			COMMING SOON COUNTER
	--------------------------------------*/
	jQuery('#tg-comingcountdown').countdown('2018/03/27', function(event) {
	var $this = jQuery(this).html(event.strftime(''
		+ '<div class="tg-counter"><div class="tg-counterbox"><span>%D</span><span>days</span></div></div>'
		+ '<div class="tg-counter"><div class="tg-counterbox"><span>%H</span><span>hours</span></div></div>'
		+ '<div class="tg-counter"><div class="tg-counterbox"><span>%M</span><span>minutes</span></div></div>'
		+ '<div class="tg-counter"><div class="tg-counterbox"><span>%S</span><span>seconds</span></div></div>'));
	});
	/* -------------------------------------
			Google Map
	-------------------------------------- */
	var _tg_officelocation = jQuery("#tg-officelocation");
	_tg_officelocation.gmap3({
		marker: {
			address: "1600 Elizabeth St, Melbourne, Victoria, Australia",
			options: {
				title: "Event Detail",
				icon: "images/locationmarker.png",
			}
		},
		map: {
			options: {
				zoom: 20,
				scrollwheel: false,
				disableDoubleClickZoom: true,
			}
		}
	});
	/* -------------------------------------
			TICKER SLIDER
	-------------------------------------- */
	var _tg_campuscarousel = jQuery('#tg-campuscarousel');
	_tg_campuscarousel.owlCarousel({
		margin: 0,
		nav: true,
		loop: true,
		dots: false,
		autoplay: false,
		navText: [
			'<i class="icon-arrow-left"></i>',
			'<i class="icon-arrow-right"></i>',
		],
		navClass: [
			'tg-btnsimpleprev tg-btnprev',
			'tg-btnsimplenext tg-btnnext'
		],
		responsiveClass:true,
		responsive : {
			0 : {
				items:1,
			},
			480 : {
				items:2,
			},
			768 : {
				items:3,
			},
			992 : {
				items:4,
			}
		}
	});
});