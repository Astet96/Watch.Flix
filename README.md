App description:
This app searches the IMdb database un order to reccomend a movie to watch.
There are two search options:
    1. Criteria Search: in which up to 8 criteria can be used to find a suitable movie/show to watch, these are:
        a. type: movie or tv series
        b. period: decade from 1900 to 2020
        c. genre
        d. rating: 1 - 10 stars
        e. actor *optional
        f. director *optional
        g. producer *optional
        h. country
    2: A random search that returns a title to watch

The result page displays the name of the title as a link to the IMdb page
for that movie/show, as well as the associated poster (if any)

If no titles are found that satisfy the search criteria, then an apology
is rendered

Finally, there is a history tab, presenting the titles (as links to IMdb pages) of the most recent 10 search results

Additional python apps:
csv_downloader.py - is used to download the IMdb TSV files
csv_db_converter.py - is used to convert the downloaded TSV diles into a SQLite3 database
pop_row.py - is used to create a new (lighter) database from the previously created one in order to shorten the search time
qry_constructor.py - has the SQLite3 query construction logic that powers the main search functionality
img.py - is used to retreive the associated title poster for display in the result page.