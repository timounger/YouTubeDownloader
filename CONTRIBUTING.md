\page CONTRIBUTING Contributing

\tableofcontents

## Architektur 🏭️

Das YouTubeDownloader Tool ist nach dem Model-View-Controller (MVC) Pattern aufgebaut, wobei eine klare Trennung zwischen View und Controller nicht möglich ist.

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

node "app.ico" as icon #yellow

package "YouTubeDownloader" as YtDl #ededed {
  component "**app**" as app #63d8ff
  note left of app
    Application entry point:
    Init and startup
  end note
  package "Controller" as controller {
    [main_window]
  }
  package "Util" as util {
    [app_data] as data
  }
  note top of data
    Constants (e.g paths, keys) and
    Functions related to data.
    Included by most components.
  end note
  package "Worker" {
    [downloader]
  }
  [app] -d-> [main_window]
  [app] -[#black]u--> icon
}

node "YouTubeDownloader.exe" #plum

package "Python Libraries (mostly third party)" #lightgreen {
 [PyInstaller]
 [pytube]
}

[app] -[#black]-> [downloader]
[downloader] -[#black]-> [pytube]
[PyInstaller] -[#black]d-> YouTubeDownloader.exe

@enduml

### Einstiegspunkt

Der Einstiegspunkt in die Anwendung ist die Datei `Source/app.py`. Sie startet den Startbildschirm und dann das Anwendungsfenster.

### Controller

Das gestartete Anwendungsfenster wird von den verschiedenen View Controllern (`Source/Controller`) gesteuert. Diese verarbeiten die Benutzereingaben, aktualisieren die im Model gespeicherten Daten und aktualisieren auf dieser Basis die View. Es ist eine Mischung aus View und Controller.

### Background-Worker

Ressourcenintensive Operationen wie z.B. der Download von YouTube Inhalten werden in Threads ausgelagert und befinden sich unter `Source/Worker`. Dadurch wird der Main-Thread nicht blockiert, so dass die GUI nicht einfriert.

### Util

Anwendungsweite, globale Konstanten und andere Daten werden in `Util/app_data.py` gespeichert.

---

## Versionsverwaltung

Die Version ist in `Source/version.py` gespeichert und wird manuell aktualisiert. Im Ordner `Executable` befindet sich ein Hilfsskript (`Executable/generate_version_file.py`), welches die aktuelle Versionsinfo-Datei erzeugt, die für die Generierung der Exe-Datei benötigt wird.

---

## Exe-Generierung 🔧

Die Generierung der EXE erfolgt mit Hilfe des `pyinstallers`. In der Datei `Executable/generate_executable.py` werden die notwendigen Parameter angegeben. Durch Ausführen des Batch-Skripts wird die EXE im Verzeichnis `Executable/bin` erzeugt.

## Setup-Generierung 🔧

Die Generierung des Installers erfolgt mit Hilfe von [InnoSetup6](https://jrsoftware.org/isdl.php). In der Datei `Executable/setup.iss` sind die notwendigen Parameter spezifiziert. Durch Ausführen des Batch-Skripts `Executable/generate_setup.bat` wird der Installer EXE im Ordner `Executable/bin` erzeugt.

---

## GitHub Release Schritte

### Vorbereitung

- [ ] Versionierung hochzählen
- [ ] `B_DEBUG` im Code auf `False` setzen
- [ ] Versionen der Pakete von Drittanbietern (`Documentation/Installation/requirements.txt`, `Documentation/Installation/constraints.txt`) (und optional Python-Version) aktualisieren
- [ ] Liste der erlaubten, in EXE eingebundenen Pakete aktualisieren (`L_ALLOWED_THIRD_PARTY_PACKAGES` in `Executable/check_included_packages.py`)
- [ ] Nicht benötigte Pakete explizit ausschließen (`L_EXCLUDE_MODULES` in `Executable/generate_executable.py`).

### Tests

- [ ] CI Jobs für statische Prüfungen starten
- [ ] stichprobenartige Prüfung aller Funktionen

### Freigabe

- [ ] Nach Merge in master: Commit taggen (z.B. `v1.0.0`) & Release erstellen
