from plexapi.myplex import MyPlexAccount, MyPlexResource
from errors import NoServerError, SignInError, WrongResourceError, NotSignedInError, NotMediaServerError, UserError
from scrape import imdb


class Plex:

    server = None
    resource = None
    account = None
    signed_in = False

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.sign_in()

    def sign_in(self):
        try:
            self.account = MyPlexAccount(self.username, self.password)
            self.signed_in = True
        except:
            raise SignInError("Could not sign in")

    def get_resources(self):
        if (not self.signed_in):
            raise NotSignedInError("Not signed in ")

        return self.account.resources()

    def get_plex_server_resources(self):
        if (not self.signed_in):
            raise NotSignedInError("Not signed in ")

        plex_servers = []

        for resource in self.account.resources():
            if (resource.product == "Plex Media Server"):
                plex_servers.append(resource)

        return plex_servers

    def add_resource_by_name(self, name):
        if (not self.signed_in):
            raise NotSignedInError("Not signed in ")

        resources = self.get_resources()

        for resource in resources:

            if (resource.name != name):
                continue

            if (resource.product != "Plex Media Server"):
                raise NotMediaServerError("Not media server")

            self.resource = resource
            return

        raise NoServerError("No server with that name")

    def add_resource(self, resource):
        if (not self.signed_in):
            raise NotSignedInError("Not signed in ")

        if (resource.product != "Plex Media Server"):
            raise NotMediaServerError("Not media server")

        self.resource = resource

    def connect(self):
        if (not self.signed_in):
            raise NotSignedInError("Not signed in ")

        if (not self.resource):
            raise NoServerError("No resource attached")

        self.server = self.resource.connect()

    def add_playlist(self, name: str, name_list):
        if (not self.signed_in):
            raise NotSignedInError("Not signed in ")

        if (not self.server):
            raise NoServerError("No server attached")

        movie_list = []
        failed_movies = []

        for movie in name_list:

            # get movie if it exists
            temp = self.__get_movie(movie)

            # loop if it can't find the movie
            if temp is False:
                failed_movies.append(movie["title"])
                continue

            # add to list if it can find it
            movie_list.append(temp)

        # create playlist
        playlist = self.server.createPlaylist(name, movie_list)

        return playlist, failed_movies

    def __get_movie(self, movie):
        results = self.server.search(movie["title"])

        # return movie if it exists
        for plex_movie in results:

            if plex_movie.type == "movie" and str(plex_movie.year) in str(
                    movie["year"]):
                return plex_movie

        return False

    def copy_to_users(self, playlist, users):
        for user in users:
            try:
                playlist.copyToUser(user)
            except:
                print(f"{user} does not have access to the library.")

    def scrape_imdb(self, link):
        movie_list = imdb(link)
        return movie_list

    def get_users(self):
        return [
            user.title for user in self.server.myPlexAccount().users()
            if user.friend
        ]

    def check_login(self, username, password):
        try:
            MyPlexAccount(username, password)
            return True
        except:
            return False
