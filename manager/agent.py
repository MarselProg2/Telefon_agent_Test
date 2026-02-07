from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.agents.parallel_agent import ParallelAgent
from mcp import StdioServerParameters
from dotenv import load_dotenv
import os
from .reservation_tool import reservation_tool
from .schemas import Reservation, Order, TelephoneData
load_dotenv()
GEMINI_MODEL = "gemini-2.0-flash"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
agent_id = os.getenv("AGENT_ID")
to_number = os.getenv("TO_NUMBER")
agent_phone_number_id = os.getenv("AGENT_PHONE_NUMBER_ID")




reservation_agent = Agent(
    name="reservation_agent",
    model=GEMINI_MODEL,
    instruction="""
    Du bist ein Reservierungs-Assistent für ein Restaurant.
    
    DEIN PROZESS (HALTE DICH STRENG DARAN):
    
    SCHRITT 1: TISCHE PRÜFEN
    - Bevor du IRGENDETWAS anderes tust oder den Kunden nach Daten fragst, MUSST du das Tool `reservation_tool` aufrufen.
    - Das Tool gibt dir eine Liste von Tischen und deren Status (z.B. {"tisch1": "belegt", ...}).
    - Analysiere das Ergebnis:
        - Sind ALLE Tische "belegt"? -> Sag dem Kunden höflich ab ("Tut mir leid, wir sind voll.") und beende das Gespräch.
        - Ist mindestens ein Tisch "frei"? -> Mach weiter mit SCHRITT 2.
    
    SCHRITT 2: DATEN AUFNEHMEN
    - Nur wenn Tische frei sind!
    - Frage den Kunden nach:
        1. Datum
        2. Uhrzeit
        3. Anzahl der Personen
        4. Name
        5. Grund des Besuchs (z.B. Geburtstag, Jahrestag)
        6. Allergien oder Unverträglichkeiten

    SCHRITT 3: BESTÄTIGUNG
    - Fasse die Reservierung zusammen.
    """,
    description="Zuständig für Tischreservierungen (Datum, Zeit, Personen).",
    tools=[reservation_tool],
    output_type=Reservation,
    output_key="displaying_reservation_data"
)

order_agent = Agent(
    name="order_agent",
    model=GEMINI_MODEL,
    instruction="""
    Du bist ein Bestell-Assistent für Essensbestellungen.
    Deine Aufgabe ist es, Bestellungen für Gerichte und Getränke aufzunehmen.
    
    1. Nimm die Bestellung auf.
    2. Frage bei Unklarheiten nach (z.B. Größe der Pizza).
    3. Am Ende: Fasse die Bestellung zusammen und gib sie als strukturiertes JSON zurück (wenn möglich).
    """,
    description="Zuständig für Essens- und Getränkebestellungen.",
    output_key="displaying_order_data",
    output_type=Order
)

telefon_agent = Agent(
    model=GEMINI_MODEL,
    name="elevenlabs_agent",
    instruction=f"""
    Du bist ein hilfreicher Assistent und die KI-Rezeption eines Restaurants.

    Deine Hauptaufgabe ist es, Anrufe entgegenzunehmen und je nach Anliegen den richtigen Experten hinzuzuziehen.

    ROUTING REGELN (WICHTIG):
    - Wenn der User eine **Bestellung** aufgeben will (Essen, Getränke) -> Delegiere sofort an den `order_agent`.
    - Wenn der User einen **Tisch reservieren** will -> Delegiere sofort an den `reservation_agent`.

    ADMIN REGELN (Nur wenn explizit danach gefragt wird):
    Regel 1: Wenn der User sagt 'Rufe Marsel an', dann MUSST du das Tool `make_outbound_call` benutzen.
    Verwende dabei ZWINGEND diese exakten Parameter:
    - agent_id: "{agent_id}"
    - to_number: "{to_number}"
    - agent_phone_number_id: "{agent_phone_number_id}"
    Frage nicht nach Bestätigung, führe es direkt aus.

    Regel 2: Wenn der User sagt 'alle Nummern geben', dann MUSST du das Tool `list_phone_numbers` benutzen. Verwende dabei ZWINGEND diese exakten Parameter:
    - agent_id: "{agent_id}"
    - to_number: "{to_number}"
    - agent_phone_number_id: "{agent_phone_number_id}"
    Frage nicht nach Bestätigung, führe es direkt aus.

    Regel 3: Wenn der User sagt 'alle Konversationen', dann MUSST du das Tool `list_conversations` benutzen.
     Verwende dabei ZWINGEND diese exakten Parameter:
    - agent_id: "{agent_id}"
    - to_number: "{to_number}"
    - agent_phone_number_id: "{agent_phone_number_id}"
    Frage nicht nach Bestätigung, führe es direkt aus.
    Regel 4: Wenn der User sagt 'gib mir agenten', dann MUSST du das Tool `get_agent` benutzen.
     Verwende dabei ZWINGEND diese exakten Parameter:
    - agent_id: "{agent_id}"
    - to_number: "{to_number}"
    - agent_phone_number_id: "{agent_phone_number_id}"
    Frage nicht nach Bestätigung, führe es direkt aus.
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=["elevenlabs-mcp"],
                    env={
                        "ELEVENLABS_API_KEY": ELEVENLABS_API_KEY,
                    }
                ),
                timeout=30,
            ),
        )
    ],
    sub_agents=[reservation_agent, order_agent],
    output_key="displaying_telephone_data",
    output_type=TelephoneData
)

root_agent = telefon_agent
