# healthblog

create a file named "var.env" with following environment varbiales in folder healthblog/app: (this will be used for the app and database credentials)

SECRET_KEY=secret

DATABASE_URL=mysql+pymysql://"user":"password"@"containername db"/"db name" (make sure the credentials in the file docker-compose.yml matches)

FLASK_APP=healthblog.py

unzip file "ib_logfile0.zip" in folder db/ before you start docker-compose
