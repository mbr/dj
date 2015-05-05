import click
from six.moves.urllib.parse import urlparse
from .plugins import all_plugins


@click.command()
@click.argument('urls', nargs=-1)
def main(urls):
    for url in urls:
        u = urlparse(url)

        for plugin in all_plugins:
            if plugin.can_handle(u):
                buf = plugin.handle(u)
                with open('out.mp3', 'w') as out:
                    out.write(buf)
