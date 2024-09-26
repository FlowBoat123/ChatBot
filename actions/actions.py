# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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
            dispatcher.utter_message(text=f"You have selected {stock_symbol} as your stock choice")
            dispatcher.utter_message(text=f"Hãy xác nhận mua {amount} cổ phiếu {stock_symbol}")
        else:
            dispatcher.utter_message(text="Im sorry, I could not detect the stock choice")
        
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

class AccountInfo(Action):

    def name(self) -> Text:
        return "action_account_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Tên đăng nhập của bạn là ....")       
        return []


class ConfirmPlaceStockOrder(Action):

    def name(self) -> Text:
        return "action_confirm_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Xác nhận thực hiện giao dịch")       
        return []

class Unclassified(Action):

    def name(self) -> Text:
        return "action_unclassified"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="")       
        return []
