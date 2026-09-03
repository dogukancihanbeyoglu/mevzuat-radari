import subprocess

sql = """SELECT 
    publication_number,
    country_code,
    filing_date,
    grant_date,
    ARRAY_TO_STRING(ARRAY(SELECT name FROM UNNEST(assignee_harmonized)), '; ') AS assignee_name,
    ARRAY_TO_STRING(ARRAY(SELECT code FROM UNNEST(cpc)), '; ') AS cpc_codes,
    (SELECT text FROM UNNEST(title_localized) WHERE language = 'tr' LIMIT 1) AS title_tr,
    (SELECT text FROM UNNEST(title_localized) WHERE language = 'en' LIMIT 1) AS title_en,
    ARRAY_TO_STRING(ARRAY(SELECT publication_number FROM UNNEST(citation)), '; ') AS forward_citations,
    ARRAY_LENGTH(citation) AS total_citations_count
FROM 
    `patents-public-data.patents.publications`
WHERE 
    country_code = 'TR' 
    AND filing_date >= 20100101
ORDER BY 
    filing_date DESC;"""

p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
p.communicate(sql.encode('utf-8'))
print("Correct SQL successfully copied to clipboard with exact table backticks!")
