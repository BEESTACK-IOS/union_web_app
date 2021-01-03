$('#pass, #re_pass').on('keyup', function () {
  if ($('#pass').val() == $('#re_pass').val()) {
    $('#err_message').css('opacity', '0');
    $('#pass_message').html('Parolalar Uyumlu').css('color', 'green');
    $('#guncelle').removeAttr("type").attr("type", "submit");
    $('#guncelle').css('opacity', '1');
  } else {
    $('#err_message').css('opacity', '0');
    $('#pass_message').html('Parolalar Uyumsuz').css('color', 'red');
    $('#guncelle').removeAttr("type").attr("type", "button");
    $('#guncelle').css('opacity', '0.5');
  }
});

$('#past_pass').on('keyup', function () {

    if ($('#past_pass').val().length <= 0) {
        $('#guncelle').removeAttr("type").attr("type", "button");
        $('#guncelle').css('opacity', '0.5');
        $('#past_pass_message').html('Parola Giriniz').css('color', 'red');
    }
    else {
        $('#guncelle').removeAttr("type").attr("type", "submit");
        $('#guncelle').css('opacity', '1');
    }

});