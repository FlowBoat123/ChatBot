from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage
from sanic import Blueprint, response
import aiohttp

class MindsDBConnector(InputChannel):
    def name(self):
        return "mindsdb"

    async def _query_mindsdb(self, query: str):
        # Example code to send a query to MindsDB
        url = "http://localhost:47334/sql/query"
        headers = {"Content-Type": "application/json"}
        data = {"query": query}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"error": "Failed to query MindsDB"}

    async def handle_message(self, text: str):
        # Customize how you handle user input
        query = f"SELECT * FROM mindsdb_model WHERE text = '{text}'"
        result = await self._query_mindsdb(query)
        return result

    def blueprint(self, on_new_message):
        mindsdb_webhook = Blueprint("mindsdb_webhook", __name__)

        @mindsdb_webhook.route("/webhook", methods=["POST"])
        async def receive(request):
            payload = request.json
            user_message = payload.get("message")
            result = await self.handle_message(user_message)
            return response.json(result)

        return mindsdb_webhook
