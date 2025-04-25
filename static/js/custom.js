$(window).on('load', function(){
    "use strict";
    /*=========================================================================
            Preloader
    =========================================================================*/
    $("#preloader").delay(750).fadeOut('slow');
});

/*=========================================================================
            Home Slider
=========================================================================*/
$(document).ready(function() {
    "use strict";

    /*=========================================================================
            Slick sliders
    =========================================================================*/
    $('.post-carousel-lg').slick({
      dots: true,
      arrows: true,
      slidesToShow: 1,
      slidesToScroll: 1,
      fade: true,
      cssEase: 'linear',
      responsive: [
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
          }
        }
      ]
    });

    $('.post-carousel-featured').slick({
      dots: true,
      arrows: false,
      slidesToShow: 5,
      slidesToScroll: 2,
      responsive: [
        {
          breakpoint: 1440,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 4,
            dots: true,
            arrows: false,
          }
        },
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
            dots: true,
            arrows: false,
          }
        },
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2,
            dots: true,
            arrows: false,
          }
        }
        ,
        {
          breakpoint: 576,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
          }
        }
      ]
    });

    // Khởi tạo Slick cho post-carousel-twoCol
    $('.post-carousel-twoCol').slick({
      dots: false,
      arrows: false,
      slidesToShow: 2,
      slidesToScroll: 1,
      responsive: [
          {
              breakpoint: 768,
              settings: {
                  slidesToShow: 2,
                  slidesToScroll: 2,
                  dots: false,
                  arrows: false,
              }
          },
          {
              breakpoint: 576,
              settings: {
                  slidesToShow: 1,
                  slidesToScroll: 1,
                  dots: false,
                  arrows: false,
              }
          }
      ]
    });

    // Gắn sự kiện sau khi Slick đã khởi tạo
    $('.carousel-topNav-prev').click(function(){ 
        $('.post-carousel-twoCol').slick('slickPrev');
    });
    $('.carousel-topNav-next').click(function(){ 
        $('.post-carousel-twoCol').slick('slickNext');
    });

    // Khởi tạo Slick cho post-carousel-twoCol
    $('.match-carousel').slick({
      dots: false,
      arrows: false,
      slidesToShow: 6,
      slidesToScroll: 2,
      responsive: [
          {
              breakpoint: 768,
              settings: {
                  slidesToShow: 2,
                  slidesToScroll: 2,
                  dots: false,
                  arrows: false,
              }
          },
          {
              breakpoint: 576,
              settings: {
                  slidesToShow: 1,
                  slidesToScroll: 1,
                  dots: false,
                  arrows: false,
              }
          }
      ]
    });

    // Gắn sự kiện sau khi Slick đã khởi tạo
    $('.carousel-topNav-prev').click(function(){ 
        $('.match-carousel').slick('slickPrev');
    });
    $('.carousel-topNav-next').click(function(){ 
        $('.match-carousel').slick('slickNext');
    });

    $('.post-carousel-widget').slick({
      dots: false,
      arrows: false,
      slidesToShow: 1,
      slidesToScroll: 1,
      responsive: [
        {
          breakpoint: 991,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 1,
          }
        },
        {
          breakpoint: 576,
          settings: {
            slidesToShow: 1,
            centerMode: true,
            slidesToScroll: 1,
          }
        }
      ]
    });
    
    /*=========================================================================
            Sticky header
    =========================================================================*/
    var $header = $(".header-default, .header-personal nav, .header-classic .header-bottom"),
      $clone = $header.before($header.clone().addClass("clone"));

    $(window).on("scroll", function() {
      var fromTop = $(window).scrollTop();
      $('body').toggleClass("down", (fromTop > 300));
    });
    /*=========================================================================
            Search Group Toggle
    =========================================================================*/
    // Xử lý sự kiện click vào nút trigger để mở ô tìm kiếm
    $('.search-group .trigger-btn').on('click', function(e) {
      e.preventDefault(); // Ngăn hành vi mặc định
      e.stopPropagation(); // Ngăn sự kiện lan ra ngoài
      var $searchGroup = $(this).closest('.search-group');
      $searchGroup.addClass('active');

      // Focus vào input khi mở ra
      $searchGroup.find('.search-input').focus();
    });

    // Đóng ô tìm kiếm khi click ra ngoài
    $(document).on('click', function(e) {
        var $searchGroup = $('.search-group');
        if (!$(e.target).closest('.search-group').length && $searchGroup.hasClass('active')) {
            $searchGroup.removeClass('active');
        }
    });

    // Ngăn nút submit đóng ô tìm kiếm khi click
    $('.search-group .submit-btn').on('click', function(e) {
        e.stopPropagation(); // Đảm bảo click nút submit không ảnh hưởng đến logic đóng
    });
    /*=========================================================================
            Share Button Toggle
    =========================================================================*/
    $('.toggle-button.icon-share').on('click', function(e) {
      e.preventDefault();
      var $icons = $(this).next('.icons');
      $icons.toggleClass('visible');
      $(this).toggleClass('active');
    });

    $(document).on('click', function(e) {
        var $toggleButton = $('.toggle-button.icon-share');
        var $icons = $('.icons');
        if (!$(e.target).closest('.toggle-button.icon-share').length && 
            !$(e.target).closest('.icons').length && 
            $icons.hasClass('visible')) {
            $icons.removeClass('visible');
            $toggleButton.removeClass('active');
        }
    });
    
});

$(function(){
    "use strict";

    /*=========================================================================
            Sticky Sidebar
    =========================================================================*/
    $('.sidebar').stickySidebar({
        topSpacing: 100,
        bottomSpacing: 30,
        containerSelector: '.main-content',
    });

    /*=========================================================================
            Vertical Menu
    =========================================================================*/
    $( ".submenu" ).before( '<i class="icon-arrow-down switch"></i>' );

    $(".vertical-menu li i.switch").on( 'click', function() {
        var $submenu = $(this).next(".submenu");
        $submenu.slideToggle(300);
        $submenu.parent().toggleClass("openmenu");
    });

    /*=========================================================================
            Canvas Menu
    =========================================================================*/
    $("button.burger-menu").on( 'click', function() {
      $(".canvas-menu").toggleClass("open");
      $(".main-overlay").toggleClass("active");
    });

    $(".canvas-menu .btn-close, .main-overlay").on( 'click', function() {
      $(".canvas-menu").removeClass("open");
      $(".main-overlay").removeClass("active");
    });

    /*=========================================================================
            Popups
    =========================================================================*/
    $("button.search").on( 'click', function() {
      $(".search-popup").addClass("visible");
    });

    $(".search-popup .btn-close").on( 'click', function() {
      $(".search-popup").removeClass("visible");
    });

    $(document).keyup(function(e) {
          if (e.key === "Escape") { // escape key maps to keycode `27`
            $(".search-popup").removeClass("visible");
        }
    });

    /*=========================================================================
            Tabs loader
    =========================================================================*/
    $('button[data-bs-toggle="tab"]').on( 'click', function() {
      $(".tab-pane").addClass("loading");
      $('.lds-dual-ring').addClass("loading");
      setTimeout(function () {
          $(".tab-pane").removeClass("loading");
          $('.lds-dual-ring').removeClass("loading");
      }, 500);
    });
    
    /*=========================================================================
            Social share toggle
    =========================================================================*/
    // $('.post button.toggle-button').each( function() {
    //   $(this).on( 'click', function(e) {
    //     $(this).next('.social-share .icons').toggleClass("visible");
    //     $(this).toggleClass('icon-close').toggleClass('icon-share');
    //   });
    // });

    /*=========================================================================
    Spacer with Data Attribute
    =========================================================================*/
    var list = document.getElementsByClassName('spacer');

    for (var i = 0; i < list.length; i++) {
      var size = list[i].getAttribute('data-height');
      list[i].style.height = "" + size + "px";
    }

    /*=========================================================================
    Background Image with Data Attribute
    =========================================================================*/
    var list = document.getElementsByClassName('data-bg-image');

    for (var i = 0; i < list.length; i++) {
      var bgimage = list[i].getAttribute('data-bg-image');
      list[i].style.backgroundImage  = "url('" + bgimage + "')";
    }

});

