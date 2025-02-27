import re
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
from server.singleton import SingletonMeta


class WebsocketManager(metaclass=SingletonMeta):
    """
    Manages the active websocket connections
    """

    def __init__(self):
        self.__sockets = []
        self.__store = {}

    async def accept(self, ws: WebSocket):
        """
        Accepts an incoming communication.

        Parameters
        ----------
        user_id : int
            Identifier of the user.
        ws : WebSocket
            Socket relative to the client.
        """
        await ws.accept()
        self.__sockets.append(ws)

        try:
            for flower_id in self.__store:
                await ws.send_text(self.stringify_one_stored_flower(flower_id))
        except WebSocketDisconnect:
            self.__sockets.remove(ws)

    async def listening(self, ws: WebSocket):
        """
        Listens incoming message from a client socket.

         Parameters
        ----------
        ws : WebSocket
            Socket relative to the client.
        """
        while True:
            try:
                message = await ws.receive_text()
                flower_id, number = self.parse_message(message)
                self.add_to_store(flower_id, number)
                await self.__send_message(ws, self.stringify_one_stored_flower(flower_id))
            except WebSocketDisconnect:
                self.__sockets.remove(ws)
                break

    def parse_message(self, message: str) -> (int, int):
        """
        Parses an incoming message.

        Parameters
        ----------
        message : str
            Message to be parsed.

        Returns
        -------
        (int, int)
            The flower identifier and the number of flowers, respectively.

        Raises
        ------
        ValueError
            When the message is invalid.
        """
        regex = re.compile(r'"flower_id":([0-9]+).+"number":(-?[0-9]+)')
        match = regex.search(message.replace(" ", ""))

        if match is None:
            raise ValueError("Invalid message")

        return int(match.group(1)), int(match.group(2))

    def add_to_store(self, flower_id: int, number: int):
        """
        Adds to the websocket store.

        Parameters
        ----------
        flower_id : int
            Identifier of the flower.
        number : int
            Number of flowers.
        """
        if flower_id not in self.__store:
            self.__store[flower_id] = number
        else:
            self.__store[flower_id] += number

    def stringify_one_stored_flower(self, flower_id: int) -> str:
        """
        Stringifies the value of the store for one flower.

        Parameters
        ----------
        flower_id : int
            Identifier of the flower.

        Returns
        -------
        str
            Stringify value of the store for one flower.
        """
        if flower_id not in self.__store:
            return f'{{"flower_id":{flower_id}, "number":0}}'
        else:
            return f'{{"flower_id":{flower_id}, "number":{self.__store[flower_id]}}}'

    async def __send_message(self, ws: WebSocket | None, message: str):
        """
        Sends a message to all clients.

        Parameters
        ----------
        ws : WebSocket
            Socket to which not send the message.
        message : str
            Message to be sent.
        """
        for socket in self.__sockets:
            if socket != ws:
                try:
                    await socket.send_text(message)
                except WebSocketDisconnect:
                    self.__sockets.remove(socket)
                    break
