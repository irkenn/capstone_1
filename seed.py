from app import app
from models import db, User, SpotifyContent, Artist, ArtistTrack, ArtistAlbum, Track, Album, Thread, Comment, ThreadVote, SubComment


db.drop_all()
db.create_all()

# User.query.delete()
# SpotifyContent.query.delete()
# Thread.query.delete()
# Artist.query.delete()
# ArtistAlbum.query.delete()
# ArtistAlbum.query.delete()
# Track.query.delete()
# Album.query.delete()

#users
u1 = User(username="Hannah", 
          email='hannah@aol.com', 
          password='123Welcome', 
          image_url='https://research-information.bris.ac.uk/ws/files/289901366/Hannah_Bloomfield_headshot_min.jpg')

u2 = User(username="Mark", 
          email='mark@aol.com', 
          password='Welcome123', 
          image_url='https://research-information.bris.ac.uk/ws/files/289901366/Hannah_Bloomfield_headshot_min.jpg')


db.session.add_all([u1, u2])
db.session.commit()


##artists
artist1 = Artist(name="Radiohead", 
                spotify_id='4Z8W4fKeB5YxbusRsdQVPb', 
                external_url="https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb", 
                preview_url="https://i.scdn.co/image/ab67616100005174a03696716c9ee605006047fd", 
                followers=7897830)
spo_art1 = SpotifyContent(content_type='artist', id='4Z8W4fKeB5YxbusRsdQVPb')

artist2 = Artist(name="Pink Floyd", 
                spotify_id='0k17h0D3J5VfsdmQ1iZtE9', 
                external_url="https://open.spotify.com/artist/0k17h0D3J5VfsdmQ1iZtE9", 
                preview_url="https://i.scdn.co/image/d011c95081cd9a329e506abd7ded47535d524a07", 
                followers=18455241)

spo_art2 = SpotifyContent(content_type='artist', id='0k17h0D3J5VfsdmQ1iZtE9')

db.session.add_all([artist1, spo_art1, artist2, spo_art2])
db.session.commit()

#albums

album1 = Album(spotify_id='4LH4d3cOWNNsVw41Gqt2kv',
                name='The Dark Side of the Moon',
                release_date='1973',
                total_tracks=10,
                external_url = 'https://open.spotify.com/album/4LH4d3cOWNNsVw41Gqt2kv',
                preview_url= 'https://i.scdn.co/image/ab67616d00001e02ea7caaff71dea1051d49b2fe')

spo_alb1 = SpotifyContent(content_type='album', id='4LH4d3cOWNNsVw41Gqt2kv')

#tracks
track1 = Track(spotify_id='6zSpb8dQRaw0M1dK8PBwQz',
                name='Cold Heart - PNAU Remix',
                external_url='https://open.spotify.com/track/6zSpb8dQRaw0M1dK8PBwQz',
                album_id= '5D8Rdb09BkmHscEGSWAlA6')

spo_tra1 = SpotifyContent(content_type='track', id='6zSpb8dQRaw0M1dK8PBwQz')

#album from the track
spo_alb2 = SpotifyContent(content_type='album', id='5D8Rdb09BkmHscEGSWAlA6')
album2 = Album(spotify_id='5D8Rdb09BkmHscEGSWAlA6',
                name='Cold Heart (PNAU Remix)',
                release_date='2021',
                total_tracks=1,
                external_url = 'https://open.spotify.com/album/5D8Rdb09BkmHscEGSWAlA6',
                preview_url= 'https://i.scdn.co/image/ab67616d00001e029f5cce8304c42d3a5463fd23')


artist3 = Artist(name="Elton John", 
                spotify_id='3PhoLpVuITZKcymswpck5b', 
                external_url='https://open.spotify.com/artist/3PhoLpVuITZKcymswpck5b', 
                preview_url='https://i.scdn.co/image/ab676161000051740a7388b95df960b5c0da8970', 
                followers=11087985)
spo_art3 = SpotifyContent(content_type='artist', id='3PhoLpVuITZKcymswpck5b')

artist4 = Artist(name="Dua Lipa", 
                spotify_id='6M2wZ9GZgrQXHCFfjv46we', 
                external_url='https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we', 
                preview_url='https://i.scdn.co/image/ab67616100005174d42a27db3286b58553da8858', 
                followers=38857802)
spo_art4 = SpotifyContent(content_type='artist', id='6M2wZ9GZgrQXHCFfjv46we')

artist5 = Artist(name='PNAU',
                spotify_id='6n28c9qs9hNGriNa72b26u', 
                external_url='https://open.spotify.com/artist/6n28c9qs9hNGriNa72b26u', 
                preview_url='https://i.scdn.co/image/ab676161000051747211732c945e492c8f8c68cc', 
                followers=200111)
spo_art5 = SpotifyContent(content_type='artist', id='6n28c9qs9hNGriNa72b26u')

db.session.add_all([album1, 
                    spo_alb1, 
                    track1, 
                    spo_tra1, 
                    artist3, 
                    spo_art3,
                    artist4,
                    spo_art4,
                    artist5,
                    spo_art5,
                    album2,
                    spo_alb2])

db.session.commit()

## This is the space for relationship tables
#Pink Floyd 
artists_albums1 = ArtistAlbum(artist_id='0k17h0D3J5VfsdmQ1iZtE9', album_id='4LH4d3cOWNNsVw41Gqt2kv')

#Cold Heart song and its artists
artists_tracks1 = ArtistTrack(artist_id='3PhoLpVuITZKcymswpck5b', track_id='6zSpb8dQRaw0M1dK8PBwQz')
artists_tracks2 = ArtistTrack(artist_id='6M2wZ9GZgrQXHCFfjv46we', track_id='6zSpb8dQRaw0M1dK8PBwQz')
artists_tracks3 = ArtistTrack(artist_id='6n28c9qs9hNGriNa72b26u', track_id='6zSpb8dQRaw0M1dK8PBwQz')

#Cold Heart album and its artists
artists_albums2 = ArtistAlbum(artist_id='3PhoLpVuITZKcymswpck5b', album_id='5D8Rdb09BkmHscEGSWAlA6')
artists_albums3 = ArtistAlbum(artist_id='6M2wZ9GZgrQXHCFfjv46we', album_id='5D8Rdb09BkmHscEGSWAlA6')
artists_albums4 = ArtistAlbum(artist_id='6n28c9qs9hNGriNa72b26u', album_id='5D8Rdb09BkmHscEGSWAlA6')

db.session.add_all([artists_albums1,
                    artists_tracks1,
                    artists_tracks2,
                    artists_tracks3,
                    artists_albums2,
                    artists_albums3,
                    artists_albums4
                    ])

db.session.commit()

t1 = Thread(user_id=1, 
            spotify_content_id = '4Z8W4fKeB5YxbusRsdQVPb', 
            title="Checking this works properly", 
            description= "Description works?")

t2 = Thread(user_id=2, 
            spotify_content_id = '4Z8W4fKeB5YxbusRsdQVPb', 
            title="Two threads about the same content", 
            description="Apparently, yes")

t3 = Thread(user_id=1,
            spotify_content_id = '4Z8W4fKeB5YxbusRsdQVPb', 
            title="Third thread about the same content", 
            description= "Another description Another description Another description Another description Another description Another description Another description Another description Another description Another description Another description Another description")

t4 = Thread(user_id=1,
            spotify_content_id = '4LH4d3cOWNNsVw41Gqt2kv', 
            title="Single thread about some content", 
            description= "This is about the Dark Side of The Moon")

t5 = Thread(user_id=2,
            spotify_content_id = '4LH4d3cOWNNsVw41Gqt2kv', 
            title="Checking why does this happens", 
            description= "This is about the Dark Side of The Moon")

db.session.add_all([t1,
                    t2,
                    t3,
                    t4,
                    t5])

db.session.commit()



c1 = Comment(user_id=1, 
             thread_id=1, 
             content = "This is a comment on thread No.1")

c2 = Comment(user_id=2, 
             thread_id=1, 
             content = "This is a second comment on thread No.1")


v1 = ThreadVote(user_id=1,
                thread_id=1,
                vote=1)

v2 = ThreadVote(user_id=2,
                thread_id=1,
                vote=1)

v3 = ThreadVote(user_id=1,
                thread_id=2,
                vote=-1)

v4 = ThreadVote(user_id=2,
                thread_id=2,
                vote=-1)

db.session.add_all([c1, 
                    c2,
                    v1,
                    v2,
                    v3,
                    v4
                    ])
db.session.commit()


sc1 = SubComment(user_id=1, 
             comment_id=1, 
             content = "This is a comment by user 1 on comment 1 on thread No.1")

sc2 = SubComment(user_id=2, 
                comment_id=1, 
                content = "This is a comment by user 2 on comment 1 on thread No.1")

db.session.add_all([sc1, 
                    sc2])

db.session.commit()
