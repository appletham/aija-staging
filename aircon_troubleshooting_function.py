from service_utils import get_google_creds_and_service
import os


def save_ac_troubleshooting_booking_details(preferred_service_date, preferred_service_time,
                                            issue_description, ac_type, ac_brand, ac_model="not mentioned",
                                            customer_budget="not mentioned", additional_request="no request"):
    """
        Saves the confirmed booking information for an aircon troubleshooting service to a Google Sheet.

        Args:
            preferred_service_date (str): The preferred date for the service.
            preferred_service_time (str): The preferred time for the service.
            issue_description (str): The summarized description of the issue with the aircon.
            ac_type (str): The type of aircon, e.g., 'wall-mounted' or 'cassette'.
            ac_brand (str): The brand of the aircon, e.g., 'Toshiba', 'Daikin', 'Midea', etc.
            ac_model (str, optional): The model of the aircon, provided by the customer.
            customer_budget (str, optional): The customer's budget for the service.
            additional_request (str, optional): Any additional request made by the customer.

        Returns:
            str: A confirmation message for the customer.
    """
    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_service_date, preferred_service_time, issue_description,
             ac_type, ac_brand, ac_model, customer_budget, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="ac_troubleshooting!A1:H1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "confirm pricing with vendors and check their availability for the requested service date. "
            "Let them know you’ll get back to them as soon as possible with a final confirmation.")

