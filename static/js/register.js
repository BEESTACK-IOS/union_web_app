$('#pass, #re_pass').on('keyup', function () {
  if ($('#pass').val() == $('#re_pass').val()) {
    $('#err_message').css('opacity', '0');
    $('#message').html('Parolalar Uyumlu').css('color', 'green');
    $('#signup').removeAttr("type").attr("type", "submit");
    $('#signup').css('opacity', '1');
  } else {
    $('#err_message').css('opacity', '0');
    $('#message').html('Parolalar Uyumsuz').css('color', 'red');
    $('#signup').removeAttr("type").attr("type", "button");
    $('#signup').css('opacity', '0.5');
  }
});