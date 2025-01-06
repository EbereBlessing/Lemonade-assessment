# Lemonade-assessment
# SECTION 2 - Coding Challenge
## HOW TO RUN RABBITMQ EXPORTER
- Install the required Python libraries: pip install requirements.txt
- Update the .env file to set the required environment variable
- Run the script - python exporter.py
## HOW TO RUN THE LARAVEL BACKEND SERVICE bASH SCRIPT
- Make the script executable: chmod +x script.sh
- Run the script: ./script.sh

## A Postgres query is running slower than expected. Explain your approach to troubleshooting it.
- Use EXPLAIN (ANALYZE) to identify slow operations like sequential scans, expensive joins, or disk spill
- Ensure appropriate indexes exist and are used in the query.
- Simplify the query, refine WHERE clauses, and avoid unnecessary joins or aggregations.
- Run ANALYZE or VACUUM ANALYZE to ensure accurate query planning.
- Check for locks, high system load, or disk I/O issues (pg_stat_activity, pg_locks).
- Increase work_mem or enable parallel queries for resource-intensive operations.
- Enable pg_stat_statements or query logging (log_min_duration_statement) to find slow queries. 

## Write a Dockerfile to containerize a Laravel application.
