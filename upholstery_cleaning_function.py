from service_utils import (
    get_google_creds_and_service
)
import os


def save_upholstery_cleaning_booking_information(upholstery_type, upholstery_material, upholstery_condition,
                                                 preferred_service_date, preferred_service_time,
                                                 customer_budget="not mentioned", additional_request="not mentioned"):

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_service_date, preferred_service_time, upholstery_type, upholstery_material,
             upholstery_condition, customer_budget, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="upholstery_cleaning!A1:G1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "confirm pricing with vendors and check their availability for the requested service date. "
            "Let them know you’ll get back to them as soon as possible with a final confirmation.")


def check_upholstery_description_complete():
    return ("Ask customers to share the video or photo of their upholstery, "
            "so you can check with the vendor and assess the issue more effectively. "
            "Kindly ask them to notify you once they have uploaded the video or image.")

