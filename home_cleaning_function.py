from service_utils import (
    get_google_creds_and_service,
    get_service_price_list
)
import os
from datetime import datetime, timedelta


def save_home_cleaning_booking_information(property_type, property_size, cleaning_type, preferred_service_date,
                                           preferred_service_time, customer_budget="not mentioned",
                                           additional_request="no request"):

    # Build the Google Sheets API service using the authenticated credentials
    service = get_google_creds_and_service(service_name='sheets', version='v4')

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Insert a new row into the Google Sheet
    data = [[preferred_service_date, preferred_service_time, cleaning_type, property_type,
             property_size, customer_budget, additional_request]]

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="home_cleaning!A1:G1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": data}).execute()

    return ("Thank you for confirming the details. We will check vendor availability and "
            "get back to you as soon as possible with a final confirmation.")


def validate_service_date(preferred_service_date):
    """
    Validates the customer's preferred service date, ensuring it's at least 3 working days from today.
    """
    # Convert the preferred service date to the expected format (DD-MMM-YYYY)
    preferred_date = datetime.strptime(preferred_service_date, '%d-%b-%Y')

    # Get today's date
    today = datetime.now().date()

    # Calculate the earliest valid date
    minimum_lead_days = 3
    earliest_valid_date = today + timedelta(days=minimum_lead_days)

    if preferred_date.date() == today:
        return "Politely inform the customer that same-day requests are not accepted."

    if preferred_date.date() < earliest_valid_date:     # Check if the preferred date is within 3 days from today
        return (f"Inform the customer that since their requested service on {preferred_service_date} is outside "
                "our usual booking window, which requires at least 3 working days' notice, you will try to find "
                "vendors who can accommodate the urgent request, but be sure to avoid making promises.")

    if preferred_date.weekday() in [5, 6]:    # Check if the preferred date falls on a Saturday or Sunday
        return (f"Inform the customer that since their requested service on {preferred_service_date} falls "
                "on a weekend, you will try to find vendors who can accommodate the request, but be sure to "
                "avoid making promises.")

    return ("The date is valid. Inform the customer that you will check with the vendors for their availability "
            "and will get back to them as soon as you have an update. At the same time, continue to gather all "
            "other necessary information from the customer.")


def estimate_rough_price():
    price_df = get_service_price_list("Home Cleaning")
    reply = ""

    for cleaning_type in ['Basic Cleaning', 'Deep Cleaning', 'Post-Renovation']:
        price = price_df.loc[price_df["Cleaning Type"] == cleaning_type, "Total Cost"]

        reply += f"{cleaning_type}: "
        if cleaning_type == "Post-Renovation":
            if len(price) == 1:
                reply += f"{price.iloc[0]}\n"
            elif len(price) > 1:
                reply += f"{price.iloc[0]} - {price.iloc[len(price) - 1]}\n"
        else:
            if len(price) == 1:
                reply += f"{price.iloc[0]}\n"
            elif len(price) > 1:
                reply += f"{price.iloc[0].split('-')[0]} to {price.iloc[len(price) - 1].split('-')[1]}\n"

    reply += "The exact cleaning fee varies depending on the size of customer's property and their home location."
    return reply


def estimate_price_by_size_and_type(property_size, cleaning_type="Basic Cleaning"):
    price_df = get_service_price_list("Home Cleaning")

    filtered_df = price_df.loc[(price_df["Cleaning Type"] == cleaning_type) &
                               (price_df["Property Size"] >= property_size)]

    if filtered_df.empty:
        return ("The price list does not include the rate for the property size you mentioned. "
                "I’ll check with the vendor and update you shortly. Thanks for your patience.")

    # Get the minimum "Property Size" that fulfills the requirement
    min_property_size = filtered_df["Property Size"].min()
    filtered_df = filtered_df.loc[filtered_df["Property Size"] == min_property_size]

    # Get min and max "Manpower Cost" and corresponding "Number of workers"
    # min_cost, max_cost = filtered_df["Manpower Cost"].agg(['min', 'max'])
    min_cost, min_workers = filtered_df.loc[filtered_df["Manpower Cost"].idxmin(), ["Total Cost", "Manpower"]]
    max_cost, max_workers = filtered_df.loc[filtered_df["Manpower Cost"].idxmax(), ["Total Cost", "Manpower"]]

    reply = "Here's the breakdown of the cleaning service provided by one of our popular vendors:\n"

    if min_cost == max_cost:
        reply += f"Cleaning Fees: {min_cost} ({min_workers})\n"
    else:
        reply += f"Cleaning Fees: {min_cost} ({min_workers}) or {max_cost} ({max_workers})\n"

    reply += "Important Note:\n"
    reply += "- The exact cleaning fees may vary depending on the size of your property and your home location.\n"
    reply += "- If you require a ladder, an additional charge of RM 50 will be incurred.\n"

    if cleaning_type == "Basic Cleaning":
        reply += ("- Cleaning tools required extra charges RM 40 (include Floor Cleaner, Toilet Bowl Cleaner, "
                  "Glass Cleaner and Bleach / Clorox + Vacuum / Broom, Trash Bag, Cloth and Toilet Brush)")
    else:
        reply += "Cleaning tools are included."

    return reply
