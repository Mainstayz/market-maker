class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__





if __name__ == "__main__":
    obj = dotdict({"aaa":"xxxx"})
    print(obj)