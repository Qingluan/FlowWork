$('#iframe-content').load(function(){
// //     alert("ok")

    
//     var iframe = $('#iframe-content').contents();
//     alert($(this).html());
// //     console.log(iframe);
// //     iframe.find("p").click(function(e) {
// //             i = $(e.target);
// //         console.log("p",i);
// //     })

// //     iframe.find("div").click(function(e) {
// //         i = $(e.target);
// //         alert("div",i);
// //     })

// //     // iframe.find(document).click(function(e){
// //             // i = $(e.target);
// //         // console.log("o ",i);

// })

        

// // });

// // var myConfObj = {
// //   iframeMouseOver : false
// // }
// // window.addEventListener('blur',function(){
// //   if(myConfObj.iframeMouseOver){
// //     console.log('Wow! Iframe Click!');
// //   }
// // });

// // document.getElementById('iframe-content').addEventListener('mouseover',function(){
// //    myConfObj.iframeMouseOver = true;
// // });
// // document.getElementById('iframe-content').addEventListener('mouseout',function(e){
// //     myConfObj.iframeMouseOver = false;
// //     console.log(e);
    $("a").click(function(e){
        alert("div",e.target);
    })
});


// function addEvent(o, evt, func) {
//     if (o.addEventListener) o.addEventListener(evt, func, false);
//     else if (o.attachEvent) o.attachEvent('on' + evt, func);
// }

// function addDocClickEvt(ifr) {
//     addEvent(ifr.contentWindow.document, click, function () {alert('点击了iframe里面的内容') });
// }

