//global vars
var modal = $('script[src*=page]').attr('modal');
var ChosenProBot = $('script[src*=page]').attr('ChosenProBot');
var ControlPage = $('script[src*=page]').attr('ControlPage');
var AdminPage = $('script[src*=page]').attr('AdminPage');
var page = location.pathname.split("/").pop();
var isPhoneDevice = "ontouchstart" in document.documentElement;
var available = 0; var online = 0; var total = 0;
var afking = 0;

var INC = 0.080;
var MAX = 0.750;

function AdminPageType(){
if (AdminPage == 'databaseInfo'){
  showAdminDatabase();
}
if (AdminPage == 'ProBotInfo'){
  showAdminProBotInfo();
}
}

function showAdminDatabase() {
  document.getElementById("databaseInfo").style.display="block";
  document.getElementById("ProBotInfo").style.display="none";
  
}

function showAdminProBotInfo (){
  document.getElementById("databaseInfo").style.display="none";
  document.getElementById("ProBotInfo").style.display="block";
}

function incDirValue(dir) {
  dir = dir + INC;
  if (dir >= MAX) {
    dir = MAX;
  }
  return dir;
}

$(document).ready(function () {
  mainjs();

  if (!isNaN(page) && (function(x) { return (x | 0) === x; })(parseFloat(page))){
    page="admin";
  }

  switch (page) {
    case "":
      index()
      break;
    case "admin":
      admin()
      AdminPageType()
      break;
    case "user":
      if (ControlPage != "active") { user(); }
      else { active(); }
      break;
  }
});

// global js
function mainjs() {
  // between modals
  $('#loginModal').on('show.bs.modal', function () {
    $('#registerModal').modal('hide');
    $('#recoverModal').modal('hide');
  });
  $('#registerModal').on('show.bs.modal', function () {
    $('#loginModal').modal('hide');
  });
  $('#recoverModal').on('show.bs.modal', function () {
    $('#loginModal').modal('hide');
  });
  $('#loginModal').on('hidden.bs.modal', function () {
    $("#WTFLoginErrorsEmail").hide();
    $("#WTFLoginErrorsPassword").hide();
    $("#loginMsgs").hide();
  });
  $('#registerModal').on('hidden.bs.modal', function () {
    $("#WTFRegisterErrorsPassword").hide();
    $("#WTFRegisterErrorsConfirm").hide();
    $("#registerMsgs").hide();
  });
  $('#unconfirmedModal').on('hidden.bs.modal', function () {
    $("#unconfirmedMsgs").hide();
  });
  $('#changePasswordModal').on('hidden.bs.modal', function () {
    $("#changePasswordMsgs").hide();
  });
  $('#recoverModal').on('hidden.bs.modal', function () {
    $("#recoverMsgs").hide();
  });

  // alert-dismiss
  $("#dropdown-alert").delay(3000).slideUp(300);

  // tooltips
  $('[data-toggle="tooltip"]').tooltip();

  // modal request
  if (modal != "") {
    openModal(modal);
  }
}

function index() {
  var albumImages;

  // navbar-shrink
  navbarCollapse()
  $(window).scroll(navbarCollapse);

  if (!isPhoneDevice) {
    // fadein animation
    wow = new WOW({ offset: 50 });
    wow.init();
  } else {
    $("#bg-video").remove();
    // gallery mobile-swipe
    $("#carousel").on("swipeleft", function () { $('#carousel').carousel('next'); });
    $("#carousel").on("swiperight", function () { $('#carousel').carousel('prev'); });
  }

  // gallery-filter animation
  var mixer = mixitup(document.querySelector('#portfolioList'), {
    selectors: { control: '[data-mixitup-control]' }
  });

  // menu-links trigger
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) { $('html, body').animate({ scrollTop: (target.offset().top - 69) }, 1000, "easeInOutExpo"); return false; }
    }
  });

  // collapse-menu bc-ground
  $('.js-menu-trigger').click(function () {
    if ($('.js-menu-trigger').attr('aria-expanded') == "false") {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      if ($("#mainNav").offset().top < 50) {
        $("#mainNav").removeClass("navbar-shrink");
      }
    }
  });

  // collapse-menu trigger
  $('.js-scroll-trigger').click(function () {
    $('.navbar-collapse').collapse('hide');
  });

  // gallery setup
  $('.js-modal-trigger').click(gallerySetup);

  // team-gallery setup
  $(".team-carousel").owlCarousel({
    items: 3, mouseDrag: false,
    navigation: true, pagination: false,
    autoWidth: true, responsiveClass: true,
    responsive: {
      0: { items: 2, nav: true },
      1024: { items: 3, nav: true, loop: false }
    },
    navigationText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
  });

  $('body').scrollspy({
    target: '#mainNav',
    offset: 70
  });

  // album-data query
  $.getJSON("/ResultSearchPhotos",
    function (data) {
      albuns = data.listOfFiles;
    });

  // index functions
  function navbarCollapse() {
    if ($("#mainNav").offset().top > 50) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
    if (!isPhoneDevice) {
      if ($("#mainNav").offset().top > 1000) {
        document.getElementById("bg-video").pause();
      } else {
        document.getElementById("bg-video").play();
      }
    }
  };
  function gallerySetup() {
    //empty content
    $(".gallery-modal .carousel-inner").empty();

    // new photos
    albuns.forEach(element => {
      if (element[0] == $(this).find('.text-title').text()) {
        albumImages = element[1].split(',');
        albumImages.forEach(function (image, i) {
          if (i == 0) {
            var firstImg = "active";
            $('.gallery-modal .carousel-possition').text("1-" + albumImages.length);
            $('.gallery-modal .close').show();
            $('.gallery-modal .carousel-control-prev').show();
            $('.gallery-modal .carousel-control-next').show();
          } else { firstImg = "" }
          var img = new Image();
          img.src = '../static/gallery/' + element[0] + '/' + image;
          img.onload = function () {
            $('.gallery-modal .carousel-inner').append('<div class="carousel-item ' + firstImg + '"><img src="' + this.src + '"></div>');
          };
        });
      }
    });

    // image nrº
    $(".carousel").on("slide.bs.carousel", function (ev) {
      $('.gallery-modal .carousel-possition').text(($(ev.relatedTarget).index() + 1) + "-" + albumImages.length);
    });

    // gallery alignment
    $('.gallery-modal').on('shown.bs.modal', function () { $(".gallery-modal").css("display", "flex"); });
  };
}

function user() {
  var temp = []; var probots = []; var newProbots = [];

  // probots query
  setInterval(function probots_query() {
    $.getJSON("/AddProbot",
      function (data) {
        if (probots.length == 0) {
          probots = data.listOfFiles;
          probotsSetup()
        } else {
          newProbots = data.listOfFiles;
          updateProbots()
        }
      });
  }, 1000);

  // user functions
  function probotsSetup() {
    probots.forEach(robot => { addProBot(robot) });

    // probots-gallery
    $(".team-carousel.probots").owlCarousel({
      items: 3, mouseDrag: false,
      navigation: true, pagination: false,
      autoWidth: true, responsiveClass: true,

      navigationText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    });
 
  }



  function addProBot(robot) {
    robot = robot.split(",");
    if (robot[1] == "NotWorking") {
      var img = "'../static/resources/images/probots/NotWorking.png'";
      $(".team-carousel.probots").append('<div class="item cover" style="background-image: url(' + img + ')"><div class="cover"></div></div>');
    } else {
      var img = "'../static/resources/images/probots/" + robot[0].toLowerCase() + ".png'";

      temp = checkProBot(robot);
      if (temp[0] == "cover") {
        $(".team-carousel.probots").append('<div class="item ' + temp[0] + '" style="background-image: url(' + img + ')"><div class="' + temp[0] + '"><div class="team-caption ' + temp[1] + '"><h3>' + robot[0] + '</h3><hr class="colored"><i class="fas fa-power-off fa-2x" style="color:' + temp[2] + '"></i><i class="fas fa-' + temp[3] + '-circle fa-2x" style="color:' + temp[4] + '"></i></div></div></div>');
      } else {
        var onClick = "var current_user_probot_control = $('#current_user_probot_control').data('playlist'); if (current_user_probot_control=='True'){if(typeof document.addEventListener === 'undefined' || hidden === undefined){$('#noticeModal').modal('show')} else {$(this).closest('form').submit()}} else{$('#WithoutPermission').modal('show')}";
        $(".team-carousel.probots").append('<form method="post" action="/user"><input type="hidden" name="ChosenProBot" value=' + robot[0] + '><a id="probot" onclick="' + onClick + '"><div class="item ' + temp[0] + '" style="background-image: url(' + img + ')"><div class="' + temp[0] + '"><div class="team-caption ' + temp[1] + '"><h3>' + robot[0] + '</h3><hr class="colored"><i class="fas fa-power-off fa-2x" style="color:' + temp[2] + '"></i><i class="fas fa-' + temp[3] + '-circle fa-2x" style="color:' + temp[4] + '"></i></div></div></div></a></form>');
      }


      // update count
      updateValues();
    }
  }
  function updateProbots() {
    newProbots.forEach(function (newData, i) {
      
      
      // check changes
      if (newData != probots[i]) {
        var robot = newData.split(",");

        temp = checkProBot(robot);
        var img = "'../static/resources/images/probots/" + robot[0].toLowerCase() + ".png'";
        if (temp[0] == "cover") {
          $('.team-carousel.probots .owl-wrapper .owl-item').children().eq(i).replaceWith('<div class="item ' + temp[0] + '" style="background-image: url(' + img + ')"><div class="' + temp[0] + '"><div class="team-caption ' + temp[1] + '"><h3>' + robot[0] + '</h3><hr class="colored"><i class="fas fa-power-off fa-2x" style="color:' + temp[2] + '"></i><i class="fas fa-' + temp[3] + '-circle fa-2x" style="color:' + temp[4] + '"></i></div></div></div>');
        } else {
          var onClick = "var current_user_probot_control = $('#current_user_probot_control').data('playlist'); if (current_user_probot_control=='True'){if(typeof document.addEventListener === 'undefined' || hidden === undefined){$('#noticeModal').modal('show')} else {$(this).closest('form').submit()}} else{$('#WithoutPermission').modal('show')}";
          $('.team-carousel.probots .owl-wrapper .owl-item').children().eq(i).replaceWith('<form method="post" action="/user"><input type="hidden" name="ChosenProBot" value=' + robot[0] + '><a id="probot" onclick="' + onClick + '"><div class="item ' + temp[0] + '" style="background-image: url(' + img + ')"><div class="' + temp[0] + '"><div class="team-caption ' + temp[1] + '"><h3>' + robot[0] + '</h3><hr class="colored"><i class="fas fa-power-off fa-2x" style="color:' + temp[2] + '"></i><i class="fas fa-' + temp[3] + '-circle fa-2x" style="color:' + temp[4] + '"></i></div></div></div></a></form>');
        }

        // remove old count
        var oldData = probots[i].split(",");
        if (oldData[1] != "NotWorking") {
          total -= 1;
          if (oldData[1] == "NotAvailable" || oldData[1] == "Available") {
            online -= 1;
            if (oldData[1] == "Available") {
              available -= 1;
            }
          }
        }

        // update count
        updateValues();
      }
    });
    probots = newProbots;
  }
}

function active() {
  var interval; var repGP; var data; var temp = true; var serverConnection; var connectionDelay; var imUsingIt; var interval_nipple;

  // Visibility API
  var hidden, visibilityChange;
  if (typeof document.hidden !== "undefined") {
    hidden = "hidden";
    visibilityChange = "visibilitychange";
  } else if (typeof document.msHidden !== "undefined") {
    hidden = "msHidden";
    visibilityChange = "msvisibilitychange";
  } else if (typeof document.webkitHidden !== "undefined") {
    hidden = "webkitHidden";
    visibilityChange = "webkitvisibilitychange";
  } else if (typeof document.mozHidden !== "undefined") {
    hidden = "mozHidden";
    visibilityChange = "webkitvisibilitychange";
  }
  document.addEventListener(visibilityChange, handleVisibilityChange, false);

  if (isPhoneDevice) {
    $("#active").addClass("full-screen");
    $("#active .settings").hide();
    $("#active .btn-information").show();

    // Force landscape
    PleaseRotateOptions = {
      forceLandscape: true,
      allowClickBypass: false,
      subMessage: "To show the Menu rotate back to vertical",
      onHide: function () {
        $("footer").hide();
        $("nav").hide();
        if (temp) {
          $("#infoModal").modal("show");
          setupNipples();
          clearInterval(interval);
          temp = false;
        }
      },
      onShow: function () {
        $("nav").show();
        $("#infoModal").modal("hide");

      }
    };
    var script = document.createElement("script");
    script.setAttribute("src", "/static/resources/rotation.js");
    document.body.appendChild(script);
  }

  // status-confirmation
  imUsingIt = setInterval(function () {
    $.post("/ProBotInUse", {
      ProBotInUse: String('[[' + JSON.stringify(ChosenProBot) + ', "NotAvailable"]]')
    });
  }, 1000);

  // ProBots values
  connectionDelay = setTimeout(function () {
    serverConnection = setInterval(function probots_query() {
      $.getJSON("/ProBotTelemetry",
        function (values) {
          values = values.ProBotTelemetry.split(",");
          if (values[0] == ChosenProBot) {
            values.forEach(element => {
              // Battery
              if (isNaN(values[1])) { $(".fa-stack.battery").text("0%"); }
              else { $(".fa-stack.battery").text(values[1] + "%"); }

              $(".battery-icon").removeClass("fa-battery-full").removeClass("fa-battery-half").removeClass("fa-battery-quarter").removeClass("def");
              if (values[1] > 75) { $(".battery-icon").addClass("fa-battery-full"); }
              else if (values[1] > 25 && values[1] <= 75) { $(".battery-icon").addClass("fa-battery-half"); }
              else { $(".battery-icon").addClass("fa-battery-quarter"); }

              // Degrees
              $(".male").removeClass("fa-male").removeClass("fa-rotate-90").removeAttr( 'style' );
              if ((values[2] >= 70) && (values[2] <= 120))  { 
                $(".male").addClass("fa-male")
                $(".male").css("color", "green");
                
              }

              // Latency
              $(".signal").removeClass("signal-5").removeClass("signal-4").removeClass("signal-3").removeClass("signal-2").removeClass("signal-1").removeClass("def");
              if (values[4] < 50) { $(".signal").addClass("signal-5"); }
              else if (values[4] < 100) { $(".signal").addClass("signal-4"); }
              else if (values[4] < 150) { $(".signal").addClass("signal-3"); }
              else if (values[4] < 200) { $(".signal").addClass("signal-2"); }
              else {
                $(".signal").addClass("signal-1");
                $("#noticeModal").modal("show");
                endServerConnection()
              }
            });
          }
        });

      // afk check
      afking += 1;
      if (afking == 3600000) { $("#redirectModal").modal("show"); }
    }, 1000);
  }, 3000);

  // full-screen
  $('.btn-fullscreen').click(function () {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $("#active .mobile").css("display", "block");
      $("#active").removeClass("full-screen");
      $("footer").show();
      $("nav").show();
    } else {
      $(this).addClass("active");
      $("#active .mobile").css("display", "none");
      $("#active").addClass("full-screen");
      $("footer").hide();
      $("nav").hide();
    }
  });

  // controller-modal
  $('.btn.btn-modal').click(function () {
    $('.btn.btn-modal').removeClass("selected");
    $(this).addClass("selected");
    $('.js-save-trigger').prop('disabled', false);
    $('.js-save-trigger').removeClass("disabled");
  });

  $('.js-save-trigger').click(function () {
    $('.modal .close').show();

    $(".gamepad").addClass("d-none");
    $(".keyboard").addClass("d-none");
    if ($('.btn.btn-modal').eq(0).hasClass('selected')) {
      $(".gamepad").removeClass("d-none");
      gamepadSetup();
    } else if ($('.btn.btn-modal').eq(1).hasClass('selected')) {
      $(".keyboard").removeClass("d-none");
      keyboardSetup();
    }
  });

  // modals
  $('#noticeModal').on('show.bs.modal', function () {
    $('#infoModal').modal('hide');
    $('#controllerModal').modal('hide');
    $('#redirectModal').modal('hide');
    endServerConnection()
  });
  $('#redirectModal').on('show.bs.modal', function () {
    $('#infoModal').modal('hide');
    $('#controllerModal').modal('hide');
    $('#noticeModal').modal('hide');
    endServerConnection()
  });

  function keyboardSetup() {
    clearInterval(repGP);
    interval = null;
    var up = 0; var down = 0; var left = 0; var right = 0;
    var keys = {},
      keysCount = 0,
      trackedKeys = {
        37: true, // left
        38: true, // up
        39: true, // right
        40: true // down
      };

    // key pressed
    $(document).keydown(function (event) {

      var code = event.which;
      if (trackedKeys[code]) {
        if (!keys[code]) {
          keys[code] = true;
          keysCount++;
        }

        if (interval === null) {
          interval = setInterval(function () {
            var direction = "";
            if (keys[38] && keys[37]) { up = incDirValue(up); left = incDirValue(left); }
            if (keys[38] && keys[39]) {up = incDirValue(up);  right = incDirValue(right); }
            if (keys[40] && keys[37]) { down = incDirValue(down); left = incDirValue(left); }
            if (keys[40] && keys[39]) { down = incDirValue(down); right = incDirValue(right); }

            if (keys[38]) { up = incDirValue(up); }
            if (keys[40]) {down = incDirValue(down); }
            if (keys[37]) { left = incDirValue(left); }
            if (keys[39]) { right = incDirValue(right); }

            sendData(up, down, left, right)
          }, 1000 / 50);
        }
      }
    });

    // key released
    $(document).keyup(function (event) {
      $(".keyboard").css("color", "green");
      var code = event.which;
      if (keys[code]) {
        if (keys[38]) { up = 0; }
        if (keys[40]) { down = 0; }
        if (keys[37]) { left = 0; }
        if (keys[39]) { right = 0; }
        
        delete keys[code];
        keysCount--;
      }

      if ((trackedKeys[code]) && (keysCount === 0)) {
        clearInterval(interval);
        interval = null;
        up = 0; down = 0; left = 0; right = 0;
        sendData(up, down, left, right)
      }
    });
  }
  function gamepadSetup() {
    interval = "";
    clearInterval(interval);
    document.onkeydown = null;
    document.onkeyup = null;
    var up = 0; var down = 0; var left = 0; var right = 0;
    $(".keyboard").css("color", "red");

    function reportOnGamepad() {
      var gp = navigator.getGamepads()[0];
      if (gp.axes[1] == 0) { up = 0; down = 0; }
      if (gp.axes[1] < 0) { up = gp.axes[1] * -1; down = 0; }
      if (gp.axes[1] > 0) { down = gp.axes[1]; up = 0; }
      if (gp.axes[2] == 0) { left = 0; right = 0; }
      if (gp.axes[2] < 0) { left = gp.axes[2] * -1; right = 0; }
      if (gp.axes[2] > 0) { right = gp.axes[2]; left = 0; }
      sendData(up, down, left, right)
    }

    $(window).on("gamepadconnected", function () {
      $(".gamepad").css("color", "green");
      repGP = setInterval(reportOnGamepad, 200);
    });

    $(window).on("gamepaddisconnected", function () {
      $(".gamepad").css("color", "red");
      clearInterval(repGP);
      up = 0; down = 0; left = 0; right = 0;
      sendData(up, down, left, right)
    });
  }
  function setupNipples() {
    var up = 0;
    var down = 0;
    var left = 0;
    var right = 0;
    var beforeNipple = [up, down, left, right];
    var newNipple = [up, down, left, right];

    var joystickLeft = nipplejs.create({
      zone: document.getElementById('left'),
      color: 'green',
      restOpacity: 200,
      position: { bottom: '18%', left: '12%' },
      mode: 'static'

    });
    var joystickRight = nipplejs.create({
      zone: document.getElementById('right'),
      color: 'red',
      restOpacity: 200,
      position: { bottom: '18%', right: '12%' },
      mode: 'static'});
    
    joystickLeft.on('end move', function (event, data) {
      if (event.type === 'move') {
        if ((data.direction.y == 'up') && (data.direction.angle == 'up')) {
          up = data.distance/66.67;
          down = 0;
        }
        if ((data.direction.y == 'down') && (data.direction.angle == 'down')) {
          up = 0;
          down = data.distance/66.67;
        }
        if ((data.direction.angle == 'right') || (data.direction.angle == 'left')) {
          up = 0;
          down = 0;
        }

      }
      if (event.type === 'end') {
        up = 0;
        down = 0;
      }
      
    });
    
    joystickRight.on('end move', function (event, data) {
      if (event.type === 'move') {
        if ((data.direction.x == 'left') && (data.direction.angle == 'left')) {
          left = data.distance/66.67;
          right = 0;
        }
        if ((data.direction.x == 'right') && (data.direction.angle == 'right')) {
          left = 0;
          right = data.distance/66.67;
        }
        if ((data.direction.angle == 'up') || (data.direction.angle == 'down')) {
          left = 0;
          right = 0;
        }

      }
      if (event.type === 'end') {
        left = 0;
        right = 0;
      }
     
    });
      

    interval_nipple = setInterval(function () {
      sendData(up, down, left, right);
    }, 300);


    function sendData(up, down, left, right) {
      afking = 0;
      //console.log(up, down, left, right);
      $.post("/WebpageKeys", {
        ChosenProBot: JSON.stringify(ChosenProBot),
        up: JSON.stringify(up),
        down: JSON.stringify(down),
        left: JSON.stringify(left),
        right: JSON.stringify(right)
  
  });
    }  

    
    
    }
  function handleVisibilityChange() {
    if (document[hidden]) { $("#redirectModal").modal("show"); }
  }
  function sendData(up, down, left, right) {
    afking = 0;
    //console.log(up, down, left, right);
    $.post("/WebpageKeys", {
      ChosenProBot: JSON.stringify(ChosenProBot),
      up: JSON.stringify(up),
      down: JSON.stringify(down),
      left: JSON.stringify(left),
      right: JSON.stringify(right)

});
  }
  function endServerConnection() {
    interval = "";
    clearInterval(interval);
    document.onkeydown = null;
    document.onkeyup = null;

    clearInterval(repGP);

    clearInterval(imUsingIt);
    clearTimeout(connectionDelay);
    clearInterval(serverConnection);
    clearInterval(interval_nipple);
  }
}

// dev
function admin() {
  var probots; var newProbots; var temp;
  

  // table hover
  $("tr").hover(function () {
    if ($(this).find(".signal").hasClass("def")) { $(this).find(".signal").css("color", "#FFFFFF"); }
    if ($(this).find(".battery-icon").hasClass("def")) { $(this).find(".battery-icon").css("color", "#FFFFFF"); }
  }, function () {
    if ($(this).find(".signal").hasClass("def")) { $(this).find(".signal").css("color", ""); }
    if ($(this).find(".battery-icon").hasClass("def")) { $(this).find(".battery-icon").css("color", ""); }
  });
var probots = [];

  // probots query
  setInterval(function probots_query() {
    $.getJSON("/ProBotTelemetryAdmin",
      function (data) {
        if (probots.length == 0) {
          probots = data.listOfFiles;
          probots.forEach(robot => { addProBot(robot) });
        } else {
          newProbots = data.listOfFiles;
          updateProbots()
        }
      });
    }, 1000);

  // admin functions
  function addProBot(robot) {
    robot = robot.toString().split(",");

    if (isNaN(robot[1]) || robot[1] == 'Offline') {
      // ProBot Offline
      if(window.innerHeight > window.innerWidth){
      column1 = "<span class='fa-stack '><i class='fas fa-power-off fa-1x offline'></i></span><span class='fa-stack battery power-state'>Offline</span>";
      $(".tprobots tr:last").after('<tr> \
      <td class="text-center">'+ robot[0] + '</td> \
        <td class="text-center">'+ column1 + '</td></tr>');
      } else {
      column1 = "<span class='fa-stack '><i class='fas fa-power-off fa-1x offline'></i></span><span class='fa-stack battery power-state'>Offline</span>";  
      column2 = "<span></span>";
      column3 = "<span></span>";
      column4 = "<span></span>";
      
      $(".tprobots tr:last").after('<tr> \
      <td class="text-center">'+ robot[0] + '</td> \
        <td class="text-center">'+ column1 + '</td><td class="text-center">'+ column2 + '</td><td class="text-center">'+ column3 + '</td><td class="text-center">'+ column4 + '</td></tr>');
    }
    } else {
      // ProBot Online
      column1 = "<span class='fa-stack text-right'><i class='fas fa-power-off fa-1x online'></i></span>";
      column2 = "<span></span>";
      column3 = "<span></span>";
      column4 = "<span></span>";
      if (robot[6] == 'Available') {
        // ProBot Available  
        column1 += "<span class='fa-stack text-right'><i class='fa fa-check-circle fa-1x online'></i></span>"
        column2 += "<span></span>";
        column3 += "<span></span>";
        column4 += "<span></span>";
      } else if (robot[6] == "NotAvailable") {
        // ProBot NotAvailable
        column1 += "<span class='fa-stack text-right'><i class='fa fa-check-circle fa-1x offline'></i></span>"
        column2 += "<span></span>";
        column3 += "<span></span>";
        column4 += "<span></span>";
      }

    // battery
    if (robot[1] > 75) { var battery = "full"; }
    else if (robot[1] > 25 && robot[1] <= 75) { var battery = "half"; }
    else { var battery = "quarter"; }

    // Latency
    if (robot[4] < 200) { var lantency = "5"; }
    else if (robot[4] < 300) { var lantency = "4"; }
    else if (robot[4] < 500) { var lantency = "3"; }
    else if (robot[4] < 1000) { var lantency = "2"; }
    else { var lantency = "1"; }

    
    var onClick = "$(this).closest('form').submit()"
    column1 += '<span class="fa-stack text-right"><i class="fa fa-signal me" aria-hidden="true"></i><div class="signal signal-' + lantency + '"><i class="fa fa-signal" aria-hidden="true"></i></div></span>\
    <span class="fa-stack small text-right battery">'+ robot[1] + '%</span>\
    <span class="fa-stack text-center"><i class="fa fa-battery-'+ battery + ' fa-lg battery-icon"></i></span>'
    column2 += '<span title="User IP Adress, Country and City">'+ robot[7] + '</span>'
    column3 += '<span title="ProBot IP Adress">'+  robot[5] + '</span>'
    column4 += '<form method="post" action="/admin"><input type="hidden" name="ProBotToShutdown" value=' + robot[0] + '><span onclick="' + onClick + '" class="fa-stack bigger text-center icon-btn "><i class="fa fa-power-off fa-1x" data-toggle="tooltip" title="Power Off"></i></span></form>'



    $(".tprobots tr:last").after('<tr> \
    <td class="text-center">'+ robot[0] + '</td> \
      <td class="text-center">'+ column1 + '</td><td class="text-center">'+ column2 + '</td><td class="text-center">'+ column3 + '</td><td class="text-center">'+ column4 + '</td></tr>');


  }



  }

function updateProbots() {
  newProbots.forEach(function (newData, i) {

    var robot = newData.split(",");
 
        if (isNaN(robot[1]) || robot[1] == 'Offline') {
          // ProBot Offline
          if(window.innerHeight > window.innerWidth){
          column1 = "<span class='fa-stack '><i class='fas fa-power-off fa-1x offline'></i></span><span class='fa-stack battery power-state'>Offline</span>";
          $(".tprobots").children().eq(i+1).replaceWith('<tr><td class="text-center">'+ robot[0] + '</td> \
          <td class="text-center">'+ column1 + '</td></tr>');
          } else {  
            column1 = "<span class='fa-stack '><i class='fas fa-power-off fa-1x offline'></i></span><span class='fa-stack battery power-state'>Offline</span>";
            column2 = "<span></span>";
            column3 = "<span></span>";
            column4 = "<span></span>";
            $(".tprobots").children().eq(i+1).replaceWith('<tr><td class="text-center">'+ robot[0] + '</td> \
        <td class="text-center">'+ column1 + '</td><td class="text-center">'+ column2 + '</td><td class="text-center">'+ column3 + '</td><td class="text-center">'+ column4 + '</td></tr>');
          } 
        } else {
          // ProBot Online
          column1 = "<span class='fa-stack text-right'><i class='fas fa-power-off fa-1x online'></i></span>";
          column2 = "<span></span>";
          column3 = "<span></span>";
          column4 = "<span></span>";
          
          if (robot[6] == 'Available') {
            // ProBot Available  
            column1 += "<span class='fa-stack text-right'><i class='fa fa-check-circle fa-1x online'></i></span>"
            column2 += "<span></span>";
            column3 += "<span></span>";
            column4 += "<span></span>";
          } else if (robot[6] == "NotAvailable") {
            // ProBot NotAvailable
            column1 += "<span class='fa-stack text-right'><i class='fa fa-check-circle fa-1x offline'></i></span>"
            column2 += "<span></span>";
            column3 += "<span></span>";
            column4 += "<span></span>";
          }

        // battery
        if (robot[1] > 75) { var battery = "full"; }
        else if (robot[1] > 25 && robot[1] <= 75) { var battery = "half"; }
        else { var battery = "quarter"; }
  
        // Latency
        if (robot[4] < 200) { var lantency = "5"; }
        else if (robot[4] < 300) { var lantency = "4"; }
        else if (robot[4] < 500) { var lantency = "3"; }
        else if (robot[4] < 1000) { var lantency = "2"; }
        else { var lantency = "1"; }
  

        var onClick = "$(this).closest('form').submit()"
        column1 += '<span class="fa-stack text-right"><i class="fa fa-signal me" aria-hidden="true"></i><div class="signal signal-' + lantency + '"><i class="fa fa-signal" aria-hidden="true"></i></div></span>\
        <span class="fa-stack small text-right battery">'+ robot[1] + '%</span>\
        <span class="fa-stack text-center"><i class="fa fa-battery-'+ battery + ' fa-lg battery-icon"></i></span>'
        column2 += '<span title="User IP Adress, Country and City">'+ robot[7] + '</span>'
        column3 += '<span title="ProBot IP Adress">'+  robot[5] + '</span>'
        column4 += '<form method="post" action="/admin"><input type="hidden" name="ProBotToShutdown" value=' + robot[0] + '><span onclick="' + onClick + '" class="fa-stack bigger text-center icon-btn "><i class="fa fa-power-off fa-1x" data-toggle="tooltip" title="Power Off"></i></span></form>'
      
        
        $(".tprobots").children().eq(i+1).replaceWith('<tr><td class="text-center">'+ robot[0] + '</td> \
        <td class="text-center">'+ column1 + '</td><td class="text-center">'+ column2 + '</td><td class="text-center">'+ column3 + '</td><td class="text-center">'+ column4 + '</td></tr>');
  
      }

        
  });
}



}

// global functions
function openModal(modalId) {
  $('#' + modalId).modal('show');
}
function updateValues() {
  $(".loading").hide();
  $(".probot-status").show();
  $("p.probots").text("Working Probots: " + total);
  $("p.online").text("Online: " + online);
  $("p.available").text("Available: " + available);
}
function checkProBot(robot) {
  var temp = [];

  if (robot[1] != "NotWorking") { total += 1; }
  if ((robot[1] == "Offline") || (robot[1] == "NotWorking")) {
    temp.push("cover");
    temp.push("");
    temp.push("#ff0000");
    temp.push("times");
    temp.push("#ff0000");
  } else {
    // ONLINE
    online += 1;
    if (robot[1] == "Available") {
      available += 1;
      temp.push("");
      temp.push("available");
      temp.push("#82c91e");
      temp.push("check");
      temp.push("#82c91e");
    } if (robot[1] == "NotAvailable") {
      temp.push("cover");
      temp.push("");
      temp.push("#82c91e");
      temp.push("times");
      temp.push("#ff0000");
    }
  }

  return temp;
}