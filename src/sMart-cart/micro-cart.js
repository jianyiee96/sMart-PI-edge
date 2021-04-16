let inCartIndex = 0
let cartItems: string[] = []
serial.redirect(
SerialPin.P0,
SerialPin.P1,
BaudRate.BaudRate9600
)
radio.setTransmitPower(7)
radio.setGroup(1)
basic.forever(function () {
    basic.showNumber(cartItems.length)
    let item = serial.readUntil("=")
    inCartIndex = -1
    if(item.length == 8) {
        for (let x = 0; x <= cartItems.length - 1; x++) {
            if (cartItems[x] == item) {
                inCartIndex = x
                break;
            }
        }
        if (inCartIndex == -1) {
            cartItems.push(item)
            radio.sendString(">" + control.deviceName() + "=A=" + item)
            basic.showLeds(`
                . . . . .
                . . # . .
                . # # # .
                . . # . .
                . . . . .
                `)
        } else {
            cartItems.removeAt(inCartIndex)
            radio.sendString(">" + control.deviceName() + "=R=" + item)
            basic.showLeds(`
                . . . . .
                . . . . .
                . # # # .
                . . . . .
                . . . . .
                `)
        }
    }
})
