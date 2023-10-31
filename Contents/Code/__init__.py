from agent import JavAgent


def Start():
    Log.Info("Initializing agent ...")
    HTTP.CacheTime = CACHE_1WEEK
    HTTP.Headers['Accept-Encoding'] = 'utf-8'
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0'
    HTTP.Headers['Cookie'] = 'bus_auth=' + Prefs['token']


class JavMainAgent(JavAgent):
    def foo():
        return None
