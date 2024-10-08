from service_utils import (
    get_google_creds_and_service,
    get_service_price_list
)
import os


def save_pest_control_booking_information(pest_type, affected_areas, first_notice, entry_point, previous_treatments,
                                          preferred_service_date, preferred_service_time,
                                          customer_budget="not mentioned", additional_request="no request"):

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_service_date, preferred_service_time, pest_type, affected_areas, first_notice,
             entry_point, previous_treatments, customer_budget, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="pest_control!A1:I1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "check the vendor’s availability. Let them know you’ll get back to them as soon as possible with a "
            "final confirmation.")


def estimate_price_by_pest_type(pest_type):
    price_df = get_service_price_list("Pest Control")

    price = price_df.loc[price_df["Pest Type"] == pest_type, "Price"]

    if price.empty:
        return ("The price list does not include the rate for the pest type you mentioned. "
                "I’ll check with the vendor and update you shortly. Thanks for your patience.")
    else:
        return f"The pest control service charge for {pest_type} is RM {price.iloc[0]}.\n"
