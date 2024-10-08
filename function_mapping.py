# function_mapping.py

from aircon_cleaning_function import (
    save_aircon_cleaning_booking_details,
    estimate_aircon_cleaning_price,
    estimate_rough_aircon_cleaning_price,
    is_horsepower_unidentified
)
from aircon_installation_function import (
    save_aircon_installation_booking_details,
    estimate_aircon_installation_price
)
from aircon_troubleshooting_function import (
    save_ac_troubleshooting_booking_details
)
from appliance_repair_function import (
    save_appliance_repair_booking_details,
    determine_site_inspection_fees
)
from curtain_making_function import (
    save_curtain_making_booking_information,
    is_curtain_type_selected
)
from electrical_function import (
    save_electrical_booking_information,
    check_electrical_issue_description_complete,
    estimate_price_by_electrical_service_type
)
from home_cleaning_function import (
    save_home_cleaning_booking_information,
    estimate_rough_price,
    estimate_price_by_size_and_type,
    validate_service_date
)
from laundry_function import (
    save_laundry_booking_information,
    estimate_price_by_clothing_type
)
from locksmith_function import (
    save_locksmith_booking_details,
    check_service_description_complete,
    check_urgent_locksmith_service_request
)
from other_function import (
    save_other_service_booking_information,
    validate_other_service_date
)
from pest_control_function import (
    save_pest_control_booking_information,
    estimate_price_by_pest_type
)
from plumbing_function import (
    save_plumbing_booking_information
)
from renovation_function import (
    save_renovation_booking_information,
    validate_renovation_service_date
)
from upholstery_cleaning_function import (
    save_upholstery_cleaning_booking_information,
    check_upholstery_description_complete
)
from service_utils import (
    check_customer_disagreement_with_price,
    check_urgent_service_request,
    check_issue_description_complete,
    is_service_policy_question,
    validate_general_service_date
)

# Define the function mappings
function_mapping = {
    "save_home_cleaning_booking_information": save_home_cleaning_booking_information,
    "estimate_rough_price": estimate_rough_price,
    "estimate_price_by_size_and_type": estimate_price_by_size_and_type,
    "validate_general_service_date": validate_general_service_date,
    "check_urgent_service_request": check_urgent_service_request,
    "check_customer_disagreement_with_price": check_customer_disagreement_with_price,
    "save_plumbing_booking_information": save_plumbing_booking_information,
    "check_issue_description_complete": check_issue_description_complete,
    "save_electrical_booking_information": save_electrical_booking_information,
    "check_electrical_issue_description_complete": check_electrical_issue_description_complete,
    "estimate_price_by_electrical_service_type": estimate_price_by_electrical_service_type,
    "save_aircon_cleaning_booking_details": save_aircon_cleaning_booking_details,
    "estimate_aircon_cleaning_price": estimate_aircon_cleaning_price,
    "estimate_rough_aircon_cleaning_price": estimate_rough_aircon_cleaning_price,
    "is_horsepower_unidentified": is_horsepower_unidentified,
    "save_ac_troubleshooting_booking_details": save_ac_troubleshooting_booking_details,
    "save_aircon_installation_booking_details": save_aircon_installation_booking_details,
    "estimate_aircon_installation_price": estimate_aircon_installation_price,
    "save_appliance_repair_booking_details": save_appliance_repair_booking_details,
    "determine_site_inspection_fees": determine_site_inspection_fees,
    "save_locksmith_booking_details": save_locksmith_booking_details,
    "check_service_description_complete": check_service_description_complete,
    "check_urgent_locksmith_service_request": check_urgent_locksmith_service_request,
    "save_pest_control_booking_information": save_pest_control_booking_information,
    "estimate_price_by_pest_type": estimate_price_by_pest_type,
    "save_laundry_booking_information": save_laundry_booking_information,
    "estimate_price_by_clothing_type": estimate_price_by_clothing_type,
    "save_other_service_booking_information": save_other_service_booking_information,
    "validate_other_service_date": validate_other_service_date,
    "save_curtain_making_booking_information": save_curtain_making_booking_information,
    "is_curtain_type_selected": is_curtain_type_selected,
    "save_renovation_booking_information": save_renovation_booking_information,
    "validate_renovation_service_date": validate_renovation_service_date,
    "save_upholstery_cleaning_booking_information": save_upholstery_cleaning_booking_information,
    "check_upholstery_description_complete": check_upholstery_description_complete,
    "validate_service_date": validate_service_date,
    "is_service_policy_question": is_service_policy_question
}