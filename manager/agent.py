from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from dotenv import load_dotenv
import os
import sys
from .schemas import Reservation, Order, TelephoneData

# --- KONFIGURATION & VALIDIERUNG ---
load_dotenv()

REQUIRED_ENV_VARS = [
    "ELEVENLABS_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY"
]

for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        print(f"CRITICAL ERROR: Environment variable {var} is missing!")

GEMINI_MODEL = "gemini-2.0-flash"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# --- TOOLSETS ---

# Supabase MCP Toolset (Option A: Direkt via npx)
supabase_mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-supabase"],
            env={
                "SUPABASE_URL": SUPABASE_URL,
                "SUPABASE_API_KEY": SUPABASE_SERVICE_ROLE_KEY,
            }
        ),
        timeout=30,
    ),
)

# ElevenLabs MCP Toolset
elevenlabs_mcp = McpToolset(
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

# --- AGENTS (DIE SPEZIALISTEN) ---

reservation_agent = Agent(
    name="reservation_agent",
    model=GEMINI_MODEL,
    instruction="""
    Du bist der Reservierungs-Experte des Restaurants Al Vecchio Mulino.
    
    DEIN PROZESS:
    1. PRÜFUNG: Nutze `supabase_mcp` (Tool: `execute_sql`), um die Anzahl der belegten Plätze für das gewünschte Datum zu prüfen. 
       Wenn das Restaurant voll ist, beende das Gespräch.
    2. DATEN: Frage nach Datum, Zeit, Personenzahl, Name und Allergien.
    3. DB-SCHREIBEN: Nutze `supabase_mcp` (Tool: `insert_row`), um die Daten in die Tabelle 'reservierungen' zu schreiben.
       Spalten: name, datum, uhrzeit, personen, grund, allergien.
    4. ABSCHLUSS: Bestätige die Reservierung dem Kunden.
    """,
    description="Bearbeitet Tischreservierungen via Datenbank-Abfrage.",
    tools=[supabase_mcp],
    output_type=Reservation,
    output_key="displaying_reservation_data"
)

order_agent = Agent(
    name="order_agent",
    model=GEMINI_MODEL,
    instruction="""
    Du bist der Bestell-Experte. Nimm die Wünsche des Kunden präzise auf.
    
    1. FRAGE: Was möchte der Kunde essen/trinken? (Gerichte, Extras, Größen).
    2. FRAGE: Wann möchte der Kunde die Bestellung abholen?
    3. KATEGORIE: Weise die Bestellung 'pizza' oder 'kitchen' zu.
    4. ZUSAMMENFASSUNG: Fasse alles nochmal kurz zusammen.
    
    WICHTIG: Deine Antwort muss am Ende alle Daten für das 'Order' Schema enthalten.
    """,
    description="Nimmt Essensbestellungen auf und validiert Details.",
    output_key="displaying_order_data",
    output_type=Order
)

db_writer_agent = Agent(
    name="db_writer_agent",
    model=GEMINI_MODEL,
    instruction="""
    Du bist der Daten-Logistiker.
    Übernimm die Bestelldaten aus der Konversation und schreibe sie in die Supabase Tabelle 'bestellungen'.
    
    NUTZE DAS TOOL: `supabase_mcp` (Tool: `insert_row`)
    SPALTEN-MAPPING:
    - items -> gerichte
    - pickup_time -> abholzeit
    - category -> kategorie
    - customer_name -> tisch_oder_name
    
    Sage dem Kunden danach, dass die Bestellung erfolgreich im System registriert wurde.
    """,
    tools=[supabase_mcp],
    description="Sicherheits-Layer: Schreibt validierte Bestellungen in die Datenbank."
)

# --- PIPELINES (DIE WORKFLOWS) ---

bestell_pipeline = SequentialAgent(
    name="bestell_pipeline",
    sub_agents=[order_agent, db_writer_agent],
    description="Garantierter Workflow: Erst Aufnahme, dann DB-Speicherung."
)

# --- DISPATCHER (DER MANAGER) ---

telefon_agent = Agent(
    model=GEMINI_MODEL,
    name="elevenlabs_agent",
    instruction="""
    Du bist die Stimme von Al Vecchio Mulino. Empfange jeden Gast mit Wärme und Professionalität.
    
    ROUTING:
    - Bestellung -> Delegiere an `bestell_pipeline`.
    - Reservierung -> Delegiere an `reservation_agent`.
    
    Versuche nicht, diese Aufgaben selbst zu lösen. Du bist der Koordinator.
    """,
    tools=[elevenlabs_mcp],
    sub_agents=[reservation_agent, bestell_pipeline],
    output_key="displaying_telephone_data",
    output_type=TelephoneData
)

root_agent = telefon_agent
