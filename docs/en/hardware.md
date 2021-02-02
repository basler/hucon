# Hardware

## Power supply

![HuCon Power](images/hardware/power.png){: align=right style="height:320px"}

<p style="min-height: 320px">
In order for your robot to do his job, he needs power. He gets this power via a USB cable from your PC or a cell phone charger. Some USB PowerBanks are also usable, so that he can go even further away from a power charger or the PC.
</p>

!!! attention "Attention"
    With some notebooks, unfortunately, there can sometimes be problems once servos are connected. Under full load the servos might need so much current that your robot can no longer be supplied sufficiently with power. In this case you have to disconnect the servo from your robot and restart it. In this case you may lose your whole program!

## Reset button

![HuCon Reset](images/hardware/reset.png){: align=right style="height:320px"}

<p style="min-height: 320px">
On the side of your robot there is a button. You cannot program this button. It is a reset button. With it, you can restart your robot if it does not react at all. But since it has always reacted since its first blinking, we assume that you will never need it.
</p>

## LED

![HuCon LED](images/hardware/led.png){: align=right style="height:320px"}

<p style="min-height: 320px">
The head of your robot has four LEDs, all of which you can program. In the examples, we've always considered these to be eyes, but you can define that differently, of course.
</p>

## Servo/ motors

![HuCon Servo](images/hardware/servo.png){: align=right style="height:320px"}

You can connect up to eight servos/motors to your robot. When connecting the servos/motors you have to make sure that they are connected correctly so that the current can flow in the right direction. There are small symbols on the bottom of the board that indicate how to properly connect a servo/motor.

!!! info
    The standard assignment for a servo is as follows:

    ![HuCon Power](images/hardware/servo_connector_en.png){: style="width:340px"}

![HuCon Power](images/hardware/i2c.png){: align=right style="height:320px"}

Your HuCon also has an I²C port. This allows you to connect additional modules, such as a gyroscope.
