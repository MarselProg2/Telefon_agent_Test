# Telefon Agent Projektplan

## Aufgabe 1: Der "Gatekeeper" & Orchestrator (Systemdesign)
**Ziel:** Den Audio-Stream von Twilio empfangen und die Agenten-Kette starten.

*   **Technik:** Verbinde Twilio per Media Streams (Websockets) mit deinem Backend. Nutze das Google ADK, um den Stream nativ an Gemini zu übergeben.
*   **Wirtschaftsinformatik-Fokus:** Erstelle ein Sequenzdiagramm. Wer spricht wann mit wem?
*   **Agent 1 (Receptionist):** Nimmt den Anruf an (ElevenLabs Voice), erkennt die Absicht (Order vs. Support) und leitet die Daten weiter.
*   **Agent 2 (Manager):** Überwacht den Prozess und entscheidet, ob ein menschlicher Mitarbeiter (Human-in-the-Loop) eingreifen muss.

> **Merksatz:** "Teile und herrsche: Ein Agent, der nur eine Sache perfekt macht, ist stabiler als ein Generalist."

## Aufgabe 2: RAG & Personalisierung (Keine generischen Antworten)
**Ziel:** Der Agent soll den Kunden wiedererkennen ("Hallo Herr Schmidt, wieder die Pizza Salami?") und das Menü kennen.

*   **Technik:** Integriere eine Vektordatenbank (z.B. Pinecone). Speichere dort das Menü (PDF/Text) und die Kundenhistorie.
*   **Aufgabe:** Implementiere einen RAG-Workflow. Bevor der Agent antwortet, sucht er im "Gedächtnis" nach relevanten Infos.
*   **Wirtschaftsinformatik-Fokus:** Definiere das Context Window. Wie viele alte Bestellungen darf der Agent "sehen", ohne dass die Token-Kosten explodieren?

> **Merksatz:** "Wissen ohne Kontext ist nur Lärm – RAG gibt deiner KI ein Gedächtnis."

## Aufgabe 3: Token-Management & Finance Dashboard
**Ziel:** Jedes Wort kostet Geld. Du musst wissen, wie viel Gewinn nach Abzug der API-Kosten übrig bleibt.

*   **Technik:** Nutze die Metadaten von Google ADK und ElevenLabs. Erfasse `input_tokens` und `output_tokens` sowie die Sekunden der Voice-Synthese.
*   **Aufgabe:** Erstelle eine Middleware, die diese Daten in eine SQL-Datenbank schreibt und auf deinem Dashboard (React/Streamlit) die "Cost-per-Call" live anzeigt.
*   **Wirtschaftsinformatik-Fokus:** Berechne den Break-Even-Point. Ab welcher Gesprächsdauer ist der Anruf für das Unternehmen unrentabel?

> **Merksatz:** "Technik ist cool, aber nur schwarze Zahlen sichern das Projekt."

## Aufgabe 4: Deployment & Automatisierung (GitHub Actions & Docker)
**Ziel:** Dein System muss professionell deployt werden, nicht nur auf deinem Laptop laufen.

*   **Technik:** Schreibe ein Dockerfile für deinen Orchestrator-Service.
*   **Aufgabe:** Erstelle eine GitHub Action, die bei jedem Push:
    1.  Den Code auf Fehler prüft (Linting).
    2.  Das Docker-Image baut.
    3.  Das Image automatisch in die Cloud (z.B. Google Cloud Run) schiebt.
*   **Wirtschaftsinformatik-Fokus:** "Last-Mover-Vorteil". Warte nicht, bis dein Code perfekt ist, aber sorge dafür, dass dein Automatisierungsgrad so hoch ist, dass du schneller iterieren kannst als jeder Konkurrent.

> **Merksatz:** "Automatisierung ist der Zinseszins der Softwareentwicklung."
