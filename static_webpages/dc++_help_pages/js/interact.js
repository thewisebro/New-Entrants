/*global $*/

var active = 1; //store current active tab

function hideHelp(i) {
	"use strict";

	switch (i) {
	case 1:
		$("#windows-help").fadeOut(100);
		$("#windows").removeClass("active");
		break;
	case 2:
		$("#linux-help").fadeOut(100);
		$("#linux").removeClass("active");
		break;
	}
}

function showHelp(i) {
	"use strict";

	if (i !== active) {
		hideHelp(active);
		switch (i) {
		case 1:
			$("#windows-help").delay(100).fadeIn(200);
			$("#windows").addClass("active");
			active = 1;
			break;
		case 2:
			$("#linux-help").delay(100).fadeIn(200);
			$("#linux").addClass("active");
			active = 2;
			break;
		}
	}
}
