Open your browser and go to http://localhost:5050
Login with:
Email: admin@admin.com
Password: admin
After logging in, right-click on "Servers" in the left panel and select "Create > Server"
In the "General" tab, give your connection a name like "Weather Database"
In the "Connection" tab, enter:
Host: db (use the service name from docker-compose)
Port: 5432
Database: weather_data
Username: user
Password: password
Click "Save"