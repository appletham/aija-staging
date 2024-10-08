from service_utils import get_google_creds_and_service
import os


def save_plumbing_booking_information(preferred_service_date, preferred_service_time, property_type, service_description,
                                      customer_budget="not mentioned", additional_request="no request"):
    """
        Saves plumbing booking information to a Google Sheet.

        Args:
            preferred_service_date (str): The customer's preferred date for service.
            preferred_service_time (str): The customer's preferred time for service.
            service_description (str): A description of the plumbing issue.
            property_type (str): The type of property (e.g., residential, commercial).
            customer_budget (str, optional): The customer's budget for the service.
            additional_request (str, optional): Any additional requests from the customer.

        Returns:
            str: A confirmation message for the customer.
    """

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_service_date, preferred_service_time, service_description, property_type,
             customer_budget, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="plumbing!A1:F1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Let the customer know that their booking details have been submitted and that you'll need some time "
            "to confirm pricing with vendors and check their availability for the requested service date. "
            "Let them know you’ll get back to them as soon as possible with a final confirmation.")
