from db import execute_query, fetch_all
import time

print("=" * 60)
print("STREAMIX DATABASE POPULATION")
print("=" * 60)

try:
    # Clear existing data
    print("\n1. Clearing existing data...")
    execute_query("SET FOREIGN_KEY_CHECKS = 0")
    execute_query("DELETE FROM viewing_history")
    execute_query("DELETE FROM rating_review")
    execute_query("DELETE FROM watchlist")
    execute_query("DELETE FROM movie_genre")
    execute_query("DELETE FROM tvshow_genre")
    execute_query("DELETE FROM home_page")
    execute_query("DELETE FROM profile")
    execute_query("DELETE FROM payment")
    execute_query("DELETE FROM subscription")
    execute_query("DELETE FROM movie")
    execute_query("DELETE FROM tv_show")
    execute_query("DELETE FROM genre")
    execute_query("DELETE FROM user")
    execute_query("SET FOREIGN_KEY_CHECKS = 1")
    print("   ✅ Cleared all existing data")
    
    # Insert Users
    print("\n2. Inserting users...")
    users = [
        ("John Doe", "john@example.com", "password123", "1990-05-15", "USA"),
        ("Jane Smith", "jane@example.com", "password123", "1988-08-22", "UK"),
        ("Mike Wilson", "mike@example.com", "password123", "1995-03-10", "Canada"),
        ("Sarah Connor", "sarah@example.com", "password123", "1992-11-30", "Australia"),
        ("David Chen", "david@example.com", "password123", "1985-07-18", "Singapore"),
    ]
    for user in users:
        execute_query("INSERT INTO user (Name, Email, Password, DOB, Country) VALUES (%s, %s, %s, %s, %s)", user)
    print(f"   ✅ Inserted {len(users)} users")
    
    # Insert Genres
    print("\n3. Inserting genres...")
    genres = [
        ("Action", "High-energy films with physical stunts"),
        ("Drama", "Serious narrative focusing on character development"),
        ("Comedy", "Light-hearted entertaining content"),
        ("Thriller", "Suspenseful stories"),
        ("Horror", "Content designed to frighten"),
        ("Sci-Fi", "Science fiction exploring futuristic concepts"),
        ("Romance", "Stories centered around love"),
        ("Crime", "Criminal activities and investigations"),
        ("Fantasy", "Magical and supernatural themed content"),
        ("Documentary", "Non-fiction about real events"),
        ("Animation", "Animated content"),
        ("Adventure", "Exciting journeys and quests"),
        ("Mystery", "Puzzle-solving storylines"),
        ("Biography", "Life stories of real people"),
        ("History", "Historical events"),
    ]
    for genre in genres:
        execute_query("INSERT INTO genre (Genre_Name, Description) VALUES (%s, %s)", genre)
    print(f"   ✅ Inserted {len(genres)} genres")
    
    # Insert Movies
    print("\n4. Inserting movies...")
    movies = [
        ("The Dark Knight", "2008-07-18", 152, "Batman faces the Joker in Gotham", "PG-13", 4.9),
        ("Mad Max: Fury Road", "2015-05-15", 120, "Post-apocalyptic action adventure", "R", 4.5),
        ("John Wick", "2014-10-24", 101, "Ex-hitman seeks revenge", "R", 4.3),
        ("The Shawshank Redemption", "1994-09-23", 142, "Prison drama about hope and redemption", "R", 4.9),
        ("Forrest Gump", "1994-07-06", 142, "Life story of a simple man", "PG-13", 4.8),
        ("The Green Mile", "1999-12-10", 189, "Death row guards meet a special inmate", "R", 4.6),
        ("Inception", "2010-07-16", 148, "Dream heist thriller", "PG-13", 4.8),
        ("The Matrix", "1999-03-31", 136, "Reality-bending sci-fi action", "R", 4.7),
        ("Interstellar", "2014-11-07", 169, "Space exploration to save humanity", "PG-13", 4.6),
        ("Blade Runner 2049", "2017-10-06", 164, "Futuristic detective story", "R", 4.4),
        ("The Grand Budapest Hotel", "2014-03-28", 99, "Quirky hotel comedy-adventure", "R", 4.3),
        ("Superbad", "2007-08-17", 113, "High school comedy", "R", 4.1),
        ("Se7en", "1995-09-22", 127, "Serial killer detective thriller", "R", 4.5),
        ("Gone Girl", "2014-10-03", 149, "Marriage mystery thriller", "R", 4.4),
        ("Shutter Island", "2010-02-19", 138, "Psychological mystery", "R", 4.3),
        ("The Conjuring", "2013-07-19", 112, "Paranormal horror investigation", "R", 4.2),
        ("A Quiet Place", "2018-04-06", 90, "Silent survival horror", "PG-13", 4.3),
        ("The Notebook", "2004-06-25", 123, "Epic love story", "PG-13", 4.2),
        ("La La Land", "2016-12-09", 128, "Musical romance in LA", "PG-13", 4.4),
        ("The Godfather", "1972-03-24", 175, "Mafia family saga", "R", 4.9),
        ("Pulp Fiction", "1994-10-14", 154, "Intertwined crime stories", "R", 4.8),
    ]
    for movie in movies:
        execute_query("INSERT INTO movie (Title, Release_Date, Duration, Description, Age_Rating, average_rating) VALUES (%s, %s, %s, %s, %s, %s)", movie)
    print(f"   ✅ Inserted {len(movies)} movies")
    
    # Insert TV Shows
    print("\n5. Inserting TV shows...")
    shows = [
        ("Breaking Bad", 2008, "Chemistry teacher turned meth producer", "TV-MA", 4.9, "Completed"),
        ("Better Call Saul", 2015, "Criminal lawyer in Albuquerque", "TV-MA", 4.7, "Completed"),
        ("The Crown", 2016, "Queen Elizabeth II biography", "TV-MA", 4.6, "Ongoing"),
        ("Stranger Things", 2016, "Kids uncover supernatural mysteries", "TV-14", 4.7, "Ongoing"),
        ("Black Mirror", 2011, "Dark tech anthology series", "TV-MA", 4.5, "Ongoing"),
        ("Westworld", 2016, "AI theme park thriller", "TV-MA", 4.3, "Ongoing"),
        ("Narcos", 2015, "Pablo Escobar biography", "TV-MA", 4.5, "Completed"),
        ("Peaky Blinders", 2013, "1900s English gangster family", "TV-MA", 4.6, "Completed"),
        ("Ozark", 2017, "Money laundering in the Ozarks", "TV-MA", 4.4, "Completed"),
        ("The Office", 2005, "Mockumentary office comedy", "TV-14", 4.7, "Completed"),
        ("Brooklyn Nine-Nine", 2013, "NYPD precinct comedy", "TV-14", 4.5, "Completed"),
        ("Parks and Recreation", 2009, "Small town government comedy", "TV-14", 4.4, "Completed"),
        ("Mindhunter", 2017, "FBI serial killer profiling", "TV-MA", 4.5, "Ongoing"),
        ("True Detective", 2014, "Crime anthology series", "TV-MA", 4.4, "Ongoing"),
        ("Game of Thrones", 2011, "Fantasy epic power struggle", "TV-MA", 4.6, "Completed"),
        ("The Witcher", 2019, "Monster hunter fantasy", "TV-MA", 4.3, "Ongoing"),
        ("The Boys", 2019, "Dark superhero satire", "TV-MA", 4.6, "Ongoing"),
        ("Jack Ryan", 2018, "CIA analyst action thriller", "TV-14", 4.2, "Ongoing"),
        ("The Haunting of Hill House", 2018, "Family horror drama", "TV-MA", 4.5, "Completed"),
        ("The Walking Dead", 2010, "Zombie apocalypse survival", "TV-MA", 4.3, "Completed"),
    ]
    for show in shows:
        execute_query("INSERT INTO tv_show (Title, Release_Year, Description, Age_Rating, average_rating, Status) VALUES (%s, %s, %s, %s, %s, %s)", show)
    print(f"   ✅ Inserted {len(shows)} TV shows")
    
    # Link Movies to Genres
    print("\n6. Linking movies to genres...")
    # Fetch actual movie and genre IDs
    movies_list = fetch_all("SELECT Movie_Id, Title FROM movie ORDER BY Movie_Id")
    genres_list = fetch_all("SELECT Genre_Id, Genre_Name FROM genre ORDER BY Genre_Id")
    
    # Create mappings
    movie_id_map = {i+1: m['Movie_Id'] for i, m in enumerate(movies_list)}
    genre_name_to_id = {g['Genre_Name']: g['Genre_Id'] for g in genres_list}
    
    # Genre order: Action, Drama, Comedy, Thriller, Horror, Sci-Fi, Romance, Crime, Fantasy, Documentary, Animation, Adventure, Mystery, Biography, History
    genre_order = ["Action", "Drama", "Comedy", "Thriller", "Horror", "Sci-Fi", "Romance", "Crime", "Fantasy", "Documentary", "Animation", "Adventure", "Mystery", "Biography", "History"]
    genre_id_map = {i+1: genre_name_to_id[name] for i, name in enumerate(genre_order)}
    
    movie_genres = [
        (1,1), (1,8), (1,2), (1,4),  # Dark Knight: Action, Crime, Drama, Thriller
        (2,1), (2,12), (2,6),  # Mad Max: Action, Adventure, Sci-Fi
        (3,1), (3,8), (3,4),  # John Wick: Action, Crime, Thriller
        (4,2), (4,8),  # Shawshank: Drama, Crime
        (5,2), (5,7),  # Forrest Gump: Drama, Romance
        (6,2), (6,8), (6,9),  # Green Mile: Drama, Crime, Fantasy
        (7,6), (7,1), (7,4),  # Inception: Sci-Fi, Action, Thriller
        (8,6), (8,1),  # Matrix: Sci-Fi, Action
        (9,6), (9,2), (9,12),  # Interstellar: Sci-Fi, Drama, Adventure
        (10,6), (10,4),  # Blade Runner: Sci-Fi, Thriller
        (11,3), (11,12),  # Grand Budapest: Comedy, Adventure
        (12,3),  # Superbad: Comedy
        (13,8), (13,4), (13,13),  # Se7en: Crime, Thriller, Mystery
        (14,4), (14,2), (14,13),  # Gone Girl: Thriller, Drama, Mystery
        (15,4), (15,13),  # Shutter Island: Thriller, Mystery
        (16,5), (16,4),  # Conjuring: Horror, Thriller
        (17,5), (17,4), (17,6),  # Quiet Place: Horror, Thriller, Sci-Fi
        (18,7), (18,2),  # Notebook: Romance, Drama
        (19,7), (19,2), (19,3),  # La La Land: Romance, Drama, Comedy
        (20,8), (20,2),  # Godfather: Crime, Drama
        (21,8), (21,4),  # Pulp Fiction: Crime, Thriller
    ]
    for mg in movie_genres:
        actual_movie_id = movie_id_map.get(mg[0])
        actual_genre_id = genre_id_map.get(mg[1])
        if actual_movie_id and actual_genre_id:
            execute_query("INSERT INTO movie_genre (Movie_Id, Genre_Id) VALUES (%s, %s)", (actual_movie_id, actual_genre_id))
    print(f"   ✅ Linked movies to genres ({len(movie_genres)} links)")
    
    # Link TV Shows to Genres
    print("\n7. Linking TV shows to genres...")
    shows_list = fetch_all("SELECT Show_Id, Title FROM tv_show ORDER BY Show_Id")
    show_id_map = {i+1: s['Show_Id'] for i, s in enumerate(shows_list)}
    
    show_genres = [
        (1,8), (1,2), (1,4),  # Breaking Bad: Crime, Drama, Thriller
        (2,8), (2,2),  # Better Call Saul: Crime, Drama
        (3,2), (3,14), (3,15),  # Crown: Drama, Biography, History
        (4,6), (4,5), (4,2),  # Stranger Things: Sci-Fi, Horror, Drama
        (5,6), (5,4), (5,2),  # Black Mirror: Sci-Fi, Thriller, Drama
        (6,6), (6,2), (6,13),  # Westworld: Sci-Fi, Drama, Mystery
        (7,8), (7,2), (7,14),  # Narcos: Crime, Drama, Biography
        (8,8), (8,2),  # Peaky Blinders: Crime, Drama
        (9,8), (9,2), (9,4),  # Ozark: Crime, Drama, Thriller
        (10,3),  # Office: Comedy
        (11,3), (11,8),  # Brooklyn 99: Comedy, Crime
        (12,3),  # Parks and Rec: Comedy
        (13,8), (13,4), (13,2),  # Mindhunter: Crime, Thriller, Drama
        (14,8), (14,2), (14,13),  # True Detective: Crime, Drama, Mystery
        (15,9), (15,2), (15,12),  # Game of Thrones: Fantasy, Drama, Adventure
        (16,9), (16,1), (16,12),  # Witcher: Fantasy, Action, Adventure
        (17,1), (17,3), (17,8),  # The Boys: Action, Comedy, Crime
        (18,1), (18,4), (18,2),  # Jack Ryan: Action, Thriller, Drama
        (19,5), (19,2), (19,13),  # Haunting: Horror, Drama, Mystery
        (20,5), (20,2), (20,4),  # Walking Dead: Horror, Drama, Thriller
    ]
    for sg in show_genres:
        actual_show_id = show_id_map.get(sg[0])
        actual_genre_id = genre_id_map.get(sg[1])
        if actual_show_id and actual_genre_id:
            execute_query("INSERT INTO tvshow_genre (Show_Id, Genre_Id) VALUES (%s, %s)", (actual_show_id, actual_genre_id))
    print(f"   ✅ Linked TV shows to genres ({len(show_genres)} links)")
    
    # Create Profiles
    print("\n8. Creating user profiles...")
    # Fetch actual user IDs
    users_list = fetch_all("SELECT User_Id, Name FROM user ORDER BY User_Id")
    user_id_map = {i+1: u['User_Id'] for i, u in enumerate(users_list)}
    
    profiles = [
        (1, "John Main", None, "English", "PG-13"),
        (1, "John Jr", None, "English", "PG"),
        (2, "Jane Personal", None, "English", "R"),
        (3, "Mike", None, "English", "R"),
        (3, "Kids Profile", None, "English", "PG"),
        (4, "Sarah", None, "English", "R"),
        (5, "David Work", None, "English", "R"),
    ]
    for profile in profiles:
        actual_user_id = user_id_map.get(profile[0])
        if actual_user_id:
            execute_query("INSERT INTO profile (User_Id, Profile_Name, Profile_Picture, Language_Preference, Age_Restriction) VALUES (%s, %s, %s, %s, %s)", 
                        (actual_user_id, profile[1], profile[2], profile[3], profile[4]))
    print(f"   ✅ Created {len(profiles)} profiles")
    
    # Add Home Page Featured Content
    print("\n9. Adding home page featured content...")
    # Home_page table structure: Content_Id (PK), Content_Type, Release_Date, Language, Age_Rating
    # We'll add the most popular/featured movies and shows
    
    home_movies = [
        (movie_id_map.get(1), 'Movie', '2008-07-18', 'English', 'PG-13'),  # The Dark Knight
        (movie_id_map.get(7), 'Movie', '2010-07-16', 'English', 'PG-13'),  # Inception
        (movie_id_map.get(4), 'Movie', '1994-09-23', 'English', 'R'),      # Shawshank
        (movie_id_map.get(20), 'Movie', '1972-03-24', 'English', 'R'),     # The Godfather
        (movie_id_map.get(8), 'Movie', '1999-03-31', 'English', 'R'),      # The Matrix
    ]
    
    home_shows = [
        (show_id_map.get(1), 'TV_Show', '2008-01-20', 'English', 'TV-MA'),   # Breaking Bad
        (show_id_map.get(4), 'TV_Show', '2016-07-15', 'English', 'TV-14'),   # Stranger Things
        (show_id_map.get(15), 'TV_Show', '2011-04-17', 'English', 'TV-MA'),  # Game of Thrones
        (show_id_map.get(10), 'TV_Show', '2005-03-24', 'English', 'TV-14'),  # The Office
        (show_id_map.get(17), 'TV_Show', '2019-07-26', 'English', 'TV-MA'),  # The Boys
    ]
    
    for content in home_movies + home_shows:
        if content[0]:  # If content_id exists
            execute_query("INSERT INTO home_page (Content_Id, Content_Type, Release_Date, Language, Age_Rating) VALUES (%s, %s, %s, %s, %s)", content)
    
    print(f"   ✅ Added {len(home_movies) + len(home_shows)} items to home page")
    
    # Show Summary
    print("\n" + "=" * 60)
    print("DATABASE POPULATION SUMMARY")
    print("=" * 60)
    
    users_count = fetch_all("SELECT COUNT(*) as cnt FROM user")[0]['cnt']
    genres_count = fetch_all("SELECT COUNT(*) as cnt FROM genre")[0]['cnt']
    movies_count = fetch_all("SELECT COUNT(*) as cnt FROM movie")[0]['cnt']
    shows_count = fetch_all("SELECT COUNT(*) as cnt FROM tv_show")[0]['cnt']
    profiles_count = fetch_all("SELECT COUNT(*) as cnt FROM profile")[0]['cnt']
    home_count = fetch_all("SELECT COUNT(*) as cnt FROM home_page")[0]['cnt']
    
    print(f"Total Users: {users_count}")
    print(f"Total Genres: {genres_count}")
    print(f"Total Movies: {movies_count}")
    print(f"Total TV Shows: {shows_count}")
    print(f"Total Profiles: {profiles_count}")
    print(f"Total Home Page Items: {home_count}")
    
    print("\n✅ DATABASE POPULATED SUCCESSFULLY!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
