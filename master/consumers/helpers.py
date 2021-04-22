from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .constants import SocketChannels


def send_update_to_socket(event, sub_event, channel=SocketChannels.COLLECTION_POINT_CHANNEL, data={}):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        channel, {
            'type': 'websocket.ingest',
            'data': {
                "event": event,
                "sub-event": sub_event,
                "data": data,
            }
        }
    )
