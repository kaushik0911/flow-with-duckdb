---
title: DuckDB 🦆 - Python 🐍 downloads
---


## How Many People Downloaded DuckDB ?

<BigValue 
    title='Last week downloads'
    data={download_last_week} 
    value='weekly_downloads' 
    fmt='#,##0.00,,"M"'	
/>

<BigValue 
    title='Last month downloads'
    data={download_last_month} 
    value='monthly_downloads' 
    fmt='#,##0.00,,"M"'	
/>

<BigValue 
    title='Total download'
    data={count_over_month} 
    value='weekly_download_sum' 
    fmt='#,##0.00,,"M"'	
/>

## Download Over Months
<Grid cols=2>
<LineChart data = {download_week} y=weekly_downloads x=week_start_date  />

<DataTable data="{download_last_6_months}" search="false">
    <Column id="month_start_date" title="Month Start Date"/>
    <Column id="monthly_downloads" title="Monthly Downloads" />
</DataTable>
</Grid>

## Downloads by DuckDB and Python Version in the Last 30 Days
<Grid cols=2>
    <BarChart 
        data={download_duckdb_version}
        x=duckdb_version
        y=total_downloads 
        swapXY=true
    />
    <BarChart 
        data={download_python_version}
        x=python_version
        y=total_downloads 
        swapXY=true
    />
</Grid>

## Top 10 Countries Downloading DuckDB in the Last 30 Days

<BarChart 
    data={download_country}
    x=country_code
    y=total_downloads 
    swapXY=true
/>

```sql count_over_month
SELECT  SUM(weekly_download_sum) as weekly_download_sum
FROM weekly_download
```

```sql download_month
SELECT 
    DATE_TRUNC('month', week_start_date) AS month_start_date,
    SUM(weekly_download_sum) AS monthly_downloads
FROM weekly_download
GROUP BY 
    month_start_date
ORDER BY 
    month_start_date DESC
```

```sql download_last_6_months
select * from ${download_month} limit 6
```

```sql download_week 
SELECT 
    week_start_date,
    SUM(weekly_download_sum) AS weekly_downloads
FROM 
    weekly_download
WHERE 
    week_start_date != (SELECT week_start_date FROM ${last_4_weeks} LIMIT 1) -- skipping the current week as it's not complete
GROUP BY 
    week_start_date
ORDER BY 
    week_start_date DESC
 
```

```sql download_last_month
SELECT 
    month_start_date, 
    monthly_downloads
FROM 
    ${download_month}
WHERE 
    month_start_date = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
```

```sql download_last_week
SELECT 
    week_start_date, 
    weekly_downloads
FROM 
    ${download_week}
WHERE 
    week_start_date IN (SELECT week_start_date FROM ${last_4_weeks} OFFSET 1 LIMIT 1)
LIMIT 1
```

```sql last_4_weeks
SELECT DISTINCT week_start_date
FROM 
    weekly_download
WHERE 
    week_start_date >= DATE_TRUNC('week', CURRENT_DATE - INTERVAL '4 weeks')
ORDER BY 
    week_start_date DESC
```

```sql download_duckdb_version
SELECT 
    version AS duckdb_version,
    SUM(weekly_download_sum) AS total_downloads
FROM 
    weekly_download
WHERE 
    week_start_date IN (SELECT week_start_date FROM ${last_4_weeks})
GROUP BY 
    version
ORDER BY 
    total_downloads DESC
limit 10
```

```sql download_python_version
SELECT 
    python_version,
    SUM(weekly_download_sum) AS total_downloads
FROM 
    weekly_download
WHERE 
    week_start_date IN (SELECT week_start_date FROM ${last_4_weeks})
GROUP BY 
    python_version
ORDER BY 
    total_downloads DESC
limit 10
```

```sql download_country
SELECT 
    country_code,
    SUM(weekly_download_sum) AS total_downloads
FROM 
    weekly_download
WHERE 
    week_start_date IN (SELECT week_start_date FROM ${last_4_weeks})
GROUP BY 
    country_code
ORDER BY 
    total_downloads DESC
limit 10
```