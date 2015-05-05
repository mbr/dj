class Plugin(object):
    def can_handle(self, url):
        raise NotImplementedError


class SingleHostMixin(object):
    def can_handle(self, url):
        return url.netloc == self.NETLOC
