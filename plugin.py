###
# Copyright (c) 2016, Andrew Edwards
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import requests
import random

from urllib import parse
from bs4 import BeautifulSoup

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Dogpile')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

#globals
HEADERS = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'}
search_url = "http://dogpile.com/search"

class Dogpile(callbacks.Plugin):
    """Scrapes Dogpile.com for web and image searches."""
    threaded = True

    def gis(self, irc, msg, args, text):
        """Uses the dogpile search engine to search for images."""
        image_url = search_url + "/images"
        params = { 'q': " ".join(text.split())}
        r = requests.get(image_url, params=params, headers=HEADERS)
        soup = BeautifulSoup(r.content)
        linklist = soup.find('div', id="webResults").find_all('a', {'class':'resultThumbnailLink'})
        image = parse.unquote(parse.unquote(random.choice(linklist)['href']).split('ru=')[1].split('&')[0])
        irc.reply(image)
    gis = wrap(gis, ['string'])

    def g(self, irc, msg, args, text):
        """Uses the dogpile search engine to find shit on the web."""
        web_url = search_url + "/web"
        params = {'q':" ".join(text.split())}
        r = requests.get(web_url, params=params, headers=HEADERS)
        soup = BeautifulSoup(r.content)
        result_url = parse.unquote(parse.unquote(soup.find('div', id="webResults").find_all('a', {'class':'resultDisplayUrl'})[0]['href']).split('ru=')[1].split('&')[0])
        result_description = soup.find('div', id="webResults").find_all('div', {'class':'resultDescription'})[0].text
        irc.reply("\x02{}\x02 -- {}".format(result_url, result_description))
    g = wrap(g, ['string'])
Class = Dogpile


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
