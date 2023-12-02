\page CONTRIBUTING Contributing

\tableofcontents

## Architektur 🏭️

Das YouTubeDownloader Tool ist nach dem Model-View-Controller (MVC) Pattern aufgebaut, wobei eine klare Trennung zwischen View und Controller nicht möglich ist.

> In Qt land the distinction between the View & Controller gets a little murky. Qt accepts input events from the user (via the OS) and delegates these to the widgets (Controller) to handle. However, widgets also handle presentation of the current state to the user, putting them squarely in the View. Rather than agonize over where to draw the line, in Qt-speak the View and Controller are instead merged together creating a Model/ViewController architecture — called "Model View" for simplicity sake. [Quelle](https://pythonguis.com/tutorials/modelview-architecture/)
> <br>

@startuml cdYouTubeDownloaderSWComponents
skinparam titleFontSize 30
skinparam titleFontStyle bold
skinparam packageBorderColor black
skinparam packageFontSize 18
skinparam groupFontStyle bold
skinparam componentBorderColor black
skinparam interfaceBorderColor black
skinparam CollectionsBorderColor black

title SW components of YouTubeDownloader Tool

node "YouTubeDownloader.ico" as icon #yellow

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

Der Einstiegspunkt in die Anwendung ist die Datei `youtube_downloader.py`. Sie startet den Startbildschirm und dann das Anwendungsfenster.

### Controller

Das gestartete Anwendungsfenster wird von den verschiedenen View Controllern (`Source/Controller`) gesteuert. Diese verarbeiten die Benutzereingaben, aktualisieren die im Model gespeicherten Daten und aktualisieren auf dieser Basis die View. Es ist eine Mischung aus View und Controller. Für jeden Teil der Anwendung gibt es einen eigenen Controller, z.B. steuert der `MainWindowController` das Hauptfenster der Anwendung inklusive Menüleiste, Verbindung zur Hardware, etc. Jeder Reiter oder Dialog wird von einem eigenen Controller gesteuert.

### Background-Worker

Ressourcenintensive Operationen wie z.B. der Download von YouTube Inhalten werden in Threads ausgelagert und befinden sich unter `Source/Worker`. Dadurch wird der Main-Thread nicht blockiert, so dass die GUI nicht einfriert.

### Util

Anwendungsweite, globale Konstanten und andere Daten werden in `Util/downloader_data.py` gespeichert. Die Log-Konfiguration wird von der Klasse `LogConfig` in `Util/bonprinter_log.py` verwaltet. Der globale Exception Handler befindet sich in `Util/bonprinter_err_handler.py`.

---

## Versionsverwaltung

Die Version ist in `Source/Util/downloader_data.py` gespeichert und wird manuell aktualisiert. Im Ordner `Executable` befindet sich ein Hilfsskript (`Executable/generate_version_file.py`), welches die aktuelle Versionsinfo-Datei erzeugt, die für die Generierung der Exe-Datei benötigt wird.

---

## Exe-Generierung 🔧

Die Generierung der EXE erfolgt mit Hilfe des `pyinstallers`. In der Datei `Executable/generate_executable.py` werden die notwendigen Parameter angegeben. Durch Ausführen des Batch-Skripts wird die EXE im Verzeichnis `Executable/bin` erzeugt.

## Setup-Generierung 🔧

Die Generierung des Installers erfolgt mit Hilfe von [InnoSetup6](https://jrsoftware.org/isdl.php). In der Datei `Executable/setup_bonprinter.iss` sind die notwendigen Parameter spezifiziert. Durch Ausführen des Batch-Skripts `Executable/generate_setup.bat` wird der Installer EXE im Ordner `Executable/bin` erzeugt.

---

## GitHub Release Schritte

### Vorbereitung

- [ ] Versionierung hochzählen
- [ ] `B_DEBUG` im Code auf `False` setzen
- [ ] Versionen der Pakete von Drittanbietern (`Documentation/Installation/requirements.txt`, `Documentation/Installation/constraints.txt`) (und optional Python-Version) aktualisieren (wenn die PyQT-Version aktualisiert wird, müssen die Views anschließend neu generiert werden)
- [ ] Liste der erlaubten, in EXE eingebundenen Pakete aktualisieren (`L_ALLOWED_THIRD_PARTY_PACKAGES` in `Executable/check_included_packages.py`)
- [ ] Nicht benötigte Pakete explizit ausschließen (`L_EXCLUDE_MODULES` in `Executable/generate_executable.py`).

### Tests

- [ ] CI Jobs für statische Prüfungen starten
- [ ] stichprobenartige Prüfung aller Funktionen

### Freigabe

- [ ] Nach Merge in master: Commit taggen (z.B. `v1.0.0`) & Release erstellen
