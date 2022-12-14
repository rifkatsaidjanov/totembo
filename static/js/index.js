var owl = $('.owl-carousel');
owl.owlCarousel({
    items:3,
    loop:true,
    margin:80,
    autoplay:true,
    autoplayTimeout:1000,
    autoplayHoverPause:true,
        responsive:{
        0:{
            items:1,
            autoplayTimeout:2000,
        },
        600:{
            items:2,
        },
        768:{
            items:3,
        }
    }
});
$('.play').on('click',function(){
    owl.trigger('play.owl.autoplay',[1000])
})
$('.stop').on('click',function(){
    owl.trigger('stop.owl.autoplay')
})


var owl = $('.product_detail-slider');
owl.owlCarousel({
    items:1,
    loop:true,
    margin:15,
    autoplay:true,
    autoplayTimeout:3000,
    autoplayHoverPause:true
});
$('.play').on('click',function(){
    owl.trigger('play.owl.autoplay',[1000])
})
$('.stop').on('click',function(){
    owl.trigger('stop.owl.autoplay')
})

var owl = $('.customer_reviews-slider');
owl.owlCarousel({
    items:4,
    loop:true,
    margin:0,
    autoplay:true,
    autoplayTimeout:1000,
    autoplayHoverPause:true
});
$('.play').on('click',function(){
    owl.trigger('play.owl.autoplay',[1000])
})
$('.stop').on('click',function(){
    owl.trigger('stop.owl.autoplay')
})


