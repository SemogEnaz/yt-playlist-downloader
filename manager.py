import subprocess

user_names = [
    'Kanyeunreleased432'
]

class Playlist:

    def __init__(self, name: str, link: str) -> None:
        self.name = name
        self.link = link

def get_playlists(user_playlists_page_url: str) -> list[Playlist]:

    command = \
        f'yt-dlp --flat-playlist --get-title --get-id {user_playlists_page_url}'\
        .split()
    
    print(f'Getting playlist data from {user_playlists_page_url}')
    playlists_data_raw = \
        subprocess.run(command, text=True, stdout=subprocess.PIPE) \
        .stdout.split('\n')\
        [:-1]   # last element is an empty string

    playlists_array = [
        playlists_data_raw[i:i+2] 
        for i in range(0, len(playlists_data_raw), 2)
    ]

    playlists = [
        Playlist(playlist_array[0], playlist_array[1])
        for playlist_array in playlists_array
    ]

    return playlists

def make_user_dir(user_name: str, user_dirs: list[str]) -> str:

    if user_name in user_dirs: return

    print(f'Making {user_name}\'s director...')
    command = ['mkdir', f'{user_name}']
    subprocess.run(command)

    return user_name

def make_playlist_dir(user_name: str, playlist_name: str) -> str:

    command = f'ls {user_name}'.split()

    # Getting playlists from user_dir
    playlists_in_user_dir = \
        subprocess.run(command, text=True, stdout=subprocess.PIPE)\
        .stdout.split('\n')
    
    # Removing files with extensions to differenciate dirs
    playlists_in_user_dir = [
        playlist_dir_name \
        for playlist_dir_name in playlists_in_user_dir \
        if '.' not in playlist_dir_name
    ]

    # Sanitizing / in dir names
    playlist_name = playlist_name.replace('/', ' or')
    dir = f'{user_name}/{playlist_name}'

    if playlist_name in playlists_in_user_dir: 
        print(f'Dir {dir} exists, returning dir name')
        return dir

    print(f'Making playlist dir {dir}...')
    command = ['mkdir', dir]
    subprocess.run(command)

    return dir

user_dirs = \
    subprocess.run(['ls'], text=True, stdout=subprocess.PIPE)\
    .stdout.split('\n')

for user_name in user_names:

    user_dir = make_user_dir(user_name, user_dirs)

    user_playlist_page_url = f'https://www.youtube.com/@{user_name}/playlists'
    
    playlists = get_playlists(user_playlist_page_url)

    for playlist in playlists:

        playlist_dir = make_playlist_dir(user_name, playlist.name)

        command = f'yt-dlp -x --audio-format best --embed-thumbnail --add-metadata -o'.split()
        command.append(f'./{playlist_dir}/%(title)s.%(ext)s')
        command.append(f'https://www.youtube.com/playlist?list={playlist.link}')

        shell_command = f'yt-dlp -x --audio-format best --embed-thumbnail --add-metadata -o "./{playlist_dir}/" "https://www.youtube.com/playlist?list={playlist.link}"'

        print(f'Saving {playlist.name}!')
        subprocess.run(command)
    
