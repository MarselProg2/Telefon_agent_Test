# Workflow: Al Vecchio Mulino

## 1. Der Erstkontakt (Voice-Layer)
- Der Agent nimmt ab und fungiert als empathischer Router.
- Er erkennt sofort die Absicht des Kunden (Reservierung vs. Bestellung).

## 2. Der Bestell-Pfad (Die Küche & Abholzeit)
- **Fokus auf das Wesentliche**: Der Agent erfragt die Bestellung, den Tisch (oder Namen) und **zwingend nur die gewünschte Abhol-Uhrzeit**.
- **Datum ignorieren (UX-Boost)**: Der Agent fragt am Telefon *nicht* nach dem Datum, was das Gespräch für den Kunden deutlich flüssiger macht.
- **Silent Data Logging**: Das System ermittelt das heutige Datum selbstständig im Hintergrund und verknüpft es mit der Bestellung. So bleiben wertvolle Daten für Analysen erhalten, ohne den Kunden zu belästigen.
- **Datenbank-Update**: Per SQL-Insert schreibt der Agent die Bestellung (kategorisiert als `pizza` oder `kueche`), die Tisch-ID/Namen, die Abhol-Uhrzeit und das ermittelte Tagesdatum in die Supabase-Tabelle `bestellungen`.

## 3. Der Human-in-the-Loop (Das UI)
- **Dashboards**: Zwei Google Stitch-Dashboards existieren. Sie sind genau benannt als **„Pizza Station“** und **„Kitchen Station“**.
- **Echtzeit-Synchronisation**: Sie lesen in Echtzeit die neuen Bestellungen aus Supabase aus.
- **Menschliche Kontrolle**: Der Koch/Pizzabäcker sieht die genaue Bestellung und wählt die benötigte Zubereitungszeit über vorgegebene **Radio-Buttons** (5m, 10m, 15m, 30m, 40m, 50m oder 60m).
- **Der Vertrag**: Mit Klick auf "Bestätigen" wird diese Zeit als verbindlicher „Vertrag“ zurück in Supabase geschrieben.

## 4. Der Feedback-Loop
- Die KI liest die bestätigte Zeit aus der Datenbank und kann den Gast nun über die exakte Lieferzeit informieren.