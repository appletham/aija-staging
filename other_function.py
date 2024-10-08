from service_utils import get_google_creds_and_service
from datetime import datetime, timedelta
import os


def save_other_service_booking_information(preferred_service_date, preferred_service_time, service_description,
                                           additional_request="no request"):
    """
        Saves plumbing booking information to a Google Sheet.

        Args:
            preferred_service_date (str): The customer's preferred date for service.
            preferred_service_time (str): The customer's preferred time for service.
            service_description (str): A description of the plumbing issue.
            additional_request (str, optional): Any additional requests from the customer.

        Returns:
            str: A confirmation message for the customer.
    """

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_service_date, preferred_service_time, service_description, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="others!A1:D1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been successfully submitted and that you will "
            "take some time to identify suitable vendors who can address their issue or provide the requested service. "
            "Let them know you’ll get back to them as soon as possible with a final confirmation.")


def validate_other_service_date(preferred_service_date):
    """
    Validates the customer's preferred service date, ensuring it's at least 3 working days from today.
    """
    # Convert the preferred service date to the expected format (DD-MMM-YYYY)
    preferred_date = datetime.strptime(preferred_service_date, '%d-%b-%Y')

    # Get today's date
    today = datetime.now().date()

    # Calculate the earliest valid date
    minimum_lead_days = 3
    earliest_valid_date = today + timedelta(days=minimum_lead_days)

    if preferred_date.date() == today:
        return "Politely inform the customer that same-day requests are not accepted."

    if preferred_date.date() < earliest_valid_date:     # Check if the preferred date is within 3 days from today
        return (f"Inform the customer that since their requested service on {preferred_service_date} is outside "
                "our usual booking window, which requires at least 2 days' notice, you will try to find "
                "vendors who can accommodate the urgent request, but be sure to avoid making promises.")

    if preferred_date.weekday() == 6:    # Check if the preferred date falls on a Saturday or Sunday
        return (f"Inform the customer that since their requested service on {preferred_service_date} falls "
                "on a Sunday, you will try to find vendors who can accommodate the request, but be sure to "
                "avoid making promises.")

    return ("Inform the customer that you will try to find suitable vendors who can address their issue or provide the "
            "requested service. At the same time, continue to gather all other necessary information from the customer.")
