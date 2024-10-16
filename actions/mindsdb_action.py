import logging
import random
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

def replace_braces(text):
    return text.replace('{', '(').replace('}', ')')

def create_nlu_file(data):
    with open('data/nlu.yml', 'w', encoding='utf-8') as nlu_file:
        nlu_file.write("version: '3.1'")
        nlu_file.write("\n\nnlu:")
        i = 0
        while i < len(data):
            # print(data[i])
            intent = data[i][1] if data[i][1] is not None else data[i][0]
            nlu_file.write(f"\n\n- intent: {intent}\n  examples: |")
            while i < len(data) and (data[i][0] == intent or data[i][1] == intent):
                example = data[i][2]  # Lấy example
                nlu_file.write(f"\n    - {replace_braces(example)}")
                i += 1
        
        #lệnh test lấy dữ liệu mindsDB
        nlu_file.write("\n\n- intent: lấy dữ liệu\n  examples: |\n    - Lấy dữ liệu từ mindsDB")
        #

def create_nlu_test_file(data):
    with open('tests/nlu_test.yml', 'w', encoding='utf-8') as nlu_file:
        nlu_file.write("version: '3.1'")
        nlu_file.write("\n\nnlu:")
        i = 0
        while i < len(data):
            # print(data[i])
            intent = data[i][1] if data[i][1] is not None else data[i][0]
            nlu_file.write(f"\n\n- intent: {intent}\n  examples: |")
            while i < len(data) and (data[i][0] == intent or data[i][1] == intent):
                example = data[i][2]  # Lấy example
                nlu_file.write(f"\n    - {replace_braces(example)}")
                i += 1

def create_domain_file(data):
    with open('domain.yml', 'w', encoding='utf-8') as domain_file:
        domain_file.write("version: '3.1'")
        domain_file.write("\n\nintents:")
        for intent in data['intent']:
            domain_file.write(f"\n  - {intent}")

        #lệnh test lấy dữ liệu mindsDB
        domain_file.write(f"\n  - lấy dữ liệu")
        #

        domain_file.write("\n\nentities:")
        for entity in data['entities']:
            domain_file.write(f"\n  - {entity}")

        domain_file.write('\n\nactions:')
        domain_file.write("\n  - action_return_intent_and_entity")
        
        #lệnh test lấy dữ liệu mindsDB
        domain_file.write("\n  - action_get_data_from_mindsDB")
        #

        domain_file.write("\n\nsession_config:\n  session_expiration_time: 60\n  carry_over_slots_to_new_session: true")

def create_stories_file(intents):
    with open('data/stories.yml', 'w', encoding='utf-8') as stories_file:
        # stories_file.write(f"\n- story: {data['story_name']}\n")
        # stories_file.write(f"  steps:\n    - intent: {data['intent']}\n")
        stories_file.write("version: '3.1'")
        stories_file.write("\n\nstories:")

        for intent in intents:
            stories_file.write(f"\n- story: {intent}")
            stories_file.write(f"\n  steps:\n    - intent: {intent}")
            stories_file.write("\n    - action: action_return_intent_and_entity\n")

        #lệnh test lấy dữ liệu mindsDB
        stories_file.write("\n- story: lấy dữ liệu từ mindsDB\n  steps:\n    - intent: lấy dữ liệu\n    - action: action_get_data_from_mindsDB")
        #

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

def split_data(data, prob):
    """split data into fractions [prob, 1 - prob]"""
    results = [], []
    i = 0
    while i < len(data):
        # print(data[i])
        intent = data[i][1] if data[i][1] is not None else data[i][0]
        while i < len(data) and (data[i][0] == intent or data[i][1] == intent):
            if random.random() < prob:
                results[0].append(data[i])  # Thêm toàn bộ intent vào tập train
            else:
                results[1].append(data[i])  # Thêm toàn bộ intent vào tập test
            i += 1
    return results

class ActionGetDataFromMindsDB(Action):
    def name(self) -> str:
        return "action_get_data_from_mindsDB"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:

        # # Lấy dữ liệu cần thiết từ tracker
        user_message = tracker.latest_message.get('text')
        user_intent = tracker.latest_message.get('intent')
        print(user_message)
        print(user_intent)

        # Kết nối với MindsDB và lấy dự đoán
        connector = MindsDBConnector()
        logging.info("Sending query to MindsDB...")  # Thêm logging trước khi gửi yêu cầu
        query = "SELECT * FROM files.chatbot_data;"
        result = await connector.handle_message(query)
        # logging.info(f"Received prediction: {result}")  # Ghi lại giá trị trả về

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

        train_data, test_data = split_data(result['data'], 0.8)

        create_nlu_file(train_data)
        create_nlu_test_file(test_data)
        create_domain_file({"intent": intents, "entities": entities })
        create_stories_file(intents)

        # Kiểm tra giá trị dự đoán
        if "error" in result:
            dispatcher.utter_message(text="Đã xảy ra lỗi khi lấy dữ liệu.")
        else:
            dispatcher.utter_message(text=f"Quá trình lấy dữ liệu đã hoàn tất")
            
        # Gán giá trị cho slot
        # model_response = prediction  # Lấy giá trị dự đoán
        # dispatcher.utter_message(text=f"Dự đoán của bạn là: {model_response}")  # Gửi thông điệp dự đoán

        # return [SlotSet("model_response", model_response)]  # Gán giá trị cho slot
        return []
