// ===================show/hide password-login screen==================

function showPassword(){
    var x = document.getElementById("id_password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }

  // jquery for disappearing messages alert automatically
setTimeout(function(){
  $('#messages').fadeOut('slow')
}, 2000)