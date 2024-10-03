from mindsdb_connector import MindsDBConnector
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionPredictWithMindsDB(Action):
    def name(self) -> str:
        return "action_predict_with_mindsdb"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        # Lấy dữ liệu cần thiết từ tracker
        input_data = tracker.get_slot("your_slot_name")

        # Kết nối với MindsDB và lấy dự đoán
        prediction = MindsDBConnector(self.model_name).process_message({"text": input_data})

        # Gửi kết quả dự đoán đến người dùng
        dispatcher.utter_message(text=f"Dự đoán của bạn là: {prediction}")

        return []
