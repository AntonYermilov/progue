import pickle


def serialize_object(obj):
    return pickle.dumps(obj)


def deserialize_object(buffer: bytes):
    return pickle.loads(buffer)
