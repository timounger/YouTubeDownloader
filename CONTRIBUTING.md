\page CONTRIBUTING Contributing

\tableofcontents

## Architektur 🏭️

Das YouTube Downloader Tool ist nach dem Model-View-Controller (MVC) Pattern aufgebaut, wobei eine klare Trennung zwischen View und Controller nicht möglich ist.

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

Der Einstiegspunkt in die Anwendung ist die Datei `youtube_downlaoder.py`. Sie startet das Anwendungsfenster.

### Controller

Das gestartete Anwendungsfenster wird von den verschiedenen View Controllern (`Source/Controller`) gesteuert. Diese verarbeiten die Benutzereingaben, aktualisieren die im Model gespeicherten Daten und aktualisieren auf dieser Basis die View. Es ist eine Mischung aus View und Controller. Für jeden Teil der Anwendung gibt es einen eigenen Controller, z.B. steuert der `MainWindowController` das Hauptfenster der Anwendung inklusive Menüleiste, Verbindung zur Hardware, etc.

### Background-Worker

Ressourcenintensive Operationen wie z.B. der Download von YouTube Inhalten werden in Threads ausgelagert und befinden sich unter `Source/Worker`. Dadurch wird der Main-Thread nicht blockiert, so dass die GUI nicht einfriert.

### Util

Anwendungsweite, globale Konstanten und andere Daten werden in `Util/downloader_data.py` gespeichert.

---

## Versionsverwaltung

Die Version ist in `Source/Util/downloader_data.bat` gespeichert und wird manuell aktualisiert. Im Ordner `Executable` befindet sich ein Hilfsskript (`generate_version_file.py`), welches die aktuelle Versionsinfo-Datei erzeugt, die für die Generierung der Exe-Datei benötigt wird.

---

## Exe-Generierung 🔧

Die Generierung der EXE erfolgt mit Hilfe des `pyinstallers`. In der Datei `Executable/generate_executable.bat` werden die notwendigen Parameter angegeben. Durch Ausführen des Batch-Skripts wird die EXE im Verzeichnis `Executable/bin` erzeugt.

---

## GitHub Release Schritte

### Vorbereitung

* [ ] Versionierung hochzählen
* [ ] Versionen der Pakete von Drittanbietern (requirements.txt) (und optional Python-Version) aktualisieren.
* [ ] Liste der erlaubten, in EXE eingebundenen Pakete aktualisieren (`l_allowed_third_party_packages` in `Executable/check_include_packages.py`
* [ ] Nicht benötigte Pakete explizit ausschließen (`--exclude-modules` in `Executable/generate_executable.bat`).

### Tests

* [ ] EXE generieren, alle Funktionalitäten stichprobenartig testen

### Freigabe

* [ ] Nach Merge in master: Commit taggen (z.B. `v1.0.0`) & Release erstellen
