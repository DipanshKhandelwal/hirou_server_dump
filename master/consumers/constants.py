class SocketChannels:
    COLLECTION_POINT_CHANNEL = 'collection-point-channel'
    TASK_COLLECTION_POINT_CHANNEL = 'task-collection-point-channel'

    @classmethod
    def get_all(cls):
        return [cls.COLLECTION_POINT_CHANNEL, cls.TASK_COLLECTION_POINT_CHANNEL]


class SocketEventTypes:
    BASE_ROUTE = 'base-route'
    TASK_ROUTE = 'task-route'
    COLLECTION_POINT = 'collection-point'
    TASK_COLLECTION_POINT = 'task-collection-point'


class SocketSubEventTypes:
    REORDER = 'reorder'
    UPDATE = 'update'
    CREATE = 'create'


class SocketUpdateTypes:
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'
