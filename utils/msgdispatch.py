# encoding=utf-8
import logging

MESSAGE_TYPES = {}
DEFAULT_MSG_HANDLER = 'default'


def register_message(msg_type):
    def register(fun):
        MESSAGE_TYPES[msg_type] = fun
        return fun

    return register


def msgdispatch(msg):
    msg_type = msg.type + '.%s' % msg.event if hasattr(msg, 'event') else ''
    msg_type += '.%s' % msg.key if hasattr(msg, 'key') and msg.key else ''
    logging.debug(msg_type)
    try:
        impl = MESSAGE_TYPES[msg_type]
    except KeyError:
        try:
            impl = MESSAGE_TYPES[DEFAULT_MSG_HANDLER]
        except KeyError:
            impl = lambda m: ''
    return impl(msg)
