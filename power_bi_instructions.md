# Power BI Dashboard Instructions

1. Open Power BI Desktop.
2. Click **Get data > Text/CSV** and choose `cleaned_netflix.csv` (this file will be produced after running the notebook/script).
3. Create visuals:
   - KPI cards: Total Movies, Total TV Shows, Unique Countries.
   - Bar chart: Top 10 genres (split `listed_in` by comma if needed).
   - Map: Country-wise counts (use 'country' field; you might need to split multi-country rows).
   - Line chart: Number of items added by year (use `date_added_year`).
   - Treemap: Counts by rating.
   - Table: Top directors and their counts.
4. Add slicers for `type`, `rating`, `date_added_year`.
5. Format the report and export as `.pbix` (save locally).
