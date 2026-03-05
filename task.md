# Projekt-Fortschritt: Telefon-Agent (Last Mover Edition)

Wir folgen dem iterativen Lernplan: Erst Prototyp, dann Profi-Refactoring.

- [ ] **Phase 1: Der "Dirty Prototype"**
    - [x] Twilio & Ngrok Setup (Infrastruktur)
    - [x] Einfacher ADK-Agent ("Hallo Welt")
    - [x] Erster erfolgreicher Telefonanruf
    - [x] Hardcodierte Logik (Reservierung) testen
    - [x] Pydantic Models für Reservierungen, Bestellungen und Telefonagenten
    -frontend mit gradio und google stitch später nutzen per MCP(stitch skills nutzen)

- [ ] **Phase 2: Analyse & Schwachstellen**
    - [ ] Testanrufe durchführen und scheitern lassen (Gedächtnis, Validierung)
    - [ ] Log-Analyse via ElevenLabs (`list_conversations`)

- [x] **Phase 3: Der "Last Mover" Umbau (Infrastruktur)**
    - [x] **Typensicherheit**: Pydantic Models (`Order`, `Reservation`) in `schemas.py`
    - [x] **Datenbank**: Supabase/Postgres Integration via McpToolset (Option A)
    - [x] **Reservierung**: Check via SQL Query (kein fiktives Tool mehr)
    - [ ] **RAG**: Speisekarte als Vektoren laden (`add_knowledge_base_to_agent`)

- [ ] **Phase 4: Workflow & Enterprise Grade**
    - [ ] **Pipeline**: `bestell_pipeline` (SequentialAgent) implementieren
    - [ ] **ReFORCE**: Human-in-the-Loop LoopAgent (Koch-Bestätigung)
    - [ ] **Dashboard**: Gradio Dashboard für Bestellübersicht
    - [ ] **CI/CD**: GitHub Actions Pipeline

---

## Dein Werkzeugkasten (Toolbox)

### Phase 1: Der "Dirty Prototype"
| Dein Werkzeug | Mein MCP-Tool | Wofür? |
| :--- | :--- | :--- |
| **Python (`adk`)** | `create_agent` | Basis-Agent. |
| **Twilio** | `list_phone_numbers` | Nummer anzeigen. |
| **Ngrok** | `make_outbound_call` | Testanruf. |

### Phase 4: Enterprise Grade
| Dein Werkzeug | Mein MCP-Tool | Wofür? |
| :--- | :--- | :--- |
| **Gradio** | `list_conversations` | Dashboard bauen. |
