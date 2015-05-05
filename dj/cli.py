import os
import subprocess

import click
from six.moves.urllib.parse import urlparse
from slugger import Slugger
from .plugins import all_plugins


sl = Slugger('en_US')


@click.command()
@click.argument('urls', nargs=-1)
@click.option('--dest-dir', '-d', default='.')
def main(urls, dest_dir):
    for url in urls:
        u = urlparse(url)

        for plugin in all_plugins:
            if plugin.can_handle(u):
                buf, name, ext = plugin.handle(u)

                fn = os.path.join(dest_dir, sl.sluggify(name)) + '.' + ext
                print 'Writing track', fn
                with open(fn, 'w') as out:
                    out.write(buf)

                if ext == 'mp3':
                    # apply replaygain as id3v2 tag
                    subprocess.check_call(['mp3gain', '-s', 'i', fn])
