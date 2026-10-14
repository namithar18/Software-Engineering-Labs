"""Manage pharmacy stock, patient allergies, and prescriptions."""

import json
import sqlite3
from datetime import datetime, timedelta

# Global state
conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    """Create and populate the patient database."""
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE patients "
        "(id TEXT, name TEXT, allergy TEXT)"
    )
    patients = [
        ("P1", "Kavya", "penicillin"),
        ("P2", "Arjun", "none"),
        ("P3", "Meena", "ibuprofen"),
    ]
    cur.executemany(
        "INSERT INTO patients VALUES (?, ?, ?)", patients
    )
    conn.commit()


def find_patient(name):
    """Find a patient by name and return their ID and allergy."""
    cur = conn.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cur.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add drug units to stock and record the batch."""
    if batch_log is None:
        batch_log = []

    if units < 0:
        raise ValueError("Stock units cannot be negative.")

    datetime.strptime(expiry, "%Y-%m-%d")

    current_stock = stock.get(drug, {})
    stock[drug] = {
        "units": current_stock.get("units", 0) + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


# pylint: disable=too-many-return-statements
def dispense(patient_name, drug, units):
    """Dispense medicine if the patient and stock are valid."""
    if units <= 0:
        print("Dispense quantity must be positive.")
        return False

    patients = find_patient(patient_name)
    if not patients:
        print("Patient not found:", patient_name)
        return False

    patient_id, allergy = patients[0]

    if allergy.strip().casefold() != "none":
        allergies = {
            item.strip().casefold()
            for item in allergy.split(",")
        }
        if drug.strip().casefold() in allergies:
            print("Allergy warning for", patient_name)
            return False

    if drug not in stock:
        print("Drug not found in stock:", drug)
        return False

    expiry_date = datetime.strptime(
        stock[drug]["expiry"], "%Y-%m-%d"
    ).date()

    if expiry_date < datetime.now().date():
        print("Cannot dispense expired medicine:", drug)
        return False

    if stock[drug]["units"] < units:
        print("Insufficient stock for", drug)
        return False

    stock[drug]["units"] -= units
    prescriptions.append(
        {
            "patient": patient_id,
            "drug": drug,
            "units": units,
            "time": datetime.now().isoformat(),
        }
    )
    return True


def expiring_soon(days=30):
    """Return drugs expiring within the specified number of days."""
    if days < 0:
        raise ValueError("Days cannot be negative.")

    soon = []
    today = datetime.now().date()
    deadline = today + timedelta(days=days)

    for drug, details in stock.items():
        expiry = datetime.strptime(
            details["expiry"], "%Y-%m-%d"
        ).date()

        if today <= expiry <= deadline:
            soon.append(drug)

    return soon


def export_prescriptions(file="prescriptions.json"):
    """Export prescription records to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(prescriptions, output_file, indent=4)


def load_stock(file="stock.json"):
    """Load and validate stock records from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as stock_file:
            loaded_stock = json.load(stock_file)

        if not isinstance(loaded_stock, dict):
            raise ValueError("Stock data must be a JSON object.")

        for drug, details in loaded_stock.items():
            if (
                not isinstance(details, dict)
                or not isinstance(details.get("units"), int)
                or isinstance(details.get("units"), bool)
                or details["units"] < 0
                or not isinstance(details.get("expiry"), str)
            ):
                raise ValueError(f"Invalid stock record for {drug}.")

            datetime.strptime(details["expiry"], "%Y-%m-%d")

        return loaded_stock

    except FileNotFoundError:
        return {}
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not load stock: {error}")
        return {}


def print_stock():
    """Display all drugs and their current stock levels."""
    print("Pharmacy Stock")
    for drug, details in stock.items():
        print(
            f"{drug} -> {details['units']} units, "
            f"expires {details['expiry']}"
        )


def main():
    """Run the pharmacy stock demonstration."""
    setup_database()
    stock.update(load_stock())

    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", 15, "2026-11-30")

    print(
        "Arjun gets Amoxicillin:",
        dispense("Arjun", "Amoxicillin", 10),
    )
    print(
        "Kavya gets Penicillin:",
        dispense("Kavya", "Penicillin", 10),
    )
    print(
        "Meena gets ibuprofen:",
        dispense("Meena", "ibuprofen", 2),
    )
    print(
        "Unknown patient:",
        dispense("Ghost", "Paracetamol", 5),
    )

    name = input(
        "Patient name to look up (Enter for Arjun): "
    ).strip() or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())

    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()
