from service_utils import get_google_creds_and_service
import os


def save_locksmith_booking_details(service_description, service_type, service_address, preferred_service_date,
                                   preferred_service_time, customer_budget="Not mentioned",
                                   additional_request="No request"):

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[service_address, preferred_service_date, preferred_service_time, service_type, service_description,
             customer_budget, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="locksmith!A1:G1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "check the vendor’s availability. Let them know you’ll get back to them as soon as possible with a "
            "final confirmation.")


def check_service_description_complete():
    """
    Request customers to upload images or videos of their issues.

    Returns:
        str: A message prompting the customer to share media for better assessment.
    """
    return ("Ask customers to share the video or photo of their door knob or lock, "
            "so you can check with the vendor and assess the issue more effectively. "
            "Kindly ask them to notify you once they have uploaded the video or image. ")


def check_urgent_locksmith_service_request(preferred_service_date):
    return (f"Tell the customer that since their requested service on {preferred_service_date} "
            f"is outside our usual booking window, you will check with the vendors for their "
            "availability and will get back to them as soon as you have an update. "
            "At the same time, make sure the customer reviews and confirms that the booking details are correct, "
            "then save the booking using the 'save_locksmith_booking_details' function.")
