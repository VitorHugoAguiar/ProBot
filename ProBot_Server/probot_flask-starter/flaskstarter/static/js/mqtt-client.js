//global variables
window.keyUp = 0;
window.keyDown = 0;
window.keyLeft = 0;
window.keyRight = 0;
window.MainRoutine = [];
window.availability = [];

//local variables
var battery = [];
var angle = [];
var mainRoutineStatus = [];
var probotID = 0;
var battery_timeout = [];
var OnlineProbots = [];
var numberProbots = 6;
var busyProbots = [];
var disableLabels=0;
var sendKeysTimer=0;

var this_js_script = $('script[src*=mqtt-client]');
var enable = this_js_script.attr('enable');
var mobile = this_js_script.attr('mobile');
var $SCRIPT_ROOT = this_js_script.attr('$SCRIPT_ROOT');

function drawChart() {

    var data = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Degrees', AngleChart]
    ]);
    var options = {
        redFrom: 70,
        redTo: 110,
        redColor: '#00FF00',
        greenFrom: 0,
        greenTo: 180,
        greenColor: '#FF0000',
        minorTicks: 20,
        max: 180,
        min: 0,
        majorTicks: ['0', '180']
    };

    var chart = new google.visualization.Gauge(document.getElementById('chart_div' + window.probot_ID));
    chart.draw(data, options);

}

chooseControl = function(control_id) {
	console.log("control_chosen ", control_id)
    if (control_id == "keyboard") {
        document.getElementById("keyboard").src = "../static/images/keyboard_disable.png";
        document.getElementById("gamepad").src = "../static/images/gamepad_set.png";
        keyboardHandler();
		clearTimeout(sendKeysTimer);   
        SendKeys();

    }
    if (control_id == "gamepad") {
        document.getElementById("gamepad").src = "../static/images/gamepad_disable.png";
        document.getElementById("keyboard").src = "../static/images/keyboard_set.png";
        gamepadHandler();
        clearTimeout(sendKeysTimer);
        SendKeys();
    }
    if (control_id == "nipple") {
        SendKeys();
    }

}

function SendKeys() {
    $.post("/WebpageKeys", {
        probot_ID: JSON.parse(window.probot_ID),
        keyUp: JSON.parse(window.keyUp),
        keyDown: JSON.parse(window.keyDown),
        keyLeft: JSON.parse(window.keyLeft),
        keyRight: JSON.parse(window.keyRight)

    });

    sendKeysTimer=setTimeout(SendKeys, 100);
}

function SendMainRoutine(MainRoutineStatus, probot) {
    $.post("/MainRoutine", {
        probot_ID: JSON.parse(probot),
        MainRoutineStatus: String (MainRoutineStatus)

    });
}

function shutdownProBot(probot) {
	if (document.getElementById("online_offline" + probot).getAttribute('src') == "../static/images/online.png"){
	if (confirm("Do you really want to SHUTDOWN the ProBot" + probot +"?")==true){
    $.post("/shutdownProBot", {
        probot_ID: JSON.parse(probot),
        shutdownProBotStatus: String ("shutdown")

    });}
    else {
    	return false
    }} else {                    
    	alert("The ProBot" + probot + " is offline.");
        return false;
    	
    }
}

function noLogin() {
	    if (enable == 1) {
            alert("To start a ProBot, you need to login as an admin!");
        }
        if (enable == 2) {
            alert("To control a ProBot, you need to login first!");
        }
}

function LoginStart() {
	window.onload = function(){
	ifvisible.focus(); // Will trigger wakeup event as well
	ifvisible.wakeup();

	}

	ifvisible.setIdleDuration(3600);
	ifvisible.on('statusChanged', function(e){


	if (e.status == "idle"){
		document.getElementById('link').click();
		}

	});

}

function checkform(value) {
        if (enable == 1) {
            if (window.mainRoutineStatus[value] == "stopped") {
                if (confirm("Do you really want to START the main routine?") == true) {
                    SendMainRoutine("start", value);
                } else {
                    return false;
                }

            } else {
                if (window.mainRoutineStatus[value] == "started") {
                    if (confirm("Do you really want to STOP the main routine?") == true) {
                        SendMainRoutine("stop", value);
                    } else {
                        return false;
                    }

                } else {
                    alert("The ProBot" + value + " is offline or ProBot.py is not executing. Please choose another one");
                    return false;
                }
            }
        }

        if (enable == 2) {
            if (document.getElementById("available" + value).getAttribute('src') == "../static/images/available.png") {
                if (confirm("Are you sure?") == true) {
                    document.formName.submit();
                    document.formName.reset();
                } else {
                    return false;
                }

            } else {
                alert("The ProBot" + value + " is not available. Please choose another one");
                return false;
            }

        }

}

/////
function update_values() {
	
    $.getJSON($SCRIPT_ROOT + "/ServerToWebpage",
        function(data) {
            $("#busyProbots").text(data.busyProbots);
            busyProbots = data.busyProbots;
            $("#OnlineProbots").text(data.OnlineProbots);
            OnlineProbots = data.OnlineProbots;

            for (i = 1; i < OnlineProbots.length; i++) {
                if (OnlineProbots[i] != 0) {
                    probotID = OnlineProbots[i][0];
                    
                    if (OnlineProbots[probotID][1] != "OFF-LINE") {
                        battery[probotID] = OnlineProbots[i][1];
                        angle[probotID] = OnlineProbots[i][2];
                        mainRoutineStatus[probotID] = OnlineProbots[i][3];
                        battery_timeout[probotID] = new Date().getTime();
						
                        if (enable == 1) {
                            document.getElementById("online_offline" + probotID).src = "../static/images/online.png";

                            if (battery[probotID] < '20') {
                                window.availability[probotID] = false;
                            }
                            if (battery[probotID] >= '20' && battery[probotID] < '21') {
                                window.availability[probotID] = true;
                            }
                            if (battery[probotID] < '21' && battery[probotID] != 0) {
                                document.getElementById("battery" + probotID).src = "../static/images/low_battery.png";
                            }
                            if (battery[probotID] >= '21' && battery[probotID] < '22') {
                                window.availability[probotID] = true;
                                document.getElementById("battery" + probotID).src = "../static/images/half_battery.png";
                            }
                            if (battery[probotID] >= '22') {
                                window.availability[probotID] = true;
                                document.getElementById("battery" + probotID).src = "../static/images/full_battery.png";
                            }


                            if (mainRoutineStatus[probotID] == 'started') {
                                document.getElementById("executing" + probotID).src = "../static/images/executing.png";

                            }

                            if (mainRoutineStatus[probotID] == 'stopped' || mainRoutineStatus[probotID] == 'undefined' || mainRoutineStatus[probotID] == '0') {
                                document.getElementById("executing" + probotID).src = "../static/images/not_executing.png";

                            }


                        }

                        if (enable == 2) {
                            if (battery[probotID] < '20') {
                                window.availability[probotID] = false;
                            }
                            if (battery[probotID] >= '20') {
                                window.availability[probotID] = true;
                            }

                        }

                        if (enable == 1 || enable == 2) {
                            if (window.availability[probotID] === true && busyProbots[probotID] == 0 && mainRoutineStatus[probotID] == 'started') {
                                document.getElementById("available" + probotID).src = "../static/images/available.png";

                            }
                            if (window.availability[probotID] === false || busyProbots[probotID] == probotID || mainRoutineStatus[probotID] == 'stopped' || mainRoutineStatus[probotID] == 'undefined' || mainRoutineStatus[probotID] == '0') {
                                document.getElementById("available" + probotID).src = "../static/images/not_available.png";
                            }

                        }


                        if (enable == 3) {
                            if (probotID == window.probot_ID) {
								if (disableLabels==0){
                                document.getElementById('lost_connection' + probotID).style.display = "none";
                                document.getElementById('statusBBB' + probotID).style.color = "#000000";
                                $('#statusBBB' + probotID).html('Connected to the ProBot' + probotID + '!');

                                if (battery[probotID] < '21' && battery[probotID] != 0) {
                                    document.getElementById("battery" + probotID).src = "../static/images/low_battery.png";
                                }
                                if (battery[probotID] >= '21' && battery[probotID] < '22') {
                                    document.getElementById("battery" + probotID).src = "../static/images/half_battery.png";
                                }
                                if (battery[probotID] >= '22') {
                                    document.getElementById("battery" + probotID).src = "../static/images/full_battery.png";
                                }


                            if (mainRoutineStatus[probotID] == 'stopped' || mainRoutineStatus[probotID] == 'undefined' || mainRoutineStatus[probotID] == '0') {
                            	document.getElementById('mainRoutineLabel' + probotID).style.color = "#ff0000"
                                document.getElementById('mainRoutineLabel' + probotID).style.display = "block";
    							setTimeout(function() {
                					window.location = window.location;

    							}, 10000);
                            }

                            if (mainRoutineStatus[probotID] == 'started' ) {
                            	document.getElementById('mainRoutineLabel' + probotID).style.color = "#000000";
                                document.getElementById('mainRoutineLabel' + probotID).style.display = "none";
                            }

                                AngleChart = parseFloat(angle[probotID]) + 90;
                                drawChart();
                                google.setOnLoadCallback(drawChart);
                            }
                        }}

                    }
                    if (OnlineProbots[probotID][1] == "OFF-LINE") {
                        battery[probotID] = 0;
                        window.availability[probotID] = false;
                        if (enable == 1) {
                            document.getElementById("available" + probotID).src = "../static/images/not_available.png";
                            document.getElementById("online_offline" + probotID).src = "../static/images/offline.png";
                            document.getElementById("battery" + probotID).src = "../static/images/not_connected.png";
                            document.getElementById("executing" + probotID).src = "../static/images/not_executing.png";
                        }

                        if (enable == 2) {
                            document.getElementById("available" + probotID).src = "../static/images/not_available.png";
                        }

                        if (enable == 3 && probotID == window.probot_ID) {
                            document.getElementById("battery" + probotID).src = "../static/images/not_connected.png";
                            document.getElementById('statusBBB' + probotID).style.color = "#ff0000";
                            $('#statusBBB' + probotID).html('Connection lost!');
                            document.getElementById('lost_connection' + probotID).style.display = "block";
                            AngleChart = NaN;
                            drawChart();
                            google.setOnLoadCallback(drawChart);
                            if (new Date().getTime() - battery_timeout[probotID] >= 10000) {
                                window.location = window.location;
                            }

                        }
                    }
                }
            }

        });
}

setInterval(update_values, 500)

