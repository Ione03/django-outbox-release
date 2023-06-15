let $slider = $('.slider-item');
let currentSliderItem = 0;
let currentSliderItemPrev = 0;
let int_interval = 5000;
let sliderInterval = 0; // setInterval(nextSlide, int_interval);

let playing = true;
let $pausePlayButton = $('#pause-play');
let $nextButton = $('#next');
let $previousButton = $('#previous');

let $sliderPanel = $('.slider-panel');
let $indContainer = $('.slider-panel__navigation');
let $indItem = $('.indicator');
let style = ""
let imgList = []

// update to make slide show text too...
let titleList = []
let subtitleList = []
let contentList = []

function getImage() {
    //console.log('enter image');
    $.each($slider, function (i, val) {
        //console.log(i, $(val).css('background-image'));
        imgList.push($(val).css('background-image'));

        titleList.push($(val).find(".title").text());
        subtitleList.push($(val).find(".sub-title").text());
        contentList.push($(val).find(".content").text());

        //console.log(titleList, subtitleList, contentList);
    });
    //console.log(imgList[0]);
}

function nextSlide() {
    goToSlide(currentSliderItem + 1);
}

function prevSlide() {
    goToSlide(currentSliderItem - 1);
}

function goToSlide(n) {
    //$($slider[currentSliderItem]).toggleClass('active');
    $($indItem[currentSliderItem]).attr('class', 'far fa-circle indicator');
    
    currentSliderItemPrev = currentSliderItem;
    //style = $($slider[currentSliderItemPrev]).attr('style');
    
    currentSliderItem = ($slider.length + n) % $slider.length;
    //console.log(style);
    
    //$($slider[currentSliderItem]).toggleClass('active');
    
    //console.log(n, currentSliderItem);
    
    //$($slider[currentSliderItem]).fadeIn(1500);
    
    //$($slider[currentSliderItem]).fadeIn(1500,function() {
        //$($slider[currentSliderItem]).attr('style',style);
    //    $($slider[currentSliderItem]).fadeOut(1000);
    //});
    $('.slider-item-show').fadeIn(int_interval,function() {
        
        $('.slider-item-show').css({
            'background-image': imgList[currentSliderItem]
        });

        $('.slider-item-show').find('.title').text(titleList[currentSliderItem]);
        $('.slider-item-show').find('.sub-title').text(subtitleList[currentSliderItem]);
        $('.slider-item-show').find('.content').text(contentList[currentSliderItem]);
        
        
        $('.slider-item-show').fadeIn(int_interval);
        //
    });
    
    
    $($indItem[currentSliderItem]).attr('class', 'fas fa-circle indicator');
}

function pauseSlideShow() {
    $pausePlayButton.attr('class', 'far fa-play-circle');
    playing = false;
    clearInterval(sliderInterval);
}

function playSlideShow() {
    $pausePlayButton.attr('class', 'far fa-pause-circle');
    playing = true;
    sliderInterval = setInterval(nextSlide, int_interval);
}

$sliderPanel.css('display', 'flex');

$pausePlayButton.on('click', () => {
    if (playing) pauseSlideShow();
    else playSlideShow();
});

$nextButton.on('click', () => {
    pauseSlideShow();
    nextSlide();
});

$previousButton.on('click', () => {
    pauseSlideShow();
    prevSlide();
});

$indContainer.on('click', (event) => {
    
    
    let target = event.target;

    if (target.classList.contains('indicator')) {
        pauseSlideShow();
        goToSlide(+target.getAttribute('data-slide-to'));
    }
});

//---------------------------------------------------------------------
$(document).on('keydown', keyNavigation);
$(document).ready(function () {
    getImage();
    $('.slider-item-show').css({
        'background-image': imgList[0]
    });

    $('.slider-item-show').find('.title').text(titleList[0]);
    $('.slider-item-show').find('.sub-title').text(subtitleList[0]);
    $('.slider-item-show').find('.content').text(contentList[0]);
    
    sliderInterval = setInterval(nextSlide, int_interval);

});

function keyNavigation(event) {
    
    if (event.code === 'ArrowLeft') { //стрелка влево
        pauseSlideShow();
        prevSlide();
    }
    if (event.code === 'ArrowRight') { //стрелка вправо
        pauseSlideShow();
        nextSlide();
    }
    if (event.code === 'Space') { //пробел
        if (playing) pauseSlideShow();
        else playSlideShow();
    }
}

//---------------------------------------------------------------------
