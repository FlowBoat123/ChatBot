import logging
from mindsdb_connector import MindsDBConnector
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet  # Thêm dòng này để import SlotSet

# Đặt mức độ logging
logging.basicConfig(level=logging.INFO)

class ActionPredictWithMindsDB(Action):
    def name(self) -> str:
        return "action_predict"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:

        # # Lấy dữ liệu cần thiết từ tracker
        user_message = tracker.latest_message.get('text')
        user_intent = tracker.latest_message.get('intent')
        print(user_message)
        print(user_intent)
        # # Ghi lại thông tin
        # logging.info(f"Input data: {input_data}")

        # if input_data is None:
        #     dispatcher.utter_message(text="Không có dữ liệu đầu vào.")
        #     return []

        # Kết nối với MindsDB và lấy dự đoán
        connector = MindsDBConnector()
        logging.info("Sending query to MindsDB...")  # Thêm logging trước khi gửi yêu cầu
        prediction = await connector.handle_message("AAPL")
        logging.info(f"Received prediction: {prediction}")  # Ghi lại giá trị trả về

        # Kiểm tra giá trị dự đoán
        if "error" in prediction:
            dispatcher.utter_message(text="Đã xảy ra lỗi khi dự đoán.")
        else:
            dispatcher.utter_message(text=f"Dự đoán của bạn là: {prediction}")
            
        # Gán giá trị cho slot
        # model_response = prediction  # Lấy giá trị dự đoán
        # dispatcher.utter_message(text=f"Dự đoán của bạn là: {model_response}")  # Gửi thông điệp dự đoán

        # return [SlotSet("model_response", model_response)]  # Gán giá trị cho slot
        return []
