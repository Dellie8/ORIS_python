class Playlist:
    def __init__(self):
        self.songs = []


    def add_song(self, name, duration):
        songs_dir = {}
        songs_dir["name"] = name
        songs_dir["duration"] = duration
        self.songs.append(songs_dir)



    def remove_song(self, name):
        for song in self.songs:
            if song["name"]==name:
                self.songs.remove(song)
                break
        else:
            print("Такой песни нет в плейлисте")


    def total_duration(self):
        total =0
        for song in self.songs:
            total += song["duration"]

        return total

    def __len__(self):
        return len(self.songs)

    def see_all_songs(self):
        for song in self.songs:
            print(f"{song['name']} : {song['duration']}")

playlist = Playlist()
playlist0 = Playlist()
playlist.add_song("Life will change", 262)
playlist.add_song("Rivers in the desert", 310)
print(len(playlist))
print(len(playlist0))
playlist.remove_song("Life will change")
playlist.remove_song("Hudshag;ogh;f")
print(playlist.total_duration())
playlist.see_all_songs()






