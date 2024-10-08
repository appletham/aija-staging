import os
import re
import time
import json
import logging
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from function_mapping import function_mapping
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Mapping of home services to their assistant IDs
HOME_SERVICES = {
    "Aircon Cleaning": "AIRCON_CLEANING_ASSISTANT_ID",
    "Aircon Installation": "AIRCON_INSTALLATION_ASSISTANT_ID",
    "Aircon Troubleshooting": "AIRCON_TROUBLESHOOTING_ASSISTANT_ID",
    "Appliance Repair": "APPLIANCE_REPAIR_ASSISTANT_ID",
    "Curtain Making": "CURTAIN_MAKING_ASSISTANT_ID",
    "Electrician & Wiring": "ELECTRICAL_ASSISTANT_ID",
    "Home Cleaning": "HOME_CLEANING_ASSISTANT_ID",
    "Laundry": "LAUNDRY_ASSISTANT_ID",
    "Locksmith": "LOCKSMITH_ASSISTANT_ID",
    "Others": "OTHERS_ASSISTANT_ID",
    "Plumbing": "PLUMBING_ASSISTANT_ID",
    "Pest Control": "PEST_CONTROL_ASSISTANT_ID",
    "Renovation": "RENOVATION_ASSISTANT_ID",
    "Upholstery Cleaning": "UPHOLSTERY_CLEANING_ASSISTANT_ID"
}


class OpenAIClient:
    """
    Client for interacting with OpenAI API to manage service bookings.
    """

    def __init__(self, service_name=""):
        # Initialize the environment and client
        load_dotenv()

        # Fetch assistant_id based on service name
        self.assistant_id = os.getenv(HOME_SERVICES.get(service_name))

        # Handle the case where no valid assistant ID is found
        if not self.assistant_id:
            logging.error("Invalid assistant key for service: %s", service_name)
            raise ValueError("Invalid assistant key.")

        # Initialize the OpenAI client
        self.client = OpenAI()

        # Create a thread
        self.thread_number = self.create_thread()
        print(self.thread_number)

    def create_thread(self):
        """
        Create a new conversation thread for interacting with OpenAI API.
        """
        try:
            thread = self.client.beta.threads.create()
            logging.info("Conversation thread created successfully.")
            return thread.id
        except Exception as e:
            logging.error("Failed to create a conversation thread: %s", e)
            raise

    def create_message(self, message, role="user"):
        """
        Create a message in the OpenAI conversation thread.
        """
        try:
            self.client.beta.threads.messages.create(
                thread_id=self.thread_number,
                role=role,
                content=message,
            )
            logging.info("Message created successfully in the thread.")
        except Exception as e:
            logging.error("Failed to create a message: %s", e)
            raise

    def update_assistant_instructions(self, service_name):
        """
        Update assistant instructions with the current date and earliest available date.
        """
        try:
            assistant = self.get_assistant()
            today = datetime.now()
            today_date_str = today.strftime("%d-%b-%Y")
            today_day_of_week = today.strftime("%A")

            # Extract dates from instructions
            pattern = r'\b\d{2}-[A-Za-z]{3}-\d{4}\b'
            matches = re.findall(pattern, assistant.instructions)
            if len(matches) == 2 and matches[0] != today_date_str:
                self._update_instructions_dates(assistant, service_name, matches, today_date_str, today_day_of_week)
        except Exception as e:
            logging.error("Failed to update assistant instructions: %s", e)

    def _update_instructions_dates(self, assistant, service_name, matches, today_date_str, today_day_of_week):
        """
        Helper function to update the assistant's instructions with new dates.
        """
        old_date = pd.to_datetime(matches[0], format="%d-%b-%Y")
        old_date_str = old_date.strftime("%d-%b-%Y")
        old_day_of_week = old_date.day_name()

        old_earliest_available_date = pd.to_datetime(matches[1], format="%d-%b-%Y")
        old_earliest_available_date_str = old_earliest_available_date.strftime("%d-%b-%Y")
        old_earliest_available_day_of_week = old_earliest_available_date.day_name()

        # Calculate the new earliest available date
        if service_name in ['Home Cleaning', 'Others']:
            # Exclude weekends
            working_date_range = pd.date_range(start=pd.Timestamp.now().date(), periods=4, freq='B')
            if working_date_range[0].date() == pd.Timestamp.now().date():
                new_earliest_available_date = working_date_range[3]
            else:
                new_earliest_available_date = working_date_range[2]
        else:
            date_range = pd.date_range(start=pd.Timestamp.now().date(), periods=4, freq='D')
            # Exclude Sunday
            working_date_range = [d for d in date_range if d.weekday() != 6]
            if working_date_range[0].date() == pd.Timestamp.now().date():
                new_earliest_available_date = working_date_range[2]
            else:
                new_earliest_available_date = working_date_range[1]

        new_earliest_available_date_str = new_earliest_available_date.strftime("%d-%b-%Y")
        new_earliest_available_day_of_week = new_earliest_available_date.day_name()

        try:
            self.client.beta.assistants.update(
                assistant_id=self.assistant_id,
                instructions=assistant.instructions.replace(
                    f"{old_day_of_week}, {old_date_str}",
                    f"{today_day_of_week}, {today_date_str}"
                ).replace(
                    f"{old_earliest_available_date_str} ({old_earliest_available_day_of_week})",
                    f"{new_earliest_available_date_str} ({new_earliest_available_day_of_week})"
                )
            )
            logging.info("Assistant instructions updated successfully.")
        except Exception as e:
            logging.error("Failed to update assistant instructions: %s", e)
            raise

    def get_assistant(self):
        """
        Retrieve the assistant object for further interactions.
        """
        try:
            return self.client.beta.assistants.retrieve(assistant_id=self.assistant_id)
        except Exception as e:
            logging.error("Failed to retrieve assistant: %s", e)
            raise

    def get_response_without_streaming(self, prompt):
        """
        Get a response from OpenAI API without streaming.
        """
        try:
            max_iterations = 10  # Set your desired maximum iterations
            iteration = 0
            chk_response = self.client.moderations.create(input=prompt)
            output = chk_response.results[0]

            if output.flagged:
                logging.warning("Prompt flagged as harmful content.")
                return "Harmful content."

            self.create_message(prompt)
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread_number,
                assistant_id=self.assistant_id
            )

            while run.status != "completed" and iteration < max_iterations:
                run = self._handle_run_status(run)
                iteration += 1

            return self._get_final_message_content(run)

        except Exception as e:
            logging.error("Failed to get response: %s", e)
            return "Error getting response."

    def _handle_run_status(self, run):
        """
        Handle the run status during interaction with the OpenAI API.
        """
        if run.status == "requires_action":
            tool_outputs = self._process_required_actions(run)
            if tool_outputs:
                try:
                    run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=self.thread_number,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    logging.info("Tool outputs submitted successfully.")
                except Exception as e:
                    logging.error("Failed to submit tool outputs: %s", e)
                    raise
        else:
            time.sleep(3)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_number,
                run_id=run.id
            )
        return run

    def _process_required_actions(self, run):
        """
        Process required actions based on tools needed during the conversation.
        """
        tool_outputs = []
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name in function_mapping:
                func = function_mapping.get(tool.function.name)
                if func:
                    try:
                        tool_response = func(**json.loads(tool.function.arguments))
                        tool_outputs.append({"tool_call_id": tool.id, "output": tool_response})
                        logging.info("Calling function %s with arguments: %s", tool.function.name,
                                     tool.function.arguments)
                    except Exception as e:
                        logging.error("Failed to execute function %s: %s", tool.function.name, e)
        return tool_outputs

    def _get_final_message_content(self, run):
        """
        Retrieve the final message content after completing the API interaction.
        """
        try:
            messages = list(self.client.beta.threads.messages.list(
                thread_id=self.thread_number,
                run_id=run.id
            ))
            return messages[0].content[0].text.value
        except Exception as e:
            logging.error("Failed to retrieve final message content: %s", e)
            raise
