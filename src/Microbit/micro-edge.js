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
radio.setTransmitPower(7)
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
