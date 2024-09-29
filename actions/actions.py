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
        else:
            dispatcher.utter_message(text="Xin lỗi, tôi không thể xác định được cổ phiếu mà bạn định mua, hãy kiểm tra lại tên cô phiếu của bạn.")
        
        return []

class ConfirmPlaceStockOrder(Action):
    def name(self) -> Text:
        return "action_confirm_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_symbol = next(tracker.get_latest_entity_values('stock_symbol'), None) 
        amount = next(tracker.get_latest_entity_values('amount'), None) 

        if stock_symbol and amount:
            # Get the current list of stocks form the slot
            current_stocks = tracker.get_slot("stocks")

            if current_stocks is None:
                current_stocks = []

            # Check if stock already in the list, update the amount if found
            stock_found = False
            for stock in current_stocks:
                if stock["stock_symbol"] == stock_symbol:
                    stock["amount"] += int(amount)
                    stock_found = True
                    dispatcher.utter_message(text=f'Đã hoàn tất giao dịch mua {amount} cổ phiếu {stock_symbol}')
                    break

            # if stock not already in the list, append it ! :3
            if not stock_found:
                current_stocks.append({"stock_symbol": stock_symbol, "amount": int(amount)})
                dispatcher.utter_message(text=f'Đã hoàn tất giao dịch mua {amount} cổ phiếu {stock_symbol}')  
        
        else:
            dispatcher.utter_message(text='Hãy kiểm tra lại giao dịch của bạn!')  
        
        return [{"slot": "stocks", "value": current_stocks}]

class ActionListStocks(Action):
    def name(self) -> Text:
        return "action_list_stock"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            # Get the current_stock to list
            current_stocks = tracker.get_slot("stocks")

            if isinstance(current_stocks, list): 
                stock_list = [f"{stock['amount']} shares of {stock['stock_symbol']}" for stock in current_stocks]
                dispatcher.utter_message(text=f"You currently own: {', '.join(stock_list)}.")
            else:
                dispatcher.utter_message(text="You haven't buy any stock yet")
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
