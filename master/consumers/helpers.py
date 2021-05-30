from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .constants import SocketChannels, SocketKeys


def send_update_to_socket(event, sub_event, channel, data):
    channel_layer = get_channel_layer()

    if channel is None or event is None or sub_event is None or data is None:
        return

    try:
        async_to_sync(channel_layer.group_send)(
            channel, {
                'type': 'websocket.ingest',
                'data': {
                    SocketKeys.EVENT: event,
                    SocketKeys.SUB_EVENT: sub_event,
                    SocketKeys.DATA: data,
                }
            }
        )
    except:
        print("Error sending socket message")
