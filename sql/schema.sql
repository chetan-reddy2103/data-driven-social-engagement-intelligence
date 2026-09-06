CREATE DATABASE IF NOT EXISTS social_engagement;
USE social_engagement;

CREATE TABLE content_performance (
    content_id VARCHAR(20) PRIMARY KEY,
    date DATE,
    platform VARCHAR(30),
    topic VARCHAR(100),
    format VARCHAR(30),
    hook VARCHAR(30),
    caption_style VARCHAR(50),
    video_length_sec INT,
    impressions INT,
    followers_before INT,
    likes INT,
    comments INT,
    shares INT,
    saves INT,
    retention_rate DECIMAL(6,4),
    followers_gained INT,
    engagement_rate_pct DECIMAL(8,3),
    save_to_share_ratio DECIMAL(10,3),
    viral_coefficient DECIMAL(10,4),
    viral_score DECIMAL(10,6),
    viral_label VARCHAR(20)
);

CREATE TABLE user_comments (
    comment_id VARCHAR(20) PRIMARY KEY,
    content_id VARCHAR(20),
    comment_text TEXT,
    created_at DATETIME,
    FOREIGN KEY (content_id) REFERENCES content_performance(content_id)
);

CREATE INDEX idx_content_topic ON content_performance(topic);
CREATE INDEX idx_content_date ON content_performance(date);
CREATE INDEX idx_comments_content ON user_comments(content_id);
