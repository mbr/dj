from __future__ import absolute_import

import requests
from tempfile import NamedTemporaryFile

from mutagen.easyid3 import EasyID3
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

        with NamedTemporaryFile() as tmpfile:
            progress_download_url(stream_url.location, tmpfile, label='TRACK')

            fields = track.fields()
            track_id = fields['id']

            # create new set of id3v2 tags
            meta = EasyID3()
            meta['title'] = 'some soundcloud track'
            if fields['bpm']:
                meta['bpm'] = str(int(fields['bpm']))
            meta['genre'] = fields['genre']
            meta['title'] = fields['title']
            meta['artist'] = fields['user']['username']

            # add track image
            if fields['artwork_url']:
                try:
                    resp = requests.get(fields['artwork_url'])
                except Exception as e:
                    # currently, we always get an ssl error =(
                    print 'Error downloading artwork: {}'.format(e)
                else:
                    resp.raise_for_status()
                    raise NotImplementedError

            meta.save(tmpfile.name)

            tmpfile.seek(0)

            return tmpfile.read(), track_id, 'mp3'
