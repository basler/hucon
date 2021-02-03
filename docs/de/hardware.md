# Hardware

## Spannungsversorgung

![HuCon Power](images/hardware/power.png){: align=right style="height:320px"}

<p style="min-height: 320px">
Damit dein Roboter seine Arbeit verrichten kann, benötigt er Strom. Diesen bekommt er über ein USB-Kabel von deinem PC oder einem Handyladegerät. Es eignen sich auch einige USB-Powerbanks, damit er sich noch weiter von einer Steckdose oder dem PC entfernen kann.
</p>

!!! attention "Achtung"
    Bei einigen Notebooks kann es leider manchmal Probleme geben, sobald Servos angeschlossen sind. Diese benötigen, wenn sie am Anschlag sind, so viel Strom, dass dein Roboter nicht mehr ausreichend mit Strom versorgt werden kann. In diesem Fall musst du den Servo von deinem Roboter trennen und diesen neu starten. Dabei kann dann auch eventuell dein ganzes Programm verloren gehen!

## Reset-Taster

![HuCon Reset](images/hardware/reset.png){: align=right style="height:320px"}

<p style="min-height: 320px">
An der Seite deines Roboters befindet sich ein Taster. Diesen kannst du nicht programmieren. Es ist ein Reset-Taster. Damit kannst du deinen Roboter neu starten lassen, wenn er einmal überhaupt nicht mehr reagieren sollte. Da er aber seit seinem ersten Blinken immer reagiert hat, gehen wir davon aus, dass du diesen niemals benötigen wirst.
</p>

## LED

![HuCon LED](images/hardware/led.png){: align=right style="height:320px"}

<p style="min-height: 320px">
Der Kopf deines Roboters hat vier LEDs, die du alle programmieren kannst. In den Beispielen haben wir diese immer als Augen betrachtet, aber das kannst du natürlich anders definieren.
</p>

## Servo/ Motoren

![HuCon Servo](images/hardware/servo.png){: align=right style="height:320px"}

An deinem Roboter kannst du bis zu acht Servos/ Motoren anschließen. Beim Anschließen der Servos/ Motoren musst du darauf achten, dass diese auch richtig verbunden sind damit der Strom in die richtige Richtung fließen kann. Auf der Unterseite der Platine sind kleine Symbole, die kennzeichnen, wie ein Servo/ Motor richtig anzuschließen ist.

!!! info
    Die Standardbelegung für einen Servo ist wie folgt:

    ![HuCon Power](images/hardware/servo_connector_de.png){: style="width:340px"}

![HuCon Power](images/hardware/i2c.png){: align=right style="height:320px"}

Dein HuCon verfügt zusätzlich über einen I²C Anschluss. Damit kannst du weitere Module, wie unter anderem ein Gyroskop, anschließen.
