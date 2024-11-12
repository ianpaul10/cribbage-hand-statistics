## TODOs

- add a readme (lol)
- fetch hand spread directly from the csv/parquet, or figure out a way to load from the big boi parquet with the output display
- image upload
- impage upload with camera
- nicer display of the data
- deployment/ci/cd

## Ideas to write/reference in the future

- DuckDB. Why an OLAP DB is good for this use case
- what data to store vs query in real-time b/c we're using a file db (I think DuckDB is like SQLite in that way?). e.g. all hand results vs just all points for given 4 card + crib hand
- optimal query patterns for getting all combos of a certain set
- duck db load directly from s3 bucket
