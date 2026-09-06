-- 1. Best topics by engagement
SELECT topic, ROUND(AVG(engagement_rate_pct),2) AS avg_engagement,
       ROUND(AVG(viral_coefficient),3) AS avg_viral
FROM content_performance
GROUP BY topic ORDER BY avg_viral DESC;

-- 2. Best content format
SELECT format, COUNT(*) AS posts, ROUND(AVG(engagement_rate_pct),2) AS avg_engagement
FROM content_performance GROUP BY format ORDER BY avg_engagement DESC;

-- 3. Save-to-share ratio by topic
SELECT topic, ROUND(AVG(save_to_share_ratio),2) AS save_share_ratio
FROM content_performance GROUP BY topic ORDER BY save_share_ratio DESC;

-- 4. Top 20 viral posts
SELECT content_id, topic, platform, shares, saves, retention_rate, viral_coefficient
FROM content_performance ORDER BY viral_coefficient DESC LIMIT 20;

-- 5. Monthly follower growth
SELECT DATE_FORMAT(date,'%Y-%m') AS month, SUM(followers_gained) AS followers_gained
FROM content_performance GROUP BY month ORDER BY month;

-- 6. Relatable comments per topic
SELECT c.topic, COUNT(*) AS relatable_comments
FROM content_performance c
JOIN user_comments u ON c.content_id = u.content_id
WHERE LOWER(u.comment_text) REGEXP 'relatable|only one|same|needed this|understood|put.*words'
GROUP BY c.topic ORDER BY relatable_comments DESC;
