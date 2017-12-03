import logging
logger = logging.getLogger(__name__)
tabbing = 0


def log(fn):
    from itertools import chain

    def wrapped(*v, **k):
        global tabbing
        name = fn.__name__
        module = fn.__module__
        params = ", ".join(map(repr, chain(v, k.values())))

        logger.debug("%s%s.%s(%s)" % ('|' * tabbing, module, name, params))
        tabbing += 1
        retval = fn(*v, **k)
        tabbing -= 1
        logger.debug("%sreturned %s" % ('|' * tabbing, retval))

        return retval
    return wrapped

