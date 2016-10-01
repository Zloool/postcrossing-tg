import cookielib
import urllib
import urllib2
import requests
import re
import ssl

class PostCardUser(object):

    def __init__(self, login, password):
        """ Start up... """
        self.login = login
        self.password = password
        #ctx = ssl.create_default_context()
        #ctx.check_hostname = False
        #ctx.verify_mode = ssl.CERT_NONE

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0, ),#context=ctx
            #urllib2.ProxyHandler({'https': '127.0.0.1:8080'}),
            urllib2.HTTPCookieProcessor(self.cj),
            )

        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]
        self.token = self.gettoken()

    def gettoken(self):
        """
        Handle login. This should populate our cookie jar.
        """
        response = self.opener.open("https://www.postcrossing.com/loginFirst")
        page = ''.join(response.readlines())
        regex = r'_csrf_token\]\" value=\"(.+)\" id'
        result = re.search(regex, page)
        return result.group(1)

    def loginToPC(self):
        """
        Handle login. This should populate our cookie jar.
        """
        login_data = urllib.urlencode({
            'signin[username]' : self.login,
            'signin[password]' : self.password,
            'signin[remember]' : 'on',
            'signin[_csrf_token]' : self.token,
        })
        response = self.opener.open("https://www.postcrossing.com/login", login_data)
        page = ''.join(response.readlines())
        regex = r'send\">(\d) left'
        result = re.search(regex, page)
        #return ''.join(response.readlines())
        return result.group(1)
