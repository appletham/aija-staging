from service_utils import (
    get_google_creds_and_service,
    get_service_price_list
)
import os


def save_laundry_booking_information(laundry_items, preferred_service_date, preferred_service_time,
                                     customer_budget="not mentioned", additional_request="no request"):

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

    # Iterate through each air conditioning unit's details
    for i, details in enumerate(laundry_items, start=0):
        data[4 + (3 * i)] = details.get('laundry_service_type', '')
        data[5 + (3 * i)] = details.get('clothing_type', '')
        data[6 + (3 * i)] = details.get('special_fabrics', '')

    sheet.values().append(spreadsheetId=os.getenv("SAMPLE_SPREADSHEET_ID"),
                          range="laundry!A1:S1",
                          valueInputOption="USER_ENTERED",
                          insertDataOption="INSERT_ROWS",
                          body={"values": [data]}).execute()

    return ("Inform the customer that their booking details have been submitted and that you’ll need some time to "
            "check the vendor’s availability. Let them know you’ll get back to them as soon as possible with a "
            "final confirmation.")


def estimate_price_by_clothing_type(clothing_type):
    if clothing_type == 'Others':
        return ("Since the price list does not include a rate for the clothing type the customer mentioned, "
                "inform them that you will check with the vendor and provide an update shortly.")
    else:
        price_df = get_service_price_list("Laundry")
        price = price_df.loc[price_df["Clothing Type"] == clothing_type, ["Service Type", "Price"]]
        reply = f"Here are the available laundry service options for '{clothing_type}' for customers to choose from:\n"
        for index, row in price.iterrows():
            service_type = row["Service Type"]
            service_price = row["Price"]
            reply += f"{index + 1}. {service_type}: {service_price}\n"

        reply += ("Important Note:\n"
                  "- The ironing service will cost RM3 per piece and will typically take 2-3 days.\n"
                  "- Inform customers that the minimum load for a normal wash is 5kg. If the customer sends less than "
                  "5kg (e.g., 3kg), clarify that the charge will still be based on the 5kg minimum load.\n")
    print(reply)
    return reply

