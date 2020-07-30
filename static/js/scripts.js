$(document).ready(function(){
  $('.post-wrapper').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2000,
    nextArrow: $('.next'),
    prevArrow: $('.prev'),
  });

  // $('.post-wrapper2').slick({
  //   slidesToShow: 5,
  //   slidesToScroll: 1,
  //   autoplay: true,
  //   autoplaySpeed: 2000,
  //   nextArrow: $('.next2'),
  //   prevArrow: $('.prev2'),
  // });
  $('.post-wrapper2').slick({
  infinite: true,
  slidesToShow: 3,
  slidesToScroll: 3,
  nextArrow: $('.next2'),
  prevArrow: $('.prev2'),
});

});
