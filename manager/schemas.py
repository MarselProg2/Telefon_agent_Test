from pydantic import BaseModel, Field
from typing import Optional

class Reservation(BaseModel):
    guest_name: str = Field(description="Name des Gastes")
    number_of_people: int = Field(description="Anzahl der Personen")
    time: str = Field(description="Uhrzeit im Format HH:MM")
    date: str = Field(description="Datum im Format DD.MM.YYYY")
    visit_reason: str = Field(description="Grund des Besuchs (z.B. Geburtstag, Jahrestag)", default="Essen")
    allergies_asked: bool = Field(description="Wurden Allergien abgefragt?", default=False)
    allergies: str = Field(description="Genannte Allergien", default="Keine")

class Order(BaseModel):
    guest_name: str = Field(description="Name des Gastes")
    order_details: str = Field(description="Detaillierte Bestellung (Gerichte, Getränke)")
    
class TelephoneData(BaseModel):
    summary: str = Field(description="Zusammenfassung des Gesprächs")
    reservation: Optional[Reservation] = Field(description="Reservierungsdaten, falls vorhanden", default=None)
    order: Optional[Order] = Field(description="Bestelldaten, falls vorhanden", default=None)

   