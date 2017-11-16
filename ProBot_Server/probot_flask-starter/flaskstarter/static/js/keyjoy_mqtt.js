///////
var this_js_script = $('script[src*=keyjoy_mqtt]');
var probot_id = this_js_script.attr('probot_id');
window.probot_ID = probot_id;

var up = 0;
var down = 0;
var left = 0;
var right = 0;
var keys = [];
var keysMsg;
var INC = 0.080;
var MAX = 0.750;
var repGP;
var enableOneDevice=0;

function keyboardHandler() {
	enableOneDevice=1;
	window.clearInterval(repGP);
	
	
    function incDirValue(dir) {
        dir = dir + INC;
        if (dir >= MAX) {
            dir = MAX;
        }
        return dir;
    }

    document.onkeydown = checkKeyDown;
    
    $("UserDevice").text("To use your keyboard, connect it and press any key!")

    function checkKeyDown(e) {
    	$("UserDevice").text("Keyboard detected!")
        e = e || window.event;

        keys[e.keyCode] = true;

        if (keys[38] && keys[37]) //forward and left
        {
            up = incDirValue(up);
            left = incDirValue(left);
        }
        if (keys[38] && keys[39]) //forward and right
        {
            up = incDirValue(up);
            right = incDirValue(right);
        }
        if (keys[40] && keys[37]) //back and left
        {
            down = incDirValue(down);
            left = incDirValue(left);
        }
        if (keys[40] && keys[39]) //back and right
        {
            down = incDirValue(down);
            right = incDirValue(right);
        }
        if (e.keyCode == 38) //forward
        {
            up = incDirValue(up);
        }
        if (e.keyCode == 40) //back
        {
            down = incDirValue(down);
        }
        if (e.keyCode == 37) //left
        {
            left = incDirValue(left);
        }
        if (e.keyCode == 39) //right
        {
            right = incDirValue(right);
        }

        if (up != 0 || down != 0 || left != 0 || right != 0) {
            window.time = new Date().getTime();
        }

			window.keyUp = up.toFixed(3);
			window.keyDown = down.toFixed(3);
			window.keyLeft = left.toFixed(3);
			window.keyRight = right.toFixed(3);
    }

    document.onkeyup = checkKeyUp

    function checkKeyUp(e) {
        e = e || window.event;

        keys[e.keyCode] = false;

        if (!keys[38]) //forward
        {
            up = 0;
        }
        if (!keys[40]) //back
        {
            down = 0;
        }
        if (!keys[37]) //left
        {
            left = 0;
        }
        if (!keys[39]) //right
        {
            right = 0;
        }

			window.keyUp = up.toFixed(3);
			window.keyDown = down.toFixed(3);
			window.keyLeft = left.toFixed(3);
			window.keyRight = right.toFixed(3);
    }

   
}

////

function gamepadHandler() {
	enableOneDevice=2;
	document.onkeydown = null;
	document.onkeyup = null;

    var hasGP = false;
    var repGP;

    function reportOnGamepad() {
        var gp = navigator.getGamepads()[0];
		if (enableOneDevice==2) {
        for (var i = 0; i < gp.axes.length; i += 2) {


            if (gp.axes[1] == 0) {
                up = 0;
                down = 0;
            }
            if (gp.axes[1] < 0) //forward
            {
                up = gp.axes[1] * -MAX;
                down = 0;
            }
            if (gp.axes[1] > 0) //back
            {
                down = gp.axes[1] * MAX;
                up = 0;
            }

            if (gp.axes[2] == 0) {
                left = 0;
                right = 0;
            }
            if (gp.axes[2] < 0) //left
            {
                left = gp.axes[2] * -MAX;
                right = 0;
            }
            if (gp.axes[2] > 0) //right
            {
                right = gp.axes[2] * MAX;
                left = 0;
            }

            if (up != 0 || down != 0 || left != 0 || right != 0) {
                window.time = new Date().getTime();
            }
			
			window.keyUp = up.toFixed(3);
			window.keyDown = down.toFixed(3);
			window.keyLeft = left.toFixed(3);
			window.keyRight = right.toFixed(3);
        }

        
    }}
			
            $("UserDevice").text("To use your gamepad, connect it and press any key!");

            $(window).on("gamepadconnected", function() {
            	if (enableOneDevice==2){
                hasGP = true;
                $("UserDevice").text("Gamepad connected!");
                console.log("Gamepad connected!");
                repGP = window.setInterval(reportOnGamepad, 200);}

            });

            $(window).on("gamepaddisconnected", function() {
				if (enableOneDevice==2){
                console.log("Gamepad disconnected!");
                $("UserDevice").text("Gamepad disconnected!");
                window.clearInterval(repGP);}

            });

            //setup an interval for Chrome
            var checkGP = window.setInterval(function() {
                if (navigator.getGamepads()[0]) {
                    if (!hasGP) $(window).trigger("gamepadconnected");
                    window.clearInterval(checkGP);
                }
            }, 500);
      
}

