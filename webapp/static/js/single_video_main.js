let last_grade;

$(document).ready(function(){
    $('.like').on('click', function(){
        if (last_grade===1) {
            $(this).attr('src', '../static/img/like.png');
            last_grade = undefined;
        } else if (last_grade===0) {
            $('.dislike').attr('src', '../static/img/dislike.png');
            $(this).attr('src', '../static/img/fill_like.png');
            last_grade = 1;
        } else {
            $(this).attr('src', '../static/img/fill_like.png');
            last_grade = 1;
        };
    });
    $('.dislike').on('click', function(){
        if (last_grade===0) {
            $(this).attr('src', '../static/img/dislike.png');
            last_grade = undefined;
        } else if (last_grade===1) {
            $('.like').attr('src', '../static/img/like.png');
            $(this).attr('src', '../static/img/fill_dislike.png');
            last_grade = 0;
        } else {
            $(this).attr('src', '../static/img/fill_dislike.png');
            last_grade = 0;
        };
    });
    $('.logo').on('click', function(){
        document.location.href = "../templates/recomendation.html";
    });
});
let at = localStorage.getItem("at");
console.log(at);