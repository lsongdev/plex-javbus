import urllib

JAVBUS_URL = 'https://www.javbus.com'

"""
make request
"""
def make_request(path):
    try:
        res = HTML.ElementFromURL(JAVBUS_URL + path)
    except:
        return None
    else:
        return res

"""
search by name
"""
def search(name):
    feed = make_request("/search/%s" % urllib.quote(name))
    if feed is None: return
    items = feed.xpath('/html/body/div[4]/div/div[4]/div/div')
    results = []
    for item in items:
        result = {}
        id = item.xpath('./a/div[2]/span/date[1]')[0].text
        Log.Debug("result id: {}".format(id))
        result["id"] = item.xpath('./a/@href')[0].split('/')[-1]
        result["name"] = id + " - " + item.xpath('./a/div[2]/span')[0].text
        result["year"] = item.xpath('./a/div[2]/span/date[2]')[0].text.split('-')[0]
        result["thumb"] = item.xpath('./a/div[1]/img/@src')[0]
        results.append(result)
    # results
    return results


"""
fetch movie info by id
"""
def fetch_info(id):
    feed = make_request("/%s" % id)
    if feed is None: return
    title = feed.xpath('/html/body/div[5]/h3')[0].text
    cover = feed.xpath('/html/body/div[5]/div[1]/div[1]/a/@href')[0]
    date = feed.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')[0]
    duration = feed.xpath('/html/body/div[5]/div[1]/div[2]/p[3]/text()')[0]
    items = feed.xpath('/html/body/div[5]/div[1]/div[2]//a')
    # data
    data = MovieItem()
    for item in items:
        link = item.xpath('@href')[0]
        text = item.text
        if "studio" in link:
            data.studio = text
            data.studio_link = link
        if "label" in link:
            data.label = text
            data.label_link = link
        if "director" in link:
            data.director = text
            data.director_link = link
        if "series" in link:
            data.series = text
            data.series_link = link
        if "genre" in link:
            data.genres.append(text)
    casts = feed.xpath("//*[contains(@class, 'star-name')]/a")
    for item in casts:
        cast = MovieCast()
        cast.name = item.text
        cast.link = item.xpath('@href')[0]
        data.casts.append(cast)
    # data
    data.title = title
    data.cover = cover
    data.duration = duration
    data.date = Datetime.ParseDate(date)
    data.thumb = "https://pics.javbus.com/thumb/" + cover.split('/')[-1].split('_')[0]+".jpg"
    return data

class MovieCast():
    def __init__(self):
        self.name = ""
        self.link = ""
    def get_avatar(self):
        id = self.link.split("/")[-1]
        return "https://pics.javbus.com/actress/{}_a.jpg".format(id)

class MovieItem():
    def __init__(self):
        self.title = ""
        self.genres = []
        self.duration = ""
        self.date = ""
        self.thumb = ""
        self.studio = ""
        self.studio_link = ""
        self.label = ""
        self.label_link = ""
        self.director = ""
        self.director_link = ""
        self.series = ""
        self.series_link = ""
        self.casts = []
