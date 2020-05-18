<h1 align="center">
  Pandemie
</h1>
<h3 align="center">
Lösungsvorschlag für den InformatiCup 2020 der Gesellschaft für Informatik
</h3>
<p align="center">
Dieses Repository beeinhaltet die Lösung für den InformatiCup 2020 des Teams Nicolas Schaber, Daniel Schulz und Max Schiffer der DHBW Karlsruhe.
</p>
<p align="center">
Repository der Aufgabe: https://github.com/informatiCup/informatiCup2020
</p>
<p align="center">
    <a href="https://www.python.org/"><img alt="GitHub top language" src="https://img.shields.io/github/languages/top/nicosc77/pandemie?style=for-the-badge"></a>
</p>

## 🚀 Deployment

- **Docker:**
Mithilfe des Dockerfile im Root-Verzeichnis des Projekt lässt sich ein Image bauen, das als Container mit Docker ausgeführt werden kann. Die Anwendung ist dann unter http://localhost:5000 zu erreichen. 
  ```shell
  docker build -t pandemie .
  docker run -p 5000:5000 -d pandemie
  ```

## 🔧Testen
Mithilfe der aktuellsten Version des Kommandozeilen-Tools aus dem Repository des Wettbewerbs kann mit der Software ein Spiel gespielt werden. Dazu führt man das Tool mit Angabe der URL der Anwendung aus. Auf Unix-Systemen muss das Tool eventuell zuerst ausführbar gemacht werden.

Hier z.B. mit der URL für das lokale Deployment:
- **Windows:**
  ```shell
  ic20_windows.exe -u "http://localhost:5000"
  ```
- **Linux:**
  ```shell
  ./ic20_linux -u "http://localhost:5000"
  ```
- **macOS:**
  ```shell
  ./ic20_darwin -u "http://localhost:5000"
  ```

Anschließend spielt das Tool gegen unsere KI der Software ein Spiel. Nachdem entweder gewonnen oder verloren wurde wird das Tool beendet. Im Feld "outcome" des Spiele-Logs lässt sich der Ausgang des Spiels durch "win" oder "loss" feststellen.

## 📄Dokumentation
Genauere Informationen zu dieser Software ist in der [Dokumentation](Dokumentation.pdf) zu finden.

