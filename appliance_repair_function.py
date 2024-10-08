from service_utils import (
    get_google_creds_and_service,
    get_service_price_list
)
import os


def save_appliance_repair_booking_details(appliance_type, issue_description, appliance_functionality,
                                          preferred_site_inspection_date, preferred_site_inspection_time,
                                          appliance_brand="Unknown", warranty_status="Unknown",
                                          recent_power_issues="Unknown", customer_budget="Not mentioned",
                                          additional_request="No request"):

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_site_inspection_date, preferred_site_inspection_time, appliance_type,
             appliance_brand, issue_description, appliance_functionality, warranty_status, recent_power_issues,
             customer_budget, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="appliance_repair!A1:J1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "check the vendor’s availability. Let them know you’ll get back to them as soon as possible with a "
            "final confirmation.")


def determine_site_inspection_fees(appliance_type):
    """
    Determines the site inspection fees based on the appliance type.

    Args:
        appliance_type (str): The type of appliance that requires inspection.

    Returns:
        str: A message informing the customer of the inspection charges and outlining the next steps.
    """
    price_df = get_service_price_list("Appliance Repair")
    charge = price_df.loc[
        price_df["Appliance Type"] == appliance_type, "Site Inspection/Troubleshooting Charges"
    ].iloc[0]

    if appliance_type.lower() in ["washing machine", "clothes dryer", "refrigerator"]:
        message = (f"Recommend a site inspection to the customer to assess the issue, with a charge of RM {charge}. "
                   "Explain that during the inspection, the vendor will provide the repair charges on the spot.\n\n"
                   "Additionally, mention that the site inspection fee is non-refundable, regardless of whether the "
                   "issue is resolved, as it covers the cost of the inspection and transportation.\n\n"
                   "Ask the customer to confirm if they agree with the price, so the service can be scheduled at "
                   "their convenience. Remind them to reach out if they have any questions or concerns.")
    elif appliance_type.lower() in ["water heater", "water boiler"]:
        message = (f"Recommend a site inspection to the customer to assess the issue, with a charge of RM {charge}. "
                   "During the inspection, the vendor will provide the repair charges on the spot.\n\nAsk the customer "
                   "to confirm if they agree with the price so the service can be scheduled. Remind them to reach "
                   "out if they have any questions or concerns.")
    elif appliance_type.lower() == "television":
        message = (f"Inform customers that the vendor will charge RM {charge} to pick up the TV and take it to their "
                   "facility for inspection, a process that usually takes about a week. Once the inspection is "
                   "complete, the vendor will provide the repair charges.\n\nInstruct the AI to inform the customer "
                   "that, if they agree with the repair charges, the payment will be collected, and the vendor will "
                   "proceed with the repair. However, if the customer chooses not to repair the TV, the "
                   f"RM {charge} fee for pickup and inspection will not be refunded.\n\nAsk the customer to confirm "
                   "if they agree with this arrangement, so the service can be scheduled. Also, remind them to "
                   "reach out if they have any questions or concerns.")
    else:
        message = ("Inform customers that, we will need to determine if any of our vendors "
                   "are capable of repairing the appliance. Please be advised that this process may take longer "
                   "than usual to get their reply, which may delay our response time.\n\nApologize for any "
                   "inconvenience this may cause and appreciate their understanding. Assure them that we will make "
                   "every effort to provide a prompt response as soon as we receive information from the vendor.")

    return message
