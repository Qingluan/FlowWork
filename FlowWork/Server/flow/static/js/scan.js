// $('#iframe-content').load(function(){

//     after_load();

// });


function after_load(){
    $(".process-bar-load").modal();
    $(window.frames[0].document).click(function(e){
        console.log(e.target)
        s = $(e.target)
        idv = s.attr('id')
        clv = s.attr('class')
        tv = e.target.tagName
        $("#attrs").append("<li>"+tv + "." + clv+"#"+idv);
    })
    $(window.frames[0].document).find("input").focus(function(e){
        console.log('in:',e.target)
        s = $(e.target)
        idv = s.attr('id')
        clv = s.attr('class')
        tv = e.target.tagName
        $("#attrs").append("<li>"+tv + "." + clv+"#"+idv);
    })    
}
