$(document).ready(function(){
    
    $('.video').on('click', function(){
        console.log($(this));
        localStorage.setItem("at", $(this).attr('id'));
        document.location.href = "../templates/single_video.html";
    });
});
