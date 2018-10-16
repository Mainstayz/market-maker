from __future__ import absolute_import

import importlib
import os
import sys

from utils.dotdict import dotdict
import _settings_base as baseSettings


def import_path(fullpath):
    """
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do.

    动态导入模块
        一般而言，当我们需要某些功能的模块时（无论是内置模块或自定义功能的模块），可以通过import module 或者 from * import module的方式导入，这属于静态导入，很容易理解。
        而如果当我们需要在程序的运行过程时才能决定导入某个文件中的模块时，并且这些文件提供了同样的接口名字，上面说的方式就不适用了，这时候需要使用python 的动态导入。


    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.insert(0, path)
    module = importlib.import_module(filename, path)
    importlib.reload(module)  # Might be out of date
    del sys.path[0]
    return module


userSettings = import_path(os.path.join('.', 'user_settings'))
symbolSettings = None
symbol = sys.argv[1] if len(sys.argv) > 1 else None
if symbol:
    print("Importing symbol settings for %s..." % symbol)
    try:
        symbolSettings = import_path(
            os.path.join('..', 'settings-%s' % symbol))
    except Exception as e:
        print("Unable to find settings-%s.py." % symbol)


# Assemble settings.
settings = {}
settings.update(vars(baseSettings))
settings.update(vars(userSettings))
if symbolSettings:
    settings.update(vars(symbolSettings))
# Main export
settings = dotdict(settings)

