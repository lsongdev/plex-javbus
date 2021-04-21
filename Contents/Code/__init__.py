from agent import JavAgent


def Start():
    Log.Info("Initializing agent ...")
    HTTP.CacheTime = CACHE_1WEEK
    HTTP.Headers['Accept-Encoding'] = 'utf-8'


class JavMainAgent(JavAgent):
    def foo():
        return None