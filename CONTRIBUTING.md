\page CONTRIBUTING Contributing

\tableofcontents

## Architektur 🏭️

Das YouTube Downloader Tool ist nach dem Model-View-Controller (MVC) Pattern aufgebaut, wobei eine klare Trennung von View und Controller nicht möglich ist.

> In Qt land the distinction between the View & Controller gets a little murky. Qt accepts input events from the user (via the OS) and delegates these to the widgets (Controller) to handle. However, widgets also handle presentation of the current state to the user, putting them squarely in the View. Rather than agonize over where to draw the line, in Qt-speak the View and Controller are instead merged together creating a Model/ViewController architecture — called "Model View" for simplicity sake. [Quelle](https://pythonguis.com/tutorials/modelview-architecture/)
<br>

@startuml cdYouTubeDownloaderSWComponents
skinparam titleFontSize 30
skinparam titleFontStyle bold
skinparam packageBorderColor black
skinparam packageFontSize 18
skinparam groupFontStyle bold
skinparam componentBorderColor black
skinparam interfaceBorderColor black
skinparam CollectionsBorderColor black

title SW components of YouTube Downloader Tool

node "app.ico" as icon #yellow

package "YouTubeDownloader" as YtDl #ededed {
  component "**youtube_downloader**" as youtube_downloader #63d8ff
  note left of youtube_downloader
    Application entry point:
    Init and startup
  end note
  package "Controller" as controller {
    [main_window]
  }
  package "Util" as util {
    [downloader_data] as data
  }
  note top of data
    Constants (e.g paths, keys) and
    Functions related to data.
    Included by most components.
  end note
  package "Worker" {
    [downloader]
  }
  [youtube_downloader] -d-> [main_window]
  [youtube_downloader] -[#black]u--> icon
}

node "YouTubeDownloader.exe" #plum

package "Python Libraries (mostly third party)" #lightgreen {
 [PyInstaller]
 [pytube]
}

[youtube_downloader] -[#black]-> [downloader]
[downloader] -[#black]-> [pytube]
[PyInstaller] -[#black]d-> YouTubeDownloader.exe

@enduml

### Einstiegspunkt

Den Einstiegspunkt in die Anwendung bildet die Datei `youtube_downlaoder.py`. Sie startet den Splashscreen und anschließend das Anwendungsfenster.

### Controller

Das gestartete Anwendungsfenster wird von den verschiedenen View-Controllern (`Source/Controller`) gesteuert. Diese verarbeiten Benutzereingaben, aktualisieren die gespeicherten Daten im Model und aktualisieren darauf basierend die View. Es handelt sich um die Mischung aus View und Controller. Für jeden Anwendungsteil gibt es einen eigenen Controller. z.B steuert der `MainWindowController` das Hauptanwendungsfenster inklusive Menüleiste, Verbindung zum Hardware, etc. Jeder Tab oder Dialog wird durch einen eigenen Controller gesteuert.

### Background-Worker

Ressourcenintensive Operationen wie der Download von YouTube Inhalten ist in Threads ausgelagert und befindet sich unter `Source/Worker`. Dadurch wird der Main Thread nicht blockiert, damit die GUI nicht gefreezed wird ("Keine Rückmeldung").

### Util

Applikationsweite, globale Konstanten und anderer Daten werden unter `Util/downloader_data.py` gespeichert.

---

## Versionsverwaltung

Die Version ist in `Source/Util/downloader_data.bat` hinterlegt und wird manuell inkrementiert. Im Ordner `Executable` liegt ein Hilfsskript (`generate_version_file.py`) welches das aktuelle Versionsinfo-File generiert, das zur Exe-Generierung benötigt wird.

---

## Exe-Generierung 🔧

Die Generierung der EXE wird mithilfe des `pyinstaller` gemacht. In der Datei `Executable/generate_executable.bat` sind die dafür notwendigen Parameter spezifiziert. Durch Ausführen des Batch-Skriptes wird im Ordner `Executable/bin` die EXE erzeugt.

---

## GitHub Release Schritte

### Vorbereitung

* [ ] Versionierung hochzählen
* [ ] Versionen der Drittanbieterpakete (packages.txt) (und optional Python Version) auf den neuesten Stand aktualisieren (bei Aktualisierung der PyQT Version müssen die Views anschließend neu generiert werden)
* [ ] Liste der erlaubten, in EXE inkludierten Paketen aktualisieren (`l_allowed_third_party_packages` in `Executable/check_include_packages.py`
* [ ] Nicht benötigte Pakete ggf. explizit exkludieren (--exclude-modules` in `Executable/generate_executable.bat`)

### Tests

* [ ] EXE generieren, alle Funktionalitäten stichprobenartig testen

### Freigabe

* [ ] Nach Merge in master: Commit taggen (z.B. `YouTubeDownloader - 1.0.0` & Release erstellen mit Links auf Executable in Package Registry
