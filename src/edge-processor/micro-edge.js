radio.onReceivedString(function (receivedString) {
    if (receivedString.charAt(0) == ">") {
        serial.writeLine(receivedString)
        basic.showLeds(`
        . # . # .
        # . . . #
        . . # . .
        . # . # .
        # . . . #
        `)
		basic.showLeds(`
        # . . . #
        . . # . .
        . # . # .
		# . . . #
        . . # . .
        `)
        basic.showLeds(`
        . . # . .
        . # . # .
        # . . . #
        . . # . .
        . # . # .
        `)
        basic.showLeds(`
        . # . # .
        # . . . #
        . . # . .
        . # . # .
        # . . . #
        `)
		basic.showLeds(`
        # . . . #
        . . # . .
        . # . # .
		# . . . #
        . . # . .
        `)
    }
})
radio.setGroup(1)
basic.forever(function () {
    basic.showLeds(`
        . . # . .
        . # . # .
        # . . . #
        . . # . .
        . # . # .
        `)
})
