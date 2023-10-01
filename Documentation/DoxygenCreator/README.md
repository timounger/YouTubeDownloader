\page doxygen_creator Doxygen

\tableofcontents

# DoxygenCreator

## Über ℹ️

Der DoxygenCreator erzeugt ein Doxyfile mit eigenem Styling und führt es aus.
Der Bericht wird geöffnet und auch vorhandene Warnungen werden angezeigt.

## Voraussetzungen ⚠️

[Doxygen 1.9.8](https://sourceforge.net/projects/doxygen/files/rel-1.9.8/doxygen-1.9.8.windows.x64.bin.zip/download) wird zur Installation empfohlen.

Der Doxygen bin-Pfad muss in den Systemumgebungsvariablen der Variable `Path` hinzugefügt werden.

## Verwendung 👆️

Die Datei `doxygen_creator.py` ausführen um den Doxygen Bericht zu erstellen.
Dort können auch Änderungen vorgenommen werden.

## Styling 👀

### Awesome Design

Zusätzliche Stylesheets `(.css)` und Skripte `(.js)` sorgen für ein besonderes Aussehen und bieten zusätzliche Funktionen.

Die Designvorlagen [Doxygen Awesome v2.2.1](https://github.com/jothepro/doxygen-awesome-css/releases/tag/v2.2.1) werden verwendet.

Dazu werden folgende Doxygen-Einstellungen vorgenommen:

``` doxygen
HTML_COLORSTYLE = LIGHT # required with Doxygen >= 1.9.5
GENERATE_TREEVIEW = YES
DISABLE_INDEX = NO
FULL_SIDEBAR = NO
HTML_HEADER = header.html
HTML_EXTRA_STYLESHEET = doxygen-awesome.css
HTML_EXTRA_FILES = doxygen-awesome-darkmode-toggle.js \
	doxygen-awesome-fragment-copy-button.js \
	doxygen-awesome-paragraph-link.js \
	doxygen-awesome-interactive-toc.js \
	doxygen-awesome-tabs.js
```

Folgende Zusatzfunktionen sind enthalten:

* Darkmode-Toggle: Wechsel in den Darkmode möglich
* Code kopieren Button: Code-Inhalte können kopiert werden
* Paragraph Link: Alle Überschriften enthalten einen Link zum entsprechenden Absatz
* Interactive-TOC: Inhaltsverzeichnis wird bei schmaler Bildschirmbreite über den Inhalt geklappt

### GitHub Corners

Die generierte Doxygen Seite enthält einen Link ([GitHub Corner](https://tholman.com/github-corners/)) zum GitHub Repository.

### PlantUml

PlantUml Diagramme werden unterstützt.
Dazu wird, falls nicht vorhanden, die Datei `plantuml.jar` heruntergeladen.

### Emoji 😀

Es sollten nur Emojis in `UNICODE`-Schreibweise verwendet werden, damit sie von Doxygen korrekt angezeigt werden.

``` markdown
# Beispiel für 🤣
&#x1F923;
```

Aus dieser [Liste aller Emojis](https://getemoji.com/) kann ein passendes Emoji ausgewählt werden.
Alternativ kann das passende Emoji auch mit dem [EMOJI TRANSLATER](https://emojitranslate.com/) gefunden werden.

Einfacher ist es, das Emoji per Copy & Paste einzufügen.
