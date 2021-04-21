import re
import urllib

JAVBUS_URL = 'https://www.javbus.com'


def Start():
    # HTTP.ClearCache()
    HTTP.CacheTime = CACHE_1WEEK
    HTTP.Headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'
    HTTP.Headers['Accept-Encoding'] = 'utf-8'


def get_name(name):
    try:
        match = re.match('.*([a-zA-Z]{3,}-[0-9]{3})', name).groups()
    except:
        return name
    else:
        return match[0]


def make_request(pathname):
    try:
        res = HTML.ElementFromURL(JAVBUS_URL + pathname)
    except:
        return None
    else:
        return res


class JAVDB(Agent.Movies):
    name = 'The JAVDB'
    languages = [Locale.Language.English]
    primary_provider = True
    accepts_from = None
    prev_search_provider = 0

    def search(self, results, media, lang, manual=False):
        Log.Debug("javbus search: %s" % media.name)
        query = urllib.quote(get_name(media.name))
        feed = make_request("/search/%s" % query)
        if feed is not None:
            items = feed.xpath('//*[@id="waterfall"]//div')
            for item in items:
                results.Append(MetadataSearchResult(
                    id=item.xpath('//date[1]')[0].text,
                    name=item.xpath('//a/div[2]/span')[0].text,
                    year=item.xpath('//date[2]')[0].text,
                    score=100,
                    lang=Locale.Language.English,
                ))

    def update(self, metadata, media, lang, force=False):
        Log.Debug("**************update: " + metadata.id)
        data = {}
        html = make_request("/%s" % metadata.id)
        data["Title"] = html.xpath('/html/body/div[5]/h3')[0].text
        Log.Debug('*********Title: '+data["Title"])
        data["Cover"] = html.xpath(
            '/html/body/div[5]/div[1]/div[1]/a/@href')[0]
        Log.Debug('*********Cover: '+data["Cover"])
        data["Thumb"] = "https://pics.javbus.com/thumb/" + \
            data["Cover"].split('/')[-1].split('_')[0]+".jpg"
        Log.Debug('*********Thumb: '+data["Thumb"])
        data["Date"] = html.xpath(
            '/html/body/div[5]/div[1]/div[2]/p[2]/text()')[0]
        Log.Debug('*********Date: '+data["Date"])
        l = html.xpath('/html/body/div[5]/div[1]/div[2]/p[3]/text()')[0][:-2]
        data["Duration"] = int(l)*60000
        Log.Debug('*********Duration: '+str(data["Duration"]))
        items = html.xpath('/html/body/div[5]/div[1]/div[2]//a')
        for item in items:
            link = item.xpath('@href')[0]
            text = item.text
            if "studio" in link:
                data["Studio"] = text
                data["StudioLink"] = link
                Log.Debug('*********Studio: '+text)
            if "label" in link:
                data["Label"] = text
                data["LabelLink"] = link
                metadata.producers.add(text)
                Log.Debug('*********Label: '+text)
            if "director" in link:
                data["Director"] = text
                data["DirectorLink"] = link
                metadata.directors = [text]
                Log.Debug('*********Director: '+text)
            if "series" in link:
                data["Series"] = text
                data["SeriesLink"] = link
                metadata.collections.add(text)
                Log.Debug('*********Series: '+text)
            if "genre" in link:
                metadata.tags.add(text)
                metadata.genres.add(text)
                Log.Debug('*********Genre: '+text)

        metadata.title = data["Title"]
        metadata.duration = data["Duration"]
        metadata.rating = 10.0
        metadata.original_title = data["Title"]
        metadata.year = 2018
        metadata.originally_available_at = Datetime.ParseDate(
            data["Date"]).date()
        metadata.studio = data["Studio"]
        metadata.summary = data["Title"]
        metadata.content_rating = "R18"
        metadata.content_rating_age = 18
        metadata.writers = ["writer"]
        metadata.countries = ["Japan"]
        metadata.posters[data["Thumb"]] = Proxy.Preview(
            HTTP.Request(data["Thumb"]).content)
        metadata.posters[data["Cover"]] = Proxy.Preview(
            HTTP.Request(data["Cover"]).content)
