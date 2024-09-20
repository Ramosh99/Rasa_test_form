from typing import Any, Text, Dict, List
import csv
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher

ALLOWED_PERIODS = ["monthly", "weekly"]
ALLOWED_MEALPLANS = ["one", "two", "three", "1", "2", "3"]

class ActionSayName(Action):
    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("full_name")
        if not name:
            dispatcher.utter_message(text="I see you haven't provided your name. GoodCal specialises in meal plans (weekly and monthly).")
        else:
            dispatcher.utter_message(text=f"Nice to meet you {name}, GoodCal specialises in meal plans (weekly and monthly).")
        return []

class ValidateRegistrationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_registration_form"

    def validate_type_plan(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validate type_plan value."""
        if slot_value.lower() not in ALLOWED_PERIODS:
            dispatcher.utter_message(text="We only accept weekly or monthly subscriptions")
            return {"type_plan": None}
        dispatcher.utter_message(text=f"Ok, I've registered you as a {slot_value} client")
        return {"type_plan": slot_value.lower()}

    def validate_quantity_meals(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validate quantity_meals value."""
        if slot_value.lower() not in ALLOWED_MEALPLANS:
            dispatcher.utter_message(text="We only accept one, two, or three meal plan subscriptions")
            return {"quantity_meals": None}
        dispatcher.utter_message(text=f"Ok, You have been registered for a {slot_value} meal plan")
        return {"quantity_meals": slot_value.lower()}

class SaveToCSV(Action):
    def name(self) -> Text:
        return "action_save_to_csv"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        full_name = tracker.get_slot("full_name")
        contact_number = tracker.get_slot("contact_number")
        type_plan = tracker.get_slot("type_plan")
        quantity_meals = tracker.get_slot("quantity_meals")

        with open('user_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([full_name, contact_number, type_plan, quantity_meals])

        dispatcher.utter_message(text="Your information has been saved.")
        return []