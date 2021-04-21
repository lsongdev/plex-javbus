import os
import re
import api
import urllib


def parse_name(str):
    try:
        match = re.match('([a-zA-Z]{2,}-\d+)', str).group(1)
    except:
        return None
    else:
        return match


def from_filename(filename):
    if filename is None: return filename
    f = urllib.unquote(filename)
    filename_without_ext = os.path.splitext(os.path.basename(f))[0]
    return parse_name(filename_without_ext)


class JavAgent(Agent.Movies):
    name = 'The JAVDB'
    languages = [
        Locale.Language.English,
        Locale.Language.Chinese,
        Locale.Language.Japanese
    ]
    primary_provider = True
    accepts_from = None
    prev_search_provider = 0
    def search(self, results, media, lang, manual=False):
        """
        This is called when you click on "fix match" button in Plex.
        :type results: ObjectContainer
        :type media: Media
        :type lang: str
        :type manual: bool
        :return:
        """
        Log.Info("Searching media ...")
        Log.Debug("lang: {}".format(lang))
        Log.Debug("media.id: {}".format(media.id))
        Log.Debug("media.name: {}".format(media.name))
        Log.Debug("media.year: {}".format(media.year))
        Log.Debug("media.filename: {}".format(media.filename))

        name = None
        if name is None: name = from_filename(media.filename)
        if name is None: name = parse_name(media.name)
        if name is None: name = media.name
        Log.Debug("javbus search: %s" % name)
        items = api.search(name)
        if items is None: return
        for item in items:
            result = MetadataSearchResult(
                id = item["id"],
                name = item["name"],
                year = item["year"],
                thumb = item["thumb"],
                lang = Locale.Language.English,
                score=100
            )
            Log.Debug("search result item: {}".format(result))
            results.Append(result)

    def update(self, metadata, media, lang, force=False):
        """
        self:
        metadata:
        """
        Log.Info("Updating media ...")
        Log.Debug("lang: {}".format(lang))
        Log.Debug("force: {}".format(force))
        Log.Debug("metadata.id: {}".format(metadata.id))
        Log.Debug("metadata.title: {}".format(metadata.title))
        Log.Debug("metadata.year: {}".format(metadata.year))
        # make request
        data = api.fetch_info(metadata.id)
        if data is None: return
        # data
        Log.Debug("data.title: {}".format(data.title))
        Log.Debug("data.label: {}".format(data.label))
        Log.Debug("data.date: {}".format(data.date.date()))
        Log.Debug("data.studio: {}".format(data.studio))
        Log.Debug("data.duration: {}".format(data.duration))
        Log.Debug("data.director: {}".format(data.director))
        Log.Debug("data.series: {}".format(data.series))
        Log.Debug("data.thumb: {}".format(data.thumb))
        # genres
        for tag in data.genres:
            metadata.tags.add(tag)
            metadata.genres.add(tag)
            Log.Debug("data.genres: {}".format(tag))
        
        # posters
        for key in metadata.posters.keys():
            del metadata.posters[key]
        
        # casts
        for cast in data.casts:
            avatar = cast.get_avatar()
            role = metadata.roles.new()
            role.name = cast.name
            role.photo = avatar
            Log.Debug("cast: {} -> {}".format(cast.name, avatar))

        # assign
        metadata.title = data.title
        metadata.summary = data.title
        metadata.studio = data.studio
        metadata.year = data.date.year
        metadata.original_title = data.title
        metadata.originally_available_at = data.date.date()
        metadata.duration = int(data.duration[:-2]) * 60000
        metadata.rating = 10.0
        metadata.content_rating = "R18"
        metadata.content_rating_age = 18
        metadata.writers = ["writer"]
        metadata.countries = ["Japan"]
        metadata.directors = [data.director]
        metadata.producers.add(data.label)
        metadata.collections.add(data.series)
        metadata.posters[data.thumb] = Proxy.Preview(HTTP.Request(data.thumb).content)
        # done
        Log.Info("Update is done")
