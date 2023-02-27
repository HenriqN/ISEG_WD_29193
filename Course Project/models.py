import sqlite3


def init_db():
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE  IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        registered_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        picture BLOB,
        UNIQUE (username),
        UNIQUE (email)
    );
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        picture BLOB,
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        upvotes INTEGER DEFAULT 0,
        downvotes INTEGER DEFAULT 0
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        upvotes INTEGER DEFAULT 0,
        downvotes INTEGER DEFAULT 0,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS upvote_comments (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        comment_id  INTEGER
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS upvote_posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        post_id  INTEGER
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS downvote_comments (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        comment_id  INTEGER
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS downvote_posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        post_id INTEGER
    )
    ''')

    conn.commit()
    conn.close()


def delete(user_id):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (user_id,))
    c.execute("""
        DELETE FROM posts
        WHERE user_id = ?
    """, (user_id,))
    c.execute("""
        DELETE FROM comments
        WHERE user_id = ?
    """, (user_id,))
    c.execute("""
        DELETE FROM upvote_comments
        WHERE user_id = ?
    """, (user_id,))
    c.execute("""
        DELETE FROM downvote_comments
        WHERE user_id = ?
    """, (user_id,))
    c.execute("""
        DELETE FROM upvote_posts
        WHERE user_id = ?
    """, (user_id,))
    c.execute("""
        DELETE FROM downvote_posts
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()

def downvote_comment(comment_id, user_id):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        SELECT id FROM downvote_comments
        WHERE comment_id = ? and user_id = ?
    """, (comment_id, user_id))
    results = c.fetchone()
    if results:
        c.execute("""
        UPDATE comments
        SET downvotes = downvotes -1
        WHERE id = ?
        """, (comment_id,))
        c.execute("""
        DELETE FROM downvote_comments
        WHERE comment_id = ? and user_id = ? 
        """, (comment_id, user_id))
    else:
        c.execute("""
            UPDATE comments
            SET downvotes = downvotes + 1
            WHERE id = ?
        """, (comment_id,))
        c.execute("""
            INSERT INTO downvote_comments (
            comment_id, user_id)
            values(?, ?)""", (comment_id, user_id))
    conn.commit()
    conn.close()

def downvote_post(post_id, user_id):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        SELECT id FROM downvote_posts
        WHERE post_id = ? and user_id = ?
    """, (post_id, user_id))
    results = c.fetchone()
    if results:
        c.execute("""
        UPDATE posts
        SET downvotes = downvotes -1
        WHERE id = ?
        """, (post_id,))
        c.execute("""
        DELETE FROM downvote_posts
        WHERE post_id = ? and user_id = ? 
        """, (post_id, user_id))
    else:
        c.execute("""
            UPDATE posts
            SET downvotes = downvotes + 1
            WHERE id = ?
        """, (post_id,))
        c.execute("""
            INSERT INTO downvote_posts (
            post_id, user_id)
            values(?, ?)""", (post_id, user_id))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
    SELECT * 
    FROM users """, ())
    users = c.fetchall()
    conn.close()
    return users

def get_comments():
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        SELECT * FROM comments
        ORDER BY comments.timestamp DESC
    """)
    comments = c.fetchall()
    conn.close()
    return comments

def get_posts():
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        SELECT * FROM posts
        ORDER BY posts.created_at DESC
    """)
    posts = c.fetchall()
    conn.close()
    return posts

def get_user(username, email):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
    SELECT * 
    FROM users 
    WHERE username=? 
    OR email=?""", (username, email))
    user = c.fetchone()
    conn.close()
    return user

def get_user_posts(user_id):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        SELECT * FROM posts
        WHERE user_id = ?
        ORDER BY posts.created_at DESC
    """, (user_id,))
    user_posts = c.fetchall()
    conn.close()
    return user_posts

def insert_avatar(user_id, avatar):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        UPDATE users
        SET picture = ?
        WHERE id = ?
        """, (avatar, user_id))
    conn.commit()
    conn.close()

def insert_comment(post_id, user_id, content):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
    INSERT INTO comments (post_id, user_id, content, timestamp, upvotes, downvotes) VALUES (?,?,?,datetime('now'), ?, ?)""",
    (post_id, user_id, content, 0, 0))
    conn.commit()
    conn.close()

def insert_post(user_id, background, content):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
    INSERT INTO posts (user_id, picture, content, upvotes, downvotes) VALUES (?, ?, ?, ?, ?)""",
    (user_id, background , content, 0, 0))
    conn.commit()
    conn.close()

def register_user(username, email, hashed_password):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
    INSERT INTO users (username, email, password)
    VALUES (?,?,?)
    """, (username, email, hashed_password))
    conn.commit()
    conn.close()

def search(search_query):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        SELECT * FROM posts
        WHERE content LIKE ?
        """, ('%' + search_query + '%',))
    results = c.fetchall()
    conn.close()
    return results

def upvote_comment(comment_id, user_id):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        SELECT id FROM upvote_comments
        WHERE comment_id = ? and user_id = ?
    """, (comment_id, user_id))
    results = c.fetchone()
    if results:
        c.execute("""
        UPDATE comments
        SET upvotes = upvotes -1
        WHERE id = ?
        """, (comment_id,))
        c.execute("""
        DELETE FROM upvote_comments
        WHERE comment_id = ? and user_id = ? 
        """, (comment_id, user_id))
    else:
        c.execute("""
            UPDATE comments
            SET upvotes = upvotes + 1
            WHERE id = ?
        """, (comment_id,))
        c.execute("""
            INSERT INTO upvote_comments (
            comment_id, user_id)
            values(?, ?)""", (comment_id, user_id))
    conn.commit()
    conn.close()

def upvote_post(post_id, user_id):
    conn = sqlite3.connect('dtm_network.db')
    c = conn.cursor()
    c.execute("""
        SELECT id FROM upvote_posts
        WHERE post_id = ? and user_id = ?
    """, (post_id, user_id))
    results = c.fetchone()
    if results:
        c.execute("""
        UPDATE posts
        SET upvotes = upvotes -1
        WHERE id = ?
        """, (post_id,))
        c.execute("""
        DELETE FROM upvote_posts
        WHERE post_id = ? and user_id = ? 
        """, (post_id, user_id))
    else:
        c.execute("""
            UPDATE posts
            SET upvotes = upvotes + 1
            WHERE id = ?
        """, (post_id,))
        c.execute("""
            INSERT INTO upvote_posts (
            post_id, user_id)
            values(?, ?)""", (post_id, user_id))
    conn.commit()
    conn.close()



