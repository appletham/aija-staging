from service_utils import (
    get_google_creds_and_service,
    get_service_price_list,
)
import os


def save_aircon_cleaning_booking_details(number_of_ac_units, ac_details, preferred_service_date,
                                         preferred_service_time, customer_budget="not mentioned",
                                         additional_request="no request"):
    """
    Saves aircon cleaning booking details to a Google Sheet.

    Args:
        number_of_ac_units (int): The number of air conditioning units to be serviced.
        ac_details (list of dict): A list of dictionaries containing details for each unit.
        preferred_service_date (str): The customer's preferred date for the service (format: DD-MM-YYYY).
        preferred_service_time (str): The customer's preferred time for the service (format: HH:MM AM/PM).
        customer_budget (str, optional): The customer's budget for the service.
        additional_request (str, optional): Any additional requests made by the customer.

    Returns:
        str: A confirmation message for the customer.
    """
    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [""] * 29
    data[0] = preferred_service_date
    data[1] = preferred_service_time
    data[2] = customer_budget
    data[3] = additional_request
    data[4] = number_of_ac_units

    # Iterate through each air conditioning unit's details
    for i, details in enumerate(ac_details, start=0):
        data[5 + (3 * i)] = details.get('cleaning_type', '')
        data[6 + (3 * i)] = details.get('ac_type', '')
        data[7 + (3 * i)] = details.get('horsepower', '')

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="ac_cleaning!A1:AC1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": [data]}).execute()

    return ("Thank you for confirming the details. We will check vendor availability and "
            "get back to you as soon as possible with a final confirmation.")


def estimate_rough_aircon_cleaning_price(ac_type):
    """
    Provides a general price range for aircon cleaning based on the aircon type.

    Args:
        ac_type (str): The type of aircon (e.g., wall-mounted, cassette).

    Returns:
        str: Price range for normal and chemical cleaning.
    """
    price_df = get_service_price_list("Aircon Cleaning")
    reply = ""

    for cleaning_type in ['Normal Cleaning', 'Chemical Cleaning']:
        price = price_df.loc[
            (price_df["Aircon Type"] == ac_type) & (price_df["Cleaning Type"] == cleaning_type), "Price per Unit (RM)"
        ]

        reply += f"{cleaning_type} Price Per Unit: "
        if len(price) == 1:
            reply += f"{price.iloc[0]}\n"
        elif len(price) > 1:
            reply += f"{price.iloc[0].split('-')[0]} to {price.iloc[len(price) - 1].split('-')[1]}\n"

    reply += ("Gas refills will incur an additional charge of RM50 per unit.\n"
              "The cleaning fee is determined by the aircon's horsepower and the selected vendor. "
              "Please note that vendors offering lower rates may have longer waiting times for service.")

    return reply


def estimate_aircon_cleaning_price(ac_type, horsepower, cleaning_type="Normal Cleaning"):
    """
    Provides a specific cleaning price based on aircon type, horsepower, and cleaning type.

    Args:
        ac_type (str): The type of aircon.
        horsepower (float): The aircon's horsepower.
        cleaning_type (str): Type of cleaning (default is "Normal Cleaning").

    Returns:
        str: Detailed price for the requested service.
    """
    price_df = get_service_price_list("Aircon Cleaning")

    filtered_df = price_df.loc[(price_df["Aircon Type"] == ac_type) & (price_df["Cleaning Type"] == cleaning_type) &
                               (price_df["Horsepower"] >= horsepower)]

    if filtered_df.empty:
        return (f"The price list does not include the rate for {horsepower}HP aircon. "
                "I’ll check with the vendor and update you shortly. Thanks for your patience.")

    # Get the minimum "Horsepower" that fulfills the requirement
    min_horsepower = filtered_df["Horsepower"].min()
    filtered_df = filtered_df.loc[filtered_df["Horsepower"] == min_horsepower]

    # Get the cleaning price per unit with the minimum horsepower
    min_cost = filtered_df.loc[filtered_df["Horsepower"] == min_horsepower, "Price per Unit (RM)"]

    reply = ("Here's the breakdown of the cleaning service provided by our vendors:\n"
             f"Cleaning Price per Unit for {horsepower}HP Aircon: {min_cost.iloc[0]}\n"
             "Gas refills will incur an additional charge of RM50 per unit.\n")

    reply += ("Important Note:\n"
              "The cleaning fee varies based on the selected vendor. "
              "Please note that vendors offering lower rates may have longer waiting times for service.")

    return reply


def is_horsepower_unidentified():
    """
    Request customers to upload images or videos of their aircon label.

    Returns:
        str: A message prompting the customer to share media for HP identification.
    """
    return ("Ask customers to send you a picture of the aircon label so you can identify the HP for them. "
            "It's usually located under or beside the aircon. "
            "Kindly ask them to notify you once they have uploaded the video or image.")
