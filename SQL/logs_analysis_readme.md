# News Site Log Analysis Tool

Author: Clara Penn

## Summary

This is a reporting tool that reports on data in a specific PostgreSQL **news** database.

It prints out in plain text the answers to three different questions about the data, relating to the site's user activity.

The three questions about user activity on the news website that this device answers are:

1. What are the most popular three articles of all time?

2. Who are the most popular article authors of all time?

3. On which days did more than 1% of requests lead to errors?


### Design notes

The tool is a Python program using the psycopg2 module to connect to the database.
It uses SQL views, which it automatically adds to the database itself.


## Installation

This needs to be run on a machine with:
* Python 2.7
* PostgreSQL running the `news` database.

Copy the `logs_analysis.py` file to your machine.

The file can be run from any directory.


### Usage

1. Open a new terminal/shell.

2. `cd` to the location you downloaded `logs_analysis.py` to

3. Run the program from the shell using the `python` command as follows:

`$ python logs_analysis.py`

The program will output its results as plain text in your terminal. See `output.txt` for an example.


### SQL views

The code relies on views created in the database - however, these views are created by dedicated Python functions within the program, so that the program stands alone and the user does not need to create the views prior to running the tool.

For reference only, here are the views created within the program, upon which the SQL queries depend:

* __The view for question 1 is:__

```
    CREATE OR REPLACE VIEW top_three_articles AS
    SELECT articles.slug, count(slug) AS total_views
    FROM articles
    JOIN log ON log.path LIKE CONCAT ('%', articles.slug)
    GROUP BY slug
    ORDER BY total_views desc
    LIMIT 3;
```

* __The views for question 2 are:__

```
    CREATE OR REPLACE VIEW ranked_articles AS
    SELECT articles.slug, count(slug)
    AS total_views FROM articles
    JOIN log ON log.path LIKE CONCAT ('%', articles.slug)
    GROUP BY slug
    ORDER BY total_views desc;
```

```
    CREATE OR REPLACE VIEW popular_authors AS
    SELECT articles.author, sum(ranked_articles.total_views)
    AS summed_total_views
    FROM articles JOIN ranked_articles
    ON articles.slug = ranked_articles.slug
    GROUP BY author
    ORDER BY summed_total_views DESC;
```

* __The views for question 3 are:__

```
    CREATE OR REPLACE VIEW logs_by_date AS
    SELECT time::date,  COUNT(*)
    AS total_requests FROM log
    GROUP BY time::date;
```

```
    CREATE OR REPLACE VIEW errors_by_date AS
    SELECT time::date, COUNT(*)
    AS total_errors
    FROM log WHERE status='404 NOT FOUND'
    GROUP BY time::date
    ORDER BY time;
```

```
    CREATE OR REPLACE VIEW all_results AS
    SELECT logs_by_date.time, logs_by_date.total_requests, errors_by_date.total_errors
    FROM errors_by_date join logs_by_date
    ON errors_by_date.time = logs_by_date.time;
```

