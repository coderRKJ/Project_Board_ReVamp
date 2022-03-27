import os
import sys

from Project_Board_ReVamp.Project_Board_ReVamp import app, create_user

# running the site
if __name__ == '__main__':

    # creating db if it doesn't exist
    if not os.path.exists('./Project_Board_ReVamp/Project_Board_ReVampDatabase.sqlite3'):
        create_user()

    # run this command with any additional arg to run in production
    if len(sys.argv) > 1:
        print('<< PROD >>')
        os.system(f"gunicorn -b '127.0.0.1:{app.config['PORT']}' app:app")
    # or just run without an additional arg to run in debug
    else:
        print('<< DEBUG >>')
        app.run(debug=True)
