\page doxygen_creator Doxygen

\tableofcontents

# DoxygenCreator

## Über ℹ️

Der DoxygenCreator generiert und Doxyfile mit eigenem Styling und führt dieses aus. Der Bericht wird geöffnen und falls vorhanden auch die Warnungen angezeigt.

## Voraussetzungen ⚠️

[Doxygen 1.9.2](https://sourceforge.net/projects/doxygen/files/rel-1.9.2/doxygen-1.9.2-setup.exe/download) ist als Installation zu empfehlen.

Der Doxygen bin Path muss der `Path` Variable in den Systemumgebungsvariablen hinzugefügt werden.

## Verwendung 👆️

Die Datei `doxygen_creator.py` ausführen um den Doxygen Bericht zu erstellen. Dort können auch Änderungen vorgenommen werden.

## Styling 👀

### Awesome Design

Zusätzliche Stilvorlagen `(.css)` und Skripte `(.js)` sorgen für besonderes Aussehen und bieten zusätzliche Funktionen.

Diese [Designvorlagen](https://jothepro.github.io/doxygen-awesome-css/) kommen zum Einsatz.

Folgende Doxygen Einstellungen werden dafür vorgenommen:

``` doxygen
GENERATE_TREEVIEW = YES
DISABLE_INDEX = NO
FULL_SIDEBAR = NO
HTML_HEADER = header.html
HTML_EXTRA_STYLESHEET = doxygen-awesome.css
HTML_EXTRA_FILES = doxygen-awesome-darkmode-toggle.js \
	doxygen-awesome-fragment-copy-button.js \
	doxygen-awesome-paragraph-link.js \
	doxygen-awesome-interactive-toc.js
```

Folgende zusätzliche Funktionen sind enthalten:

* Darkmode toggle: Wechsel in den Darkmode möglich (!Firefox Bug: speichert die EInstellung nicht global)
* Code-Copy-Button: Code Inhalte können kopiert werden
* Paragraph Link: Alle Überschriften enthalten einen Link zu dessen Abschnitt
* Interactive-TOC: Inhaltsverzeichnis zusammengeklappt über dem Inhalt bei schmaler Bildschirmbreite

### GitHub Corners

Die generierte Doxygen Seite enthält einen Link ([GitHub Corner](https://tholman.com/github-corners/)) auf das GitHub Repository.

### PlantUml

PlantUml Diagramme werden unterstützt. Dafür wird das `plantuml.jar` heruntergeladen.

### Emoji 😀

Es sollten nur Emijis als `UNICODE` Schreibweise verwendet werden, damit diese von Doxygen korrekt dargestellt werden.

``` markdown
# Beispiel für 🤣
&#x1F923;
```

Aus dieser [Liste aller Emojis](https://getemoji.com/) kann ein passendes Emoji herausgesucht werden. Alternativ kann auch mit dem [EMOJI TRANSLATER](https://emojitranslate.com/) das dazugehörige Emoji gefunden werden.

Einfacher geht es das Emoji mit Copy-and-Paste einzufügen.
