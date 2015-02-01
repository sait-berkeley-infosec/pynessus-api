# coding=utf-8

import inspect

def multiton(cls):
    """
    Class decorator to make a class a multiton.
    That is, there will be only (at most) one object existing for a given set
    of initialization parameters.
    """
    instances = {}
    def getinstance(*args, **kwargs):
        key = _gen_key(cls, *args, **kwargs)
                
        if key not in instances:
            instances[key] = cls(*args, **kwargs)
        return instances[key]
    return getinstance

kwd_mark = (object(), ) # seperate args and kwargs with a unique object
def _gen_key(cls, *args, **kwargs):
    new_args, new_kwargs = _normalize_args(cls.__init__, *args, **kwargs)

    key = new_args
    if new_kwargs:
        key += kwd_mark
        sorted_items = sorted(new_kwargs.items())
        for item in sorted_items:
            key += item
    return tuple(key)

def _normalize_args(func, *args, **kwargs):
    try:
        arg_names, _, _, arg_defaults = inspect.getargspec(func)
    except AttributeError: # cls has no __init__
        arg_names = ['self']
        arg_defaults = ()
    arg_names = arg_names[1:] # skip first arg (self)
    if arg_defaults is None:
        arg_defaults = ()

    new_args = []
    new_kwargs = {}

    # match named args to names
    for name, arg in zip(arg_names, args):
        new_kwargs[name] = arg

    # handle extra args from *
    if len(args) > len(arg_names):
        for arg in args[len(arg_names):]:
            new_args.append(arg)
    # or fill in default values
    else:
        for name, default in zip(arg_names[len(args):], arg_defaults):
            new_kwargs[name] = default

    # merge remaining **kwargs
    new_kwargs.update(kwargs)

    return new_args, new_kwargs

