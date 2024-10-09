from googleapiclient.discovery import build
import streamlit as st
import gspread
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
from openai import OpenAI
import logging
import time
import os
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_google_creds_and_service(service_name=None, version=None):
    """Create Google API credentials and return the appropriate service client."""
    google_sheet_scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    google_sheet_key_dict = json.loads(st.secrets["TEXTKEY"])
    creds = Credentials.from_service_account_info(google_sheet_key_dict, scopes=google_sheet_scopes)

    if service_name and version:
        return build(service_name, version, credentials=creds)
    else:
        sheets_client = gspread.authorize(creds)
        return sheets_client


def get_service_price_list(sheet_name):
    """Fetch data from Google Sheets."""
    folder_id = os.getenv("REPORT_FOLDER_ID")

    sheets_client = get_google_creds_and_service()

    # Open the Google Sheet
    spreadsheet = sheets_client.open(title="Home Services Price List", folder_id=folder_id)
    worksheet = spreadsheet.worksheet(title=sheet_name)

    # Read the existing data from the Google Sheet
    existing_df = get_as_dataframe(worksheet)

    # Drop rows that are completely empty
    existing_df = existing_df.dropna(how='all')

    # Drop columns that are completely empty
    existing_df = existing_df.dropna(axis=1, how='all')

    return existing_df


def check_customer_disagreement_with_price(customer_budget):
    return ("Tell the customer that you will check vendors who can offer services within their budget "
            f"(RM {customer_budget}) and will get back to them soon. At the same time, "
            "continue to gather other necessary information.")


def check_urgent_service_request(preferred_service_date, preferred_service_time):
    return (f"Tell the customer that since their requested service on {preferred_service_date} at "
            f"{preferred_service_time} is outside our usual booking window, you will check with the vendors for their "
            "availability and will get back to them as soon as you have an update. "
            "At the same time, continue to gather all other necessary information from the customer.")


def check_issue_description_complete():
    """
    Request customers to upload images or videos of their issues.

    Returns:
        str: A message prompting the customer to share media for better assessment.
    """
    return ("Ask customers to share the video or photo of their issue, "
            "so you can check with the vendor and assess the issue more effectively. "
            "Kindly ask them to notify you once they have uploaded the video or image. ")


def is_service_policy_question(customer_question):
    try:
        # Initialize the OpenAI client and create a new thread
        client = OpenAI()
        thread = client.beta.threads.create()

        # Prepare the prompt for the assistant
        prompt = (
            f"Please analyze the following customer question: '{customer_question}'. "
            "Determine if it relates to our service policy. If it does, provide a professional response "
            "based on the relevant service policy. If the question is outside the scope of the service policy, "
            "indicate that the query will be passed to our human concierge for further assistance."
        )

        # Send the message to the assistant
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # Start the assistant run and poll for completion
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=os.getenv("SERVICE_POLICY_ASSISTANT_ID")
        )

        # Set maximum iterations and sleep time
        iteration = 0

        # Poll until the run is completed or we reach the max iteration count
        while run.status != "completed" and iteration < 10:
            logging.info(f"Polling iteration {iteration}, current status: {run.status}")
            time.sleep(3)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            iteration += 1

        # Retrieve and return the final message content
        messages = list(client.beta.threads.messages.list(
            thread_id=thread.id,
            run_id=run.id
        ))

        # Check if any messages were returned and extract the content
        if messages and messages[0].content:
            return messages[0].content[0].text.value
        else:
            logging.error("No messages returned or content is missing.")
            return "Error: No response from the assistant."

    except Exception as e:
        logging.error(f"An error occurred while processing the request: {e}")
        raise


def validate_general_service_date(preferred_service_date):
    """
    Validates the customer's preferred service date, ensuring it's at least 2 days from today (excluding Sunday).
    """
    # Convert the preferred service date to the expected format (DD-MMM-YYYY)
    preferred_date = datetime.strptime(preferred_service_date, '%d-%b-%Y')

    # Get today's date
    today = datetime.now().date()

    # Calculate the earliest valid date
    minimum_lead_days = 2
    earliest_valid_date = today + timedelta(days=minimum_lead_days)

    if preferred_date.date() == today:
        return "Politely inform the customer that same-day requests are not accepted."

    if preferred_date.date() < earliest_valid_date:     # Check if the preferred date is within 3 days from today
        return (f"Inform the customer that since their requested service on {preferred_service_date} is outside "
                "our usual booking window, which requires at least 2 days notice, you will try to find "
                "vendors who can accommodate the urgent request, but be sure to avoid making promises.")

    if preferred_date.weekday() == 6:    # Check if the preferred date falls on a Saturday or Sunday
        return (f"Inform the customer that since their requested service on {preferred_service_date} falls "
                "on a Sunday, you will try to find vendors who can accommodate the request, but be sure to "
                "avoid making promises.")

    return ("Inform the customer that you will check with the vendors for their availability and will get back "
            "to them as soon as you have an update. At the same time, continue to gather all other necessary "
            "information from the customer.")
