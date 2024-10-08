from service_utils import (
    get_google_creds_and_service,
    get_service_price_list
)
import os
from datetime import datetime, timedelta


def save_curtain_making_booking_information(curtain_type, window_dimensions, preferred_site_visit_date,
                                            preferred_site_visit_time, material_type="not mentioned",
                                            additional_features="not mentioned", customer_budget="not mentioned"):

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_site_visit_date, preferred_site_visit_time, curtain_type, material_type,
             additional_features, window_dimensions, customer_budget]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="curtain_making!A1:G1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "check the vendor’s availability. Let them know you’ll get back to them as soon as possible with a "
            "final confirmation.")


def is_curtain_type_selected():
    return ("Ask customers to send you the images or videos of the windows or space where the curtains will be "
            "installed so that you can share with the vendor. "
            "At the same time, continue to gather all other necessary information from the customer.")
