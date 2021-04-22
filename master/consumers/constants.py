class SocketChannels:
    COLLECTION_POINT_CHANNEL = 'collection-point-channel'
    TASK_COLLECTION_POINT_CHANNEL = 'task-collection-point-channel'

    @classmethod
    def get_all(cls):
        return [cls.COLLECTION_POINT_CHANNEL, cls.TASK_COLLECTION_POINT_CHANNEL]
