from service_utils import (
    get_google_creds_and_service,
    get_service_price_list
)
import os
from datetime import datetime, timedelta


def save_renovation_booking_information(renovation_location, renovation_description, preferred_site_visit_date,
                                        preferred_site_visit_time, customer_budget="not mentioned"):

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_site_visit_date, preferred_site_visit_time, renovation_location, renovation_description,
             customer_budget]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="renovation!A1:E1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "confirm pricing with vendors and check their availability for the requested site inspection date. "
            "Let them know you’ll get back to them as soon as possible with a final confirmation.")


def validate_renovation_service_date(preferred_site_visit_date):
    """
    Validates the customer's preferred service date, ensuring it's at least 3 working days from today.
    """
    # Convert the preferred service date to the expected format (DD-MMM-YYYY)
    preferred_date = datetime.strptime(preferred_site_visit_date, '%d-%b-%Y')

    # Get today's date
    today = datetime.now().date()

    # Calculate the earliest valid date
    minimum_lead_days = 7
    earliest_valid_date = today + timedelta(days=minimum_lead_days)

    if preferred_date.date() == today:
        return "Politely inform the customer that same-day requests are not accepted."

    if preferred_date.date() < earliest_valid_date:     # Check if the preferred date is within 3 days from today
        return (f"Inform the customer that since their requested service on {preferred_site_visit_date} is outside "
                "our usual booking window, which requires at least 1 week notice, you will try to find "
                "vendors who can accommodate the urgent request, but be sure to avoid making promises.")

    if preferred_date.weekday() == 6:    # Check if the preferred date falls on a Saturday or Sunday
        return (f"Inform the customer that since their requested service on {preferred_site_visit_date} falls "
                "on a Sunday, you will try to find vendors who can accommodate the request, but be sure to "
                "avoid making promises.")

    return ("Inform the customer that you will check with the vendors for their availability and will get back "
            "to them as soon as you have an update. At the same time, continue to gather all other necessary "
            "information from the customer.")
