from __future__ import absolute_import

import soundcloud

from .base import Plugin, SingleHostMixin
from ..util import progress_download_url


# from the web client, no fucks given:
CLIENT_ID = 'b45b1aa10f1ac2941910a7f0d10f8e28'


class SoundCloud(SingleHostMixin, Plugin):
    NETLOC = 'soundcloud.com'

    def handle(self, url):
        client = soundcloud.Client(client_id=CLIENT_ID)

        # resolve to API uri
        track = client.get('/resolve', url=url.geturl())
        stream_url = client.get(track.stream_url, allow_redirects=False)

        import pdb; pdb.set_trace()  # DEBUG-REMOVEME

        return progress_download_url(stream_url.location, label='TRACK')
