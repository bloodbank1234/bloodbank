import Database

# Connect to the database
con = Database.connect()
cur = con.cursor()

# Creating tables
cur.execute("""
    CREATE TABLE IF NOT EXISTS total_units (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blood_group TEXT DEFAULT NULL,
        no_of_units TEXT DEFAULT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS blood_alert (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hsp_id TEXT DEFAULT NULL,
        blood_type TEXT DEFAULT NULL,
        contact TEXT DEFAULT NULL,
        description TEXT DEFAULT NULL,
        donor_name TEXT,
        donor_mobile TEXT,
        status TEXT DEFAULT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS donation_request (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hsp TEXT DEFAULT NULL,
        name TEXT DEFAULT NULL,
        email TEXT DEFAULT NULL,
        disease TEXT DEFAULT NULL,
        blood_type TEXT DEFAULT NULL,
        b_unites TEXT DEFAULT NULL,
        r_date TEXT DEFAULT NULL,
        status TEXT DEFAULT NULL,
        age TEXT DEFAULT NULL,
        gender TEXT DEFAULT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS donor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        f_name TEXT DEFAULT NULL,
        email TEXT DEFAULT NULL,
        mobile TEXT DEFAULT NULL,
        password TEXT DEFAULT NULL,
        otp TEXT DEFAULT NULL,
        blood_type TEXT DEFAULT NULL,
        address TEXT DEFAULT NULL,
        status TEXT DEFAULT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hsp_id TEXT DEFAULT NULL,
        email TEXT DEFAULT NULL,
        mobile TEXT DEFAULT NULL,
        date_feed TEXT DEFAULT NULL,
        overall_service TEXT DEFAULT NULL,
        request_handling TEXT DEFAULT NULL,
        description TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS hospital (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact TEXT,
        email TEXT,
        address TEXT,
        password TEXT,
        status TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS patient_request (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hsp_id TEXT DEFAULT NULL,
        b_group TEXT DEFAULT NULL,
        p_name TEXT DEFAULT NULL,
        contact TEXT DEFAULT NULL,
        address TEXT DEFAULT NULL,
        status TEXT DEFAULT NULL
    )
""")

# Commit changes and close the connection
con.commit()
con.close()

