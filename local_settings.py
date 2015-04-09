
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "3cf42d69-e1fc-4135-9cc2-10255fb7672ccc2c4aba-aab6-43fd-ae75-07af402f8e2a72e08c6c-8595-417a-9d39-7b0967db10e1"
NEVERCACHE_KEY = "ffa77281-4a6b-4544-9a34-2c66e2e8b11b52d01b79-11b0-4c62-a40c-c9c3ac2521c2ddfe54c7-ed48-4525-8296-45c164cae390"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}
