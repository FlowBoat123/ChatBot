import logging
from mindsdb_connector import MindsDBConnector
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet  # Thêm dòng này để import SlotSet
import re
import difflib

# Đặt mức độ logging
logging.basicConfig(level=logging.INFO)

# Hàm để định dạng lại câu
def format_input(input_str, replacements):
    for key, value in replacements.items():
        input_str = input_str.replace(key, f"[{value}]({key[1:-1]})")
    return input_str

def create_nlu_file(data):
    # with open('data/nlu.yml', 'a', encoding='utf-8') as nlu_file:
    #     nlu_file.write(f"- intent: {data['intent']}\n")
    #     nlu_file.write(f"  examples: |\n    - {data['example']}\n")
    print('nlu.yml')
    print("version: '3.1'\nnlu:")
    i = 0
    while i < len(data):
        # print(data[i])
        intent = data[i][1] if data[i][1] is not None else data[i][0]
        print(f"- intent: {intent}\n  examples: |")
        while i < len(data) and (data[i][0] == intent or data[i][1] == intent):
            example1 = data[i][2]  # Lấy example
            example2 = data[i][3]
            print(example1, example2)
            if example2 is not None:
                # print(example1, example2)
                diff = difflib.ndiff(example1.split(' '), example2.split(' '))
                # Lấy ra các điểm khác nhau
                differences = [word for word in diff if word.startswith('+ ') or word.startswith('- ')]
                print("Điểm khác nhau giữa hai chuỗi:")
                for difference in differences:
                    print(difference)
            else:
                print(f"    - {example1}")
            i += 1

def create_domain_file(data):
    # with open('domain.yml', 'a', encoding='utf-8') as domain_file:
    #     domain_file.write(f"\nintents:\n  - {data['intent']}\n")
    print('domain.yml')
    # print(f"version: '3.1'\nintents:")
    # for intent in data['intent']:
    #     print(f"- {intent}")

    # print("\nentities:")
    # for entity in data['entities']:
    #     print(f"- {entity}")
    # print('\nactions:')
    # print(" - action_return_intent_and_entity")

def create_stories_file(data):
    # with open('data/stories.yml', 'a', encoding='utf-8') as stories_file:
    #     stories_file.write(f"\n- story: {data['story_name']}\n")
    #     stories_file.write(f"  steps:\n    - intent: {data['intent']}\n")
    print('stories.yml')
    print(f"version: '3.1'\nstories:")

    # print(f"\n- story: {data['story_name']}\n")
    # print(f"  steps:\n    - intent: {data['intent']}\n")

def extract_entities(text):
    # Kiểm tra nếu text là None hoặc không phải là chuỗi
    if text is None:
        return []
    
    # Kiểm tra nếu text chứa dấu '{' và '}'
    if '{' in text and '}' in text:
        entities = re.findall(r'\{(.*?)\}', text)
        return entities
    else:
        # Nếu không có dấu '{' và '}', trả về danh sách rỗng
        return []

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
        query = "SELECT * FROM files.chatbot_data;"
        result = await connector.handle_message(query)
        logging.info(f"Received prediction: {result}")  # Ghi lại giá trị trả về

        # Lấy chỉ số của các cột
        intent_index = result['column_names'].index('Intent')
        chi_tiet_hon_index = result['column_names'].index('Chi tiết hơn')

        # Lấy dữ liệu từ cột Intent hoặc Chi tiết hơn
        intents = list(set(
            row[chi_tiet_hon_index] if row[chi_tiet_hon_index] is not None else row[intent_index]
            for row in result['data']
        ))

        cau_hoi_index = result['column_names'].index('Câu hỏi')
        cau_hoi = list(set(row[cau_hoi_index] for row in result['data']))
        entities = set(entity for question in cau_hoi for entity in extract_entities(question))
        # entities = []

        print("ok")
        create_nlu_file(result['data'])
        create_domain_file({"intent": intents, "entities": entities })
        create_stories_file({"intent": intents, "story_name": cau_hoi})

        # Kiểm tra giá trị dự đoán
        if "error" in result:
            dispatcher.utter_message(text="Đã xảy ra lỗi khi dự đoán.")
        else:
            dispatcher.utter_message(text=f"Dự đoán của bạn là: done")
            
        # Gán giá trị cho slot
        # model_response = prediction  # Lấy giá trị dự đoán
        # dispatcher.utter_message(text=f"Dự đoán của bạn là: {model_response}")  # Gửi thông điệp dự đoán

        # return [SlotSet("model_response", model_response)]  # Gán giá trị cho slot
        return []
