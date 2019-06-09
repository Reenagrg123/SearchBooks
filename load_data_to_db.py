




def load_python(artist):
    name, bio, pic = load_wiki(artist)
    bio = bio[:100]
    artist_dict = {
        'name': name,
        'bio': bio,
        'pics': pic,
        'social_acc': 'social',
    }
    a

