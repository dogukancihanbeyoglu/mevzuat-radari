-- ========================================================================================
-- GOOGLE PATENTS PUBLIC DATASET (BIGQUERY) — SAVUNMA SANAYİİ VE SİVİL ATIF ÇEKME SORGUSU
-- Veritabanı: `patents-public-data.patents.publications`
-- Amaç: 6 Savunma Yüklenicisinin (ASELSAN, TUSAŞ, ROKETSAN, HAVELSAN, STM, BAYKAR)
--       tüm patentlerini ve bu patentlere sivil sektörlerden gelen gerçek ileri atıfları çekmek.
-- ========================================================================================

WITH DefensePatents AS (
    SELECT
        p.publication_number AS defense_patent_id,
        p.application_number AS defense_app_num,
        p.filing_date AS defense_filing_date,
        p.grant_date AS defense_grant_date,
        p.country_code AS defense_country,
        app.name AS defense_assignee,
        -- Ana IPC Teknolojik Sınıfı (İlk 4 hane, örn: G01S, H04B, B64U, G06T)
        SUBSTR(ipc.code, 1, 4) AS primary_ipc_class,
        c.publication_number AS citing_patent_id
    FROM
        `patents-public-data.patents.publications` p,
        UNNEST(p.assignee_harmonized) app,
        UNNEST(p.ipc) ipc,
        UNNEST(p.citation) c
    WHERE
        -- Türkiye menşeili veya uluslararası tescilli 6 ana savunma yüklenicisi
        (
            app.name LIKE '%ASELSAN%' OR
            app.name LIKE '%TUSAS%' OR
            app.name LIKE '%TURK HAVACILIK%' OR
            app.name LIKE '%ROKETSAN%' OR
            app.name LIKE '%HAVELSAN%' OR
            app.name LIKE '%SAVUNMA TEKNOLOJILERI MUHENDISLIK%' OR
            app.name LIKE '%STM SAVUNMA%' OR
            app.name LIKE '%BAYKAR%'
        )
        AND p.filing_date >= 20050101
)
SELECT
    dp.defense_patent_id,
    dp.defense_filing_date,
    dp.defense_grant_date,
    dp.defense_assignee,
    dp.primary_ipc_class,
    dp.citing_patent_id,
    citing_pub.filing_date AS citation_filing_date,
    EXTRACT(YEAR FROM PARSE_DATE('%Y%m%d', CAST(citing_pub.filing_date AS STRING))) AS citation_year,
    citing_app.name AS citing_assignee_name,
    citing_pub.country_code AS citing_country,
    -- Sivil Sektör Sınıflandırması (Cross-matching)
    CASE
        WHEN citing_app.name LIKE '%FORD%' OR citing_app.name LIKE '%TOFAS%' OR citing_app.name LIKE '%OTOKAR%' OR citing_app.name LIKE '%MAN%' THEN 'Otomotiv'
        WHEN citing_app.name LIKE '%TURKCELL%' OR citing_app.name LIKE '%TURK TELEKOM%' OR citing_app.name LIKE '%NETAS%' THEN 'Telekomunikasyon'
        WHEN citing_app.name LIKE '%ARCELIK%' OR citing_app.name LIKE '%BEKO%' OR citing_app.name LIKE '%VESTEL%' THEN 'Tuketici_Elektronigi'
        WHEN citing_app.name LIKE '%KORDSA%' OR citing_app.name LIKE '%SISECAM%' OR citing_app.name LIKE '%PETKIM%' THEN 'Ileri_Malzeme_Kimya'
        ELSE 'Diger_Sivil_Sanayi'
    END AS civilian_sector_group
FROM
    DefensePatents dp
INNER JOIN
    `patents-public-data.patents.publications` citing_pub ON dp.citing_patent_id = citing_pub.publication_number
LEFT JOIN
    UNNEST(citing_pub.assignee_harmonized) citing_app
WHERE
    citing_pub.filing_date >= 20050101
ORDER BY
    citation_year DESC, dp.defense_assignee ASC;
