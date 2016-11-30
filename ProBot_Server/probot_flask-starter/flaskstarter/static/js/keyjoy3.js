var up = 0;
var down = 0;
var left = 0;
var right = 0;
var keys = [];
var keysMsg = [0,0,0,0];

var INC = 0.080;
var MAX = 0.750;

var this_js_script = $('script[src*=keyjoy]');

var probot_id = this_js_script.attr('probot_id');

function keyboardHandler(session, topic)
{	
	function incDirValue(dir)
	{
		dir = dir + INC;
		if(dir >= MAX)
		{
			dir = MAX;
		}
		return dir;
	}

	document.onkeydown = checkKeyDown;
	function checkKeyDown(e)
	{
		e = e || window.event;

		keys[e.keyCode] = true;

		if(keys[38] && keys[37])	//forward and left
		{
			up = incDirValue(up);
			left = incDirValue(left);	
		}
		if(keys[38] && keys[39])	//forward and right
		{
			up = incDirValue(up);
			right = incDirValue(right);	
		}
		if(keys[40] && keys[37])	//back and left
		{
			down = incDirValue(down);
			left = incDirValue(left);
		}
		if(keys[40] && keys[39])	//back and right
		{
			down = incDirValue(down);
			right = incDirValue(right);
		}
		if(e.keyCode == 38) //forward
		{
			up = incDirValue(up);
		}
		if(e.keyCode == 40) //back
		{
			down = incDirValue(down);
		}
		if(e.keyCode == 37) //left
		{
			left = incDirValue(left);
		}
		if(e.keyCode == 39) //right
		{
			right = incDirValue(right);
		}
		
			if(up!=0 || down!=0 || left!=0 || right!=0)
			{window.time = new Date().getTime();
			}
		
		keysMsg = [up.toFixed(3), down.toFixed(3) , left.toFixed(3), right.toFixed(3)];
		session.publish(topic, [keysMsg]);		
	}

	document.onkeyup = checkKeyUp       
	function checkKeyUp(e)
	{			
		e = e || window.event;

		keys[e.keyCode] = false;
		
		if(!keys[38])	//forward
		{
			up = 0;
		}			
		if(!keys[40])	//back
		{
			down = 0;
		}
		if(!keys[37])	//left
		{
			left = 0;
		}
		if(!keys[39])	//right
		{
			right = 0;
		}
		
		
		keysMsg = [up.toFixed(3), down.toFixed(3) , left.toFixed(3), right.toFixed(3)];
		session.publish(topic, [keysMsg]);		
	}		

	document.getElementById("joystick").disabled = true;	
}

function joystickHandler(session, topic)
{

	
	var hasGP = false;
	var repGP;

	function canGame() 
	{
		return "getGamepads" in navigator;
	}

	function reportOnGamepad() 
	{
		var gp = navigator.getGamepads()[0];
		var html = "";
		html += "id: "+gp.id+"<br/>";

		for(var i=0;i<gp.buttons.length;i++)
		{
			html+= "Button "+(i+1)+": ";
			if(gp.buttons[i].pressed) html+= " pressed";
			html+= "<br/>";
		}

		for(var i=0;i<gp.axes.length; i+=2)
		{
			html+= "Stick "+(Math.ceil(i/2)+1)+": "+gp.axes[i]+","+gp.axes[i+1]+"<br/>";
			
			if(gp.axes[1] == 0)
			{
				up = 0;
				down = 0;
			}
			if(gp.axes[1] < 0)	//forward
			{
				up = gp.axes[1] * -MAX;
				down = 0;
			}
			if(gp.axes[1] > 0)	//back
			{
				down = gp.axes[1] * MAX;
				up = 0;
			}				

			if(gp.axes[2] == 0)
			{
				left = 0;
				right = 0;
			}
			if(gp.axes[2] < 0)	//left
			{
				left = gp.axes[2] * -MAX;
				right = 0;
			}
			if(gp.axes[2] > 0)	//right
			{
				right = gp.axes[2] * MAX;
				left = 0;
			}
			
			if(up!=0 || down!=0 || left!=0 || right!=0)
			{window.time = new Date().getTime();
			}
			
			keysMsg = [up.toFixed(3), down.toFixed(3) , left.toFixed(3), right.toFixed(3)];
			session.publish(topic, [keysMsg]);				            
		}
		
		$("#gamepadDisplay").html(html);
	}

	$(document).ready(function() {
		if(canGame())
		{
			
			$("gamepadPrompt").text("To use your gamepad, connect it and press any key!");
			
			
			$(window).on("gamepadconnected", function() {
				hasGP = true;
				$("gamepadPrompt").text("Gamepad connected!");
				console.log("connection event");
				repGP = window.setInterval(reportOnGamepad,200);
				
			});

			$(window).on("gamepaddisconnected", function() {
				console.log("disconnection event");
				$("gamepadPrompt").text("Gamepad disconnected!");
				window.clearInterval(repGP);
				
			});

			//setup an interval for Chrome
			var checkGP = window.setInterval(function() {
				console.log('checkGP');
				if(navigator.getGamepads()[0])
				{
					if(!hasGP) $(window).trigger("gamepadconnected");
					window.clearInterval(checkGP);
				}
			}, 500);
		} 
	});
	document.getElementById("keyboard").disabled = true;	
}

// the URL of the WAMP Router (Crossbar.io)
var connection = new autobahn.Connection({
		url: "wss://89.109.64.175:8080/ws",
		realm: "realm1"
});

// timers

var t1, t2;
var battery=0;

var chooseControl;

// fired when connection is established and session attached

connection.onopen = function (session, details){
	
console.log("Connected");
	
session.publish("general-topic", [probot_id]);
console.log("Published Probot_id to general-topic, id: " + probot_id);
	
var probot_topic = "probot-topic-" + probot_id;
var keepalive_topic = "keepalive-" + probot_id;
var probot_bat = "probot-bat-" + probot_id;
	
window.setInterval(function (){
		session.publish(keepalive_topic, []);
		console.log("keepalive");
}, 1000); // MILISEGUNDOS
	
function receiveBattery(args)
{
	var dataReceived = args[0];
	if(dataReceived == "error")
	{
		console.log("Stopped receiving battery");
		if(!alert('Looks like the ProBot'+ probot_id+' it is not responding. Please click OK and choose another ProBot.'))
			{window.location = window.location.href.split("#")[0];}

	}
	else
	{
			console.log("battery voltage: " + dataReceived+"%");
			battery=dataReceived+"%";
			document.getElementById('battery').innerHTML = battery;
			if(dataReceived < 20)
		{
			document.getElementById("battery").style.color = "red"
		}
	}
}
	
session.subscribe(probot_bat, receiveBattery).then(
	function (sub)
	{
		console.log("subscribed to topic" + probot_bat);
	},
	function (err)
	{
		console.log('failed to subscribe to topic', err);
	}
);


// PUBLISH an event every second
t1 = setInterval(function (){
	
	keysMsg = [up.toFixed(3), down.toFixed(3) , left.toFixed(3), right.toFixed(3)];
	session.publish(probot_topic, [keysMsg]);

}, 100);
	
chooseControl = function (control_id)
{
	if(control_id == "keyboard")
	{
		keyboardHandler(session, probot_topic);
	}
	else if(control_id == "joystick")
	{
		joystickHandler(session, probot_topic);
	}
}
	
};


// fired when connection was lost (or could not be established)s
connection.onclose = function (reason, details){

	console.log("Connection lost: " + reason);

	if (t1)
	{
		clearInterval(t1);
		t1 = null;
	}
	if (t2)
	{
		clearInterval(t2);
		t2 = null;
	}
}

// now actually open the connection

connection.open();
