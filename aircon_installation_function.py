from service_utils import get_google_creds_and_service
import os


def save_aircon_installation_booking_details(number_of_ac_units, ac_details, property_type, preferred_site_visit_date,
                                             preferred_site_visit_time, customer_budget="not mentioned",
                                             additional_request="no request"):
    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [""] * 29
    data[0] = preferred_site_visit_date
    data[1] = preferred_site_visit_time
    data[2] = property_type
    data[3] = customer_budget
    data[4] = additional_request
    data[5] = number_of_ac_units

    # Iterate through each air conditioning unit's details
    for i, details in enumerate(ac_details, start=0):
        data[6 + (3 * i)] = details.get('ac_type', '')
        data[7 + (3 * i)] = details.get('horsepower', '')

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="ac_installation!A1:V1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": [data]}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "confirm pricing with vendors and check their availability for the requested service date. "
            "Let them know you’ll get back to them as soon as possible with a final confirmation.")


def estimate_aircon_installation_price():
    """
    Estimate the price for aircon installation and dismantling services.

    Returns:
        str: A description of the estimated costs and the recommendation for a site visit.
    """
    return ("The labor cost for dismantling ranges from RM150 to RM300 per unit, "
            "while installation costs range from RM300 to RM600 per unit. "
            "It is recommended that the customer schedule a site visit first, which costs RM80, to allow for a "
            "thorough assessment of their setup, including factors such as aircon horsepower, piping requirements, "
            "electrical wiring, and site accessibility. This will ensure a more accurate price quote and help "
            "prevent any unexpected costs during installation.")

