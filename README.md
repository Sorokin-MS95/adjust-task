# Sample Task
#### General information
This is a demo app to expose the sample dataset using Django REST framework.

#### Installation instuctions

1. Create and activate virtual environment
    ```
    virtualenv --python=python3 venv
    source venv/bin/activate
    ```
    **Note**: You can have another `python*` binary in your OS.

2. Install application requirements and change working directory
    ```
    pip install -r requirements.txt
    cd app
    ```
3. Create new .env file with the following content
    ```
    APP_HOSTNAME={hostname}
    DEBUG=yes
    SECRET_KEY={secret_key}
    DEFAULT_DATABASE_URL={db_url}
    ```
    Where: 
        - {hostname} is your hostname.
        - {secret_key} is you application secret key.
        - {db_url} is a database url in format: sqlite:///some_path/db.sqlite3**
        Note: is no DEFAULT_DATABASE_URL is provided, sqlite3 will be used by default. 
        
4. Run migrations. This will insert sample dataset into database. 
    ```
    python manage.py migrate
    ```
5. Start the development server to test API
    ```
    python manage.py runserver
    ```
    
#### API Usage
To retrieve performance metrics send **GET /api/metrics** request.

The following GET parameters are accepted:

Date params:
- `date_from` - date string in format "%d.%m.%Y" to apply date__gte filter.
- `date_to` - date string in format "%d.%m.%Y" to apply date__lte filte.r
- `date` - date string in format "%d.%m.%Y" to filter by date.

String params:
- `channel` - string or list of channels to apply OR channel__iexact filter.
- `country` - string or list of countries to apply OR country__iexact filter.
- `os` - string or list of os to apply OR os__iexact filter.

Ordering:
- `order` - string or a list of fields in format (-?)field_name to apply DESC or ASC ordering.

Grouping:
- `group` - string or a list of fields to execute GROUP BY statement


#### Use-cases
1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.
**GET /api/metrics?date_to=01.06.2017&order=-clicks&group=country&group=channel**

2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
**GET /api/metrics?date_from=01.05.2017&date_to=31.05.2017&order=date&group=date**

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.
**GET /api/metrics?date=01.06.2017&order=-revenue&group=os**

4. Show CPI values for Canada (CA) broken down by channel ordered by CPI in descending order.
**GET /api/metrics?country=CA&order=-cpi&group=channel**
