show databases;
use JLPT;
show tables;
select * from grammararticle;
-- ALTER TABLE grammarArticle ADD COLUMN is_sent INTEGER DEFAULT 0;
CREATE INDEX idx_grammarArticle_is_sent ON grammarArticle(is_sent);
CREATE INDEX idx_grammarArticle_level ON grammarArticle(level);

-- 使這些欄位為唯一值，避免有資料重復 
ALTER TABLE grammarArticle ADD UNIQUE (name, webURL, imageURL);

SELECT COUNT(*) FROM grammararticle;

-- 檢查有沒有重複資料，為幾個?
SELECT name, webURL, imageURL, COUNT(*)
FROM grammarArticle
GROUP BY name, webURL, imageURL
HAVING COUNT(*) > 1;

-- 刪除重複資料，"safe updates" 模式的目的是防止誤刪或誤改大量資料，0為解鎖
SET SQL_SAFE_UPDATES = 0; 
DELETE t1 FROM grammarArticle t1
INNER JOIN grammarArticle t2 
WHERE t1.id < t2.id AND t1.name = t2.name AND t1.webURL = t2.webURL AND t1.imageURL = t2.imageURL;
SET SQL_SAFE_UPDATES = 1;


CREATE TABLE grammarArticle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    webURL VARCHAR(255),
    imageURL VARCHAR(255),
    level ENUM('N1', 'N2', 'N3', 'N4', 'N5', 'others'),
    is_sent INTEGER DEFAULT 0
    UNIQUE (name, webURL, imageURL)
)
CREATE INDEX idx_grammarArticle_is_sent ON grammarArticle(is_sent);
CREATE INDEX idx_grammarArticle_level ON grammarArticle(level);

-- 清除目前表中所有資料
TRUNCATE TABLE grammarArticle;

SELECT COUNT(*) FROM grammararticle;