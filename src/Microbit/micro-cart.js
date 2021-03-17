input.onButtonPressed(Button.A, function () {
    if (state == 0) {
        if (generalItems.length == 0) {
            basic.showIcon(IconNames.No)
        } else {
            state = 1
            generalIndex = 0
        }
    } else if (state == 1) {
        generalIndex = (generalIndex + 1) % generalItems.length
    } else if (state == 2) {
        cartIndex = (cartIndex + 1) % cartItems.length
    }
})
input.onButtonPressed(Button.AB, function () {
    if (state == 1) {
        state = 0
        radio.sendString(">" + control.deviceName() + "=ADD=" + generalItems[generalIndex])
        basic.showLeds(`
            . . . . .
            . . # . .
            . # # # .
            . . # . .
            . . . . .
            `)
        cartItems.push(generalItems[generalIndex])
        generalItems.removeAt(generalIndex)
    } else if (state == 2) {
        state = 0
        radio.sendString(">" + control.deviceName() + "=REMOVE=" + cartItems[cartIndex])
        basic.showLeds(`
            . . . . .
            . . . . .
            . # # # .
            . . . . .
            . . . . .
            `)
        generalItems.push(cartItems[cartIndex])
        cartItems.removeAt(cartIndex)
    }
})
input.onButtonPressed(Button.B, function () {
    if (state == 0) {
        if (cartItems.length == 0) {
            basic.showIcon(IconNames.No)
        } else {
            state = 2
            cartIndex = 0
        }
    } else if (state == 1) {
        generalIndex = (generalIndex + generalItems.length - 1) % generalItems.length
    } else if (state == 2) {
        cartIndex = (cartIndex + cartItems.length - 1) % cartItems.length
    }
})
input.onGesture(Gesture.Shake, function () {
	state = 0
})
let cartItems: string[] = []
let cartIndex = 0
let generalIndex = 0
let state = 0
let generalItems: string[] = []
radio.setTransmitPower(7)
radio.setGroup(1)
generalItems = ["A", "B", "C", "D", "E", "F"]
basic.forever(function () {
    if (state == 0) {
        basic.showIcon(IconNames.Happy)
    } else if (state == 1) {
        basic.showString("" + (generalItems[generalIndex]))
    } else if (state == 2) {
        basic.showString("" + (cartItems[cartIndex]))
    }
})