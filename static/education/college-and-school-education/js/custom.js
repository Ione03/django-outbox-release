/*==================================================================
[ Back to top ]*/
try {
    var windowH = $(window).height()/2;

    $(window).on('scroll',function(){
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").addClass('show-btn-back-to-top');
        } else {
            $("#myBtn").removeClass('show-btn-back-to-top');
        }
    });

    $('#myBtn').on("click", function(){
        $('html, body').animate({scrollTop: 0}, 300);
    });
} catch(er) {console.log(er);}