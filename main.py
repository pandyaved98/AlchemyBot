from bot_live import alive
import os
import json
import requests
import discord
API_URL = 'https://api-inference.huggingface.co/models/pandyaved98/'

class MyClient(discord.Client):
    def __init__(self, model_name):
        super().__init__()
        self.api_endpoint = API_URL + model_name
        huggingface_token = os.environ['HUGGINGFACE_TOKEN']
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }

    def query(self, payload):
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.query({'inputs': {'text': 'Hello!'}})

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        payload = {'inputs': {'text': message.content}}

        async with message.channel.typing():
          response = self.query(payload)
        bot_response = response.get('generated_text', None)

        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'Hmm... something is not right.'

        await message.channel.send(bot_response)

def main():
  client = MyClient('DialoGPT-small-AlchemyBot')
  alive()
  client.run(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
  main()