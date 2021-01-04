var recieverid = ""
var recievername = ""
var senderid = ""
var sendername = ""
$(document).on('click','.popUpButton',
function() {
    document.querySelector('.bg-modal').style.display = 'flex';
    console.log($(this).val());
    console.log($(this).attr("name"));
    recievername = console.log($(this).attr("name"));
    recieverid = console.log($(this).val());
    senderame = console.log($("#username").val());
    senderid = console.log($("#userid").val());
});

document.querySelector('.close').addEventListener('click',
function() {
    document.querySelector('.bg-modal').style.display = 'none';
});

