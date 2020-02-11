# Inbetriebnahme

Was wird benötigt:

- USB Kabel
- Terminal Programm ([MobaXterm](https://mobaxterm.mobatek.net/) (Windows) oder screen (MacOs & Linux))
- Micro SD-Karte
- Internetverbindung zum Herunterladen des HuCon 'image'

## Vorbereitung
Um die neue Software auf deinem HuCon zu installieren, musst du zunächst das letzte Release aus unserem gitHub-Repository herunterladen. Dieses findest du unter [https://github.com/basler/hucon/releases](https://github.com/basler/hucon/releases) im Abschnitt 'Assets'.
Speicher die beiden Dateien, onionIoT-[version]-hucon-[version].bin und update_flash.sh, auf deine SD-Karte.

## Installation
Baue deinen HuCon zusammen und stecke die SD-Karte in den von deinem Roboter vorgesehenen Steckplatz. Dieser befindet sich oben am Hals deines HuCon.
Dann kannst du deinen HuCon mit einem USB-Kabel an deinem Computer anschließen.

Öffne jetzt MobaXterm und klicke auf *Sessions*. Es öffnet sich das folgende Fenster, in dem du den Com-Port und die Geschwindigkeit einstellen musst.


![MobaXterm configuration](images/initial_setup/mobaxterm_configuration.png)

!!! warning
    Wenn du keinen *USB Serial Port* in deiner Liste hast, dann ist es notwendig, dass du den Treiber für den HuCon installierst. Der HuCon ist mit einem USB-Seriell-Wandler von [FTDI](https://www.ftdichip.com) ausgestattet.

    Den entsprechenden Treiber findest du [hier](https://www.ftdichip.com/Drivers/VCP.htm).


Sobald du auf OK klickst, erscheint das folgende Bild:

![MobaXterm connected](images/initial_setup/mobaxterm_connected.png)

Das ist auch in Ordnung. Dein Roboter antwortet nur, wenn du ihm etwas sagst. Drücke *Enter* und dein Roboter sollte antworten. Dies wird ähnlich aussehen wie das hier:

![MobaXterm Ready](images/initial_setup/mobaxterm_ready.png)

Jetzt bist du auf der Kommandozeile deines Roboters. Das kennst du sicher aus anderen Spielen oder Filmen, denn jetzt hast du die volle Kontrolle über das System. :smile:

Um die Software deines HuCon zu aktualisieren, musst du die folgenden beiden Befehle in die Konsole von MobaXterm eingeben und ausführen:

```sh
mount /dev/mmcblk0p1 /mnt
sh /mnt/update_flash.sh
```

Nach dem zweiten Befehl gibt es eine Menge an Text der Konsole ausgegeben wird und dein HuCon wird während dieses Vorgangs einmal neu gestartet. Dieser Vorgang kann bis zu 5 Minuten dauern, bis dein HuCon wieder betriebsbereit ist.
Ob dein HuCon neu gestartet wurde, kannst du an den Augen deines HuCon erkennen. Sobald der HuCon startet, werden die Augen rot. Wenn der interne Server startet, werden die Augen orangefarben, und wenn alles bereit ist, werden die Augen für kurze Zeit grün, bevor sie wieder erlöschen.

!!! warning
    Bitte achte darauf, dass dein HuCon nicht von deinem vom Computer getrennt wird. Sonst könnte es sein, dass es danach kaputt ist.