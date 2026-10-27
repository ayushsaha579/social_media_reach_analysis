-- Run against data/social_media_analytics.db after `python src/etl.py`.

-- 1. Overall KPI summary
SELECT COUNT(*) AS posts,
       SUM(reach) AS total_reach,
       SUM(impressions) AS total_impressions,
       SUM(total_engagement) AS total_engagement,
       ROUND(AVG(engagement_rate_pct), 2) AS avg_engagement_rate_pct
FROM posts;

-- 2. Platform performance
SELECT platform, COUNT(*) AS posts, SUM(reach) AS total_reach,
       SUM(impressions) AS impressions, SUM(total_engagement) AS engagement,
       ROUND(AVG(engagement_rate_pct), 2) AS avg_engagement_rate_pct
FROM posts GROUP BY platform ORDER BY total_reach DESC;

-- 3. Content-type performance
SELECT content_type, COUNT(*) AS posts, SUM(reach) AS total_reach,
       ROUND(AVG(engagement_rate_pct), 2) AS avg_engagement_rate_pct
FROM posts GROUP BY content_type ORDER BY avg_engagement_rate_pct DESC;

-- 4. Day-of-week performance
SELECT post_day, COUNT(*) AS posts,
       ROUND(AVG(engagement_rate_pct), 2) AS avg_engagement_rate_pct
FROM posts GROUP BY post_day ORDER BY avg_engagement_rate_pct DESC;

-- 5. Monthly reach trend
SELECT post_month, SUM(reach) AS total_reach, SUM(total_engagement) AS total_engagement
FROM posts GROUP BY post_month ORDER BY post_month;

-- 6. Top 10 posts by reach
SELECT post_id, post_date, platform, content_type, topic, reach, impressions,
       total_engagement, engagement_rate_pct
FROM posts ORDER BY reach DESC LIMIT 10;

-- 7. Sentiment mix
SELECT sentiment, COUNT(*) AS posts,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM posts), 2) AS share_pct
FROM posts GROUP BY sentiment ORDER BY posts DESC;

-- 8. Hashtag count bands
SELECT CASE WHEN hashtags_count = 0 THEN '0'
            WHEN hashtags_count BETWEEN 1 AND 3 THEN '1-3'
            WHEN hashtags_count BETWEEN 4 AND 7 THEN '4-7'
            ELSE '8+' END AS hashtag_band,
       COUNT(*) AS posts, ROUND(AVG(engagement_rate_pct), 2) AS avg_rate
FROM posts GROUP BY hashtag_band ORDER BY posts DESC;
