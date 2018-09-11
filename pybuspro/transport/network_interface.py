from .udp_client import UDPClient
from ..core.telegram import TelegramHelper, Telegram
from ..helpers.enums import OperateCode

class NetworkInterface:
    def __init__(self, buspro, gateway_address_send_receive):
        self.buspro = buspro
        self.gateway_address_send_receive = gateway_address_send_receive
        self.udp_client = None
        self.callback = None
        self._init_udp_client()
        self._th = TelegramHelper()

    def _init_udp_client(self):
        self.udp_client = UDPClient(self.buspro, self.gateway_address_send_receive, self._udp_request_received)

    def register_callback(self, callback):
        self.callback = callback

    def _udp_request_received(self, data, address):
        """
        Triggering callback for received data
        :param data:
        :param address:
        :return:
        """
        if self.callback is not None:
            telegram = self._th.build_telegram(data, address)
            self.callback(telegram)

    async def start(self):
        await self.udp_client.start()

    async def stop(self):
        if self.udp_client is not None:
            await self.udp_client.stop()
            self.udp_client = None

    async def send_message(self, message):
        await self.udp_client.send_message(message)

    async def send_telegram(self, telegram):
        message = self._th.build_send_buffer(telegram)
        await self.udp_client.send_message(message)

    '''
    async def activate_scene(self, target_address, scene_address):
        telegram = Telegram()
        telegram.target_address = tuple(target_address)
        telegram.payload = scene_address
        telegram.operate_code = OperateCode.SceneControl
        await self.send_telegram(telegram)
    '''

    async def send_message(self, target_address, payload):
        telegram = Telegram()
        telegram.target_address = tuple(target_address)
        telegram.payload = payload
        telegram.operate_code = OperateCode.SceneControl
        await self.send_telegram(telegram)
