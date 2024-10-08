from service_utils import (
    get_google_creds_and_service,
    get_service_price_list
)
import os


def save_electrical_booking_information(service_address, preferred_service_date, preferred_service_time, service_type,
                                        issue_description, appliance_or_fixture, property_type,
                                        customer_budget="not mentioned", additional_request="no request"):
    """
        Saves the confirmed booking information for an electrical service to a Google Sheet.

        Args:
            service_address (str): The address where the electrical service will be conducted.
            preferred_service_date (str): The preferred date for the service, formatted as DD-MMM-YYYY.
            preferred_service_time (str): The preferred time for the service, formatted as HH:MM XM.
            service_type (str): The type of electrical service (e.g., installation, repair, replacement).
            issue_description (str): A brief description of the electrical issue or request.
            appliance_or_fixture (str): The specific appliance or fixture that requires installation, replacement, or repair.
            property_type (str): The type of property (e.g., residential, commercial).
            customer_budget (str, optional): The customer's budget for the service.
            additional_request (str, optional): Any additional customer requests regarding the service.

        Returns:
            str: A confirmation message indicating that the details have been saved and the vendor availability will be checked.
    """
    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_service_date, preferred_service_time, service_type, issue_description,
             appliance_or_fixture, property_type, customer_budget, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="electrician!A1:H1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "confirm the vendor's availability and service price. Assure them you’ll follow up as soon as possible "
            "with a final confirmation.")


def estimate_price_by_electrical_service_type(service_type="Other"):
    if service_type == "Bulbs Replacement":
        return "Price for Bulbs Replacement: minimum 2 bulbs (RM120) + each additional bulb (RM30)"
    else:
        return (f"Let the customers know that you'll need to check with the vendors first to provide an accurate price."
                "If the issue cannot be diagnosed online, we will recommend a troubleshooting session, "
                "which will cost RM150. After evaluating the situation, the vendors will offer a detailed quote "
                "for the repair. Ask if they are comfortable proceeding with this process.")


def check_electrical_issue_description_complete():
    """
    Request customers to upload images or videos of their issues.

    Returns:
        str: A message prompting the customer to share media for better assessment.
    """
    return ("Ask customers to provide a video or photo of the issue or the location where the installation service "
            "is needed to help the vendor assess it more effectively and provide an accurate price quote. "
            "Kindly ask them to notify you once they have uploaded the video or image. ")

