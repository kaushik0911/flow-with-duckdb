SELECT 
    DATE_TRUNC('week', download_date) AS week_start_date,
    version,
    country_code,
    python_version,
    SUM(daily_download_sum) AS weekly_download_sum 
FROM 
    pypi_daily_stats 
GROUP BY 
    ALL
ORDER BY 
    week_start_date