import asyncio
import re
import random
from core.config_bd import load_bd
from core.email.senders import send_email


def _extract_msg_data(message):
    text = message.text or ""

    if text == "" or not text:
        return None

    reference_match = re.search(r"(?:Referencia|Referència|URGENT_Referència)\s*:\s*(.+)",text, re.IGNORECASE)
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text, re.IGNORECASE)
    company_match = re.search(r"(?:Centre|Centro)\s*:\s*(.+)", text, re.IGNORECASE)

    reference = (reference_match.group(1).strip() if reference_match else None)
    email = (email_match.group(0).strip() if email_match else None)
    company = (company_match.group(1).strip() if company_match else None)

    return {
        "reference" : reference,
        "email": email,
        "company": company
    }

async def check_msg_job_application(message):

    data = _extract_msg_data(message)
    print(data)
    bd = load_bd()

    if data is None or data["company"] not in bd["companies"]:
        return

    if not data["email"] or not data["reference"]:
        return

    delay = random.uniform(5, 30)

    await asyncio.sleep(delay)
    print(data)
    print("tiempo", delay)
    email = data["email"]
    subject = f"Referéncia: {data["reference"]}"

    body = f"""
        1. Nom i Cognoms: Denis Esteban Aguilar
        2. Telèfon mòbil de contacte: 644461020
        3. CV actualitzat i certificat ds:
    """

    send_email(email, subject, body)