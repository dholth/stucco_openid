class OpenID(object):
    __name__ = u''
    __parent__ = None

    def __init__(self, name='', parent=None):
        self.__name__ = name
        self.__parent__ = parent

root = OpenID('')

def get_root(request):
    """This is for testing. A real application would make an OpenID
    object available in their URL space."""
    return root
