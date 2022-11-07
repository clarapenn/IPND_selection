#!/usr/bin/env python2.7

import psycopg2


def question_one():
    '''This function prints the answer to the question:
    What are the most popular three articles of all time?'''
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    view_setup_sql = """
    CREATE OR REPLACE VIEW top_three_articles AS
    SELECT articles.slug, count(slug) AS total_views
    FROM articles
    JOIN log ON log.path LIKE CONCAT ('%', articles.slug)
    GROUP BY slug
    ORDER BY total_views desc
    LIMIT 3;
    """
    cursor.execute(view_setup_sql)

    query = """
    SELECT title, total_views
    FROM articles JOIN top_three_articles
    ON articles.slug = top_three_articles.slug
    ORDER BY total_views desc;
    """
    cursor.execute(query)

    results = cursor.fetchall()
    conn.close()

    print("\nThe most popular three articles are:")

    for result in results:
        print("{title} -- {total} views".format(
            title=result[0],
            total=result[1]
        ))


def question_two():
    '''This function prints the answer to the question: Who are the
    most popular article authors of all time?'''
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    view_setup_sql = """
    CREATE OR REPLACE VIEW ranked_articles AS
    SELECT articles.slug, count(slug)
    AS total_views FROM articles
    JOIN log ON log.path LIKE CONCAT ('%', articles.slug)
    GROUP BY slug
    ORDER BY total_views desc;
    """
    cursor.execute(view_setup_sql)

    view_setup_sql = """
    CREATE OR REPLACE VIEW popular_authors AS
    SELECT articles.author, sum(ranked_articles.total_views)
    AS summed_total_views
    FROM articles JOIN ranked_articles
    ON articles.slug = ranked_articles.slug
    GROUP BY author
    ORDER BY summed_total_views DESC;
    """
    cursor.execute(view_setup_sql)

    query = """
    SELECT authors.name, authors.id, popular_authors.summed_total_views
    FROM authors
    JOIN popular_authors
    ON authors.id = popular_authors.author;
    """
    cursor.execute(query)

    results = cursor.fetchall()
    conn.close()

    print("\nThe most popular authors are:")

    for result in results:
        print("{name} -- {total} views".format(
            name=result[0],
            total=result[2]
        ))


def question_three():
    '''This function prints the answer to the question On which
    days did more than 1% of requests lead to errors?'''
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    view_setup_sql = """
    CREATE OR REPLACE VIEW logs_by_date AS
    SELECT time::date,  COUNT(*)
    AS total_requests FROM log
    GROUP BY time::date;
    """
    cursor.execute(view_setup_sql)

    view_setup_sql = """
    CREATE OR REPLACE VIEW errors_by_date AS
    SELECT time::date, COUNT(*)
    AS total_errors
    FROM log WHERE status='404 NOT FOUND'
    GROUP BY time::date
    ORDER BY time;
    """
    cursor.execute(view_setup_sql)

    view_setup_sql = """
    CREATE OR REPLACE VIEW all_results AS
    SELECT
        logs_by_date.time,
        logs_by_date.total_requests,
        errors_by_date.total_errors
    FROM errors_by_date JOIN logs_by_date
    ON errors_by_date.time = logs_by_date.time;
    """
    cursor.execute(view_setup_sql)

    query = """
    SELECT time, percent FROM
    (SELECT
        time,
        total_errors,
        total_requests,
        ROUND(total_errors * 100.0 / total_requests,
        1
    )
    AS Percent
    FROM all_results ORDER BY percent desc)
    AS threshold_exceeded WHERE percent > 1.0;
    """
    cursor.execute(query)

    most_errors = cursor.fetchall()
    conn.close()

    print(
        "\nThe days on which more than 1 "
        "per cent of requests led to errors are:"
    )

    for error_result in most_errors:
        the_date = error_result[0]
        percent = error_result[1]
        print("{date} -- {percent}% errors".format(
            date=the_date.strftime("%B %d, %Y"),
            percent=percent
        ))


def run_reports():
    question_one()
    question_two()
    question_three()


if __name__ == "__main__":
    run_reports()
