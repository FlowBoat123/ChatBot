# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import logging 
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

stock_symbol_db = {"CEO", "SSI", "VNM", "VCB", "VIC", "SKD", "TOI"}

class FindStockNews(Action):

    def name(self) -> Text:
        return "action_find_stock_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Đây là tin tức ngày hôm nay: VNINDEX 1.283,04")
        dispatcher.utter_message(text="Bạn có muốn biết thông tin cụ thể về mã chứng khoán nào không?")

        return []
    
class FindStocDetails(Action):

    def name(self) -> Text:
        return "action_find_stock_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_symbol = next(tracker.get_latest_entity_values('stock_symbol'), None) 
        if stock_symbol:
            dispatcher.utter_message(text=f"You have selected {stock_symbol} as your stock choice")
            dispatcher.utter_message(text=f"{stock_symbol} mở cửa 15.800 cao nhất 15.900 thấp nhất 15.700")
        else:
            dispatcher.utter_message(text="Im sorry, I could not detect the stock choice")

        return []

class ExtractStockEnity(Action):

    def name(self) -> Text:
        return "action_extract_stock_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_symbol = next(tracker.get_latest_entity_values('stock_symbol'), None) 
        amount = next(tracker.get_latest_entity_values('amount'), None) 

        if stock_symbol:
            dispatcher.utter_message(text=f"Hãy xác nhận mua {amount} cổ phiếu {stock_symbol}")
            print(f"Current amount: {amount}")
            print(f"Current stock: {stock_symbol}")
            return [SlotSet("stock_symbol", stock_symbol), SlotSet("amount", amount)]
            
        else:
            dispatcher.utter_message(text="Xin lỗi, tôi không thể xác định được cổ phiếu mà bạn định mua, hãy kiểm tra lại tên cô phiếu của bạn.")
        
        return []

class ConfirmPlaceStockOrder(Action):
    def name(self) -> Text:
        return "action_confirm_order_2"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Ensure current_stocks is initialized
        current_stocks = []  # Example initialization
        stock_symbol = tracker.get_slot("stock_symbol")
        amount = tracker.get_slot("amount")

        print(f'pre stocks: {tracker.get_slot("stocks")}')

        if stock_symbol and amount:
            if tracker.get_slot("stocks") is not None:
                current_stocks = tracker.get_slot("stocks")
                stock_found = False
                for stock in current_stocks:
                    if stock["stock_symbol"] == stock_symbol:
                        stock["amount"] += int(amount)
                        stock_found = True
                        dispatcher.utter_message(text=f'Đã hoàn tất giao dịch mua {amount} cổ phiếu {stock_symbol}')
                        break
                if not stock_found:
                    current_stocks.append({"stock_symbol": stock_symbol, "amount": int(amount)})
                    dispatcher.utter_message(text=f'Đã hoàn tất giao dịch mua {amount} cổ phiếu {stock_symbol}')  
            else:
                current_stocks.append({"stock_symbol": stock_symbol, "amount": int(amount)})
                dispatcher.utter_message(text="Bạn đã thành công thực hiện giao dịch!")

        else:
            dispatcher.utter_message(text='Hãy kiểm tra lại giao dịch của bạn!')  
        print(f'Current stocks assigned: {current_stocks}')
        return [SlotSet("stocks", current_stocks)]


class ActionListStocks(Action):
    def name(self) -> Text:
        return "action_list_stock"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the current_stock to list
        current_stocks = []
        
        print(f'Current stocks assigned: {tracker.get_slot("stocks")}')
    
        if tracker.get_slot("stocks") is not None:
            print("Yes")
            current_stocks = tracker.get_slot("stocks")
            if isinstance(current_stocks, list) and all(isinstance(stock, dict) for stock in current_stocks):
                try:
                    stock_list = [f"{stock['amount']} shares of {stock['stock_symbol']}" for stock in current_stocks]
                    dispatcher.utter_message(text=f"You currently own: {', '.join(stock_list)}.")
                except KeyError as e:
                    logging.error(f"Missing key in stock data: {e}")
                    dispatcher.utter_message(text="There was an error retrieving your stocks. Please try again.")
            else:
                logging.error(f"Unexpected format for current_stocks: {current_stocks}")
                dispatcher.utter_message(text="There was an error retrieving your stocks. Please try again.")
        else:
            dispatcher.utter_message(text="You do not own any stocks.")

        return []


class FindPolicyInfo(Action):

    def name(self) -> Text:
        return "action_find_policy_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"Đây là chính sách bạn cần ... ")       
        return []

class WorkPolicyInfo(Action): 

    def name(self) -> Text:
        return "action_find_work_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"Thời gian giao dịch là từ thứ 2 đến thứ 6 bắt đầu từ 9:00 đến 15:00")       
        return []

class AccountInfo(Action): # thông tin đăng nhập

    def name(self) -> Text:
        return "action_account_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("user_name")

        if name:
            dispatcher.utter_message(text = f"Tên đăng nhập của bạn là: {name}")       
        else:
            dispatcher.utter_message(text = f"Bạn cần cung cấp nickname của bạn! Điền ngay tại đây...")
        return []
# name = tracker.get_slot("name")

class ReceiveNickname(Action):  # Ask for the user's nickname

    def name(self) -> Text:
        return "receive_account_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("user_name")
        if name:
            dispatcher.utter_message(text=f'Hello {name}, how can I assist you?')
            return []
          
        text = tracker.latest_message['text']
        dispatcher.utter_message(text=f'Hello {text}, nice to meet you!')
        
        return [SlotSet("user_name", text)]
        

class ProvideSystemInfo(Action):

    def name(self) -> Text:
        return "action_provide_system_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="")       
        return []
    

import aiohttp

class ActionQueryMindsDB(Action):
    def name(self):
        return "action_query_mindsdb"

    async def run(self, dispatcher, tracker, domain):
        user_input = tracker.latest_message.get("text")
        query = f"SELECT * FROM your_model WHERE condition = '{user_input}'"

        # Query MindsDB
        url = "http://localhost:47334/sql/query"
        headers = {"Content-Type": "application/json"}
        data = {"query": query}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    dispatcher.utter_message(text=f"Prediction: {result}")
                else:
                    dispatcher.utter_message(text="Failed to query MindsDB.")

        return []


class ActionReturnIntentAndEntity(Action):

    def name(self) -> Text:
        return "action_return_intent_and_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy intent và entity từ tracker
        user_intent = tracker.latest_message['intent'].get('name')
        user_entities = tracker.latest_message['entities']

        response_data = {
            "intent": user_intent,
            "entities": user_entities if user_entities else []
        }

        # Trả về phản hồi JSON
        dispatcher.utter_message(text=str(response_data))  # Chuyển đổi dict thành chuỗi

        return []