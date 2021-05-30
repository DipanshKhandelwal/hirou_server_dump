class SocketChannels:
    BASE_ROUTE = 'base-route'
    TASK_ROUTE = 'task-route'


class SocketKeys:
    EVENT = 'event'
    SUB_EVENT = 'sub-event'
    DATA = 'data'


class SocketEventTypes:
    BASE_ROUTE = 'base-route'
    TASK_ROUTE = 'task-route'
    COLLECTION_POINT = 'collection-point'
    TASK_COLLECTION_POINT = 'task-collection-point'
    TASK_COLLECTION = 'task-collection'
    LOCATION = 'location'


class SocketSubEventTypes:
    REORDER = 'reorder'
    BULK_COMPLETE = 'bulk-complete'
    UPDATE = 'update'
    CREATE = 'create'
    DELETE = 'delete'


class SocketUpdateTypes:
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'
