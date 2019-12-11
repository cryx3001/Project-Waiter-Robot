// ALL CREDITS TO W.S Toh FOR THE ORIGINAL CODE FROM: https://code-boxx.com/pure-javascript-numeric-keypad/
var numpad = {
selector: null,
display: null,
zero: null,
target: null,


	init: function () {
		// CREATE THE NUMPAD
		numpad.selector = document.createElement("div");
		numpad.selector.id = "numpad-back";
		var wrap = document.createElement("div");
		wrap.id = "numpad-wrap";
		numpad.selector.appendChild(wrap);

		// ATTACH THE NUMBER DISPLAY
		numpad.display = document.createElement("input");
		numpad.display.id = "numpad-display";
		numpad.display.type = "text";
		numpad.display.readOnly = true;
		wrap.appendChild(numpad.display);

		// ATTACH BUTTONS
		var buttons = document.createElement("div"),
			button = null,
			append = function (txt, fn, css) {
				button = document.createElement("div");
				button.innerHTML = txt;
				button.classList.add("numpad-btn");
				if (css) {
					button.classList.add(css);
				}
				button.addEventListener("click", fn);
				buttons.appendChild(button);
			};
		buttons.id = "numpad-btns";
		// First row - 7 to 9, delete.
		for (var i = 7; i <= 9; i++) {
			append(i, numpad.digit);
		}
		append("&#10502;", numpad.delete, "ng");
		// Second row - 4 to 6, clear.
		for (var i = 4; i <= 6; i++) {
			append(i, numpad.digit);
		}
		append("C", numpad.reset, "ng");
		// Third row - 1 to 3, cancel.
		for (var i = 1; i <= 3; i++) {
			append(i, numpad.digit);
		}
		append("STOP", numpad.stop, "cx");

		append(0, numpad.digit, "zero");
		numpad.zero = button;

		append("&#10004;", numpad.select, "ok");
		// Add all buttons to wrapper
		wrap.appendChild(buttons);
		document.body.appendChild(numpad.selector);
	},


	show: function () {
		// Show numpad
		numpad.selector.classList.add("show");
	},

	delete: function () {
		// delete() : delete last digit on the number pad

		var length = numpad.display.value.length;
		if (length > 0) {
			numpad.display.value = numpad.display.value.substring(0, length - 1);
		}
	},

	reset: function () {
		// reset() : reset the number pad

		numpad.display.value = "";
	},

	stop: function () {
		const xhr = new XMLHttpRequest();
		const data = new FormData();

		data.append('input', "-2");
		xhr.open('POST', '/api');
		xhr.send(data);

		numpad.reset()

	},

	digit: function (evt) {
		// digit() : append a digit

		var current = numpad.display.value,
			append = evt.target.innerHTML;

		if (current.length < 2) {
			if (current == "0") {
				numpad.display.value = append;
			} else {
				numpad.display.value += append;
			}
		}
	},

	select: function () {
		const xhr = new XMLHttpRequest();
		const data = new FormData();

		value = numpad.display.value;

		// No decimals allowed - strip decimal
		if (!numpad.dec && value % 1 != 0) {
			value = parseInt(value);
		}
		console.log(value);

		data.append('input', value);
		xhr.open('POST', '/api');
		xhr.send(data);

		numpad.reset();
	}};

window.addEventListener("load", numpad.init);