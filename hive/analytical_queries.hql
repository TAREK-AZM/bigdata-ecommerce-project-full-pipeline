-- 1. Top 10 produits les plus achetés
SELECT product_id, category, SUM(quantity) as total_sold
FROM purchases
WHERE event_date = '${hiveconf:target_date}'
GROUP BY product_id, category
ORDER BY total_sold DESC
LIMIT 10;

-- 2. Taux de conversion : (Nb Achats / Nb Sessions Uniques) par catégorie
WITH sessions AS (
  SELECT category, COUNT(DISTINCT session_id) as total_sessions
  FROM clicks
  WHERE event_date = '${hiveconf:target_date}'
  GROUP BY category
),
sales AS (
  SELECT category, COUNT(*) as total_sales
  FROM purchases
  WHERE event_date = '${hiveconf:target_date}'
  GROUP BY category
)
SELECT 
  s.category, 
  s.total_sessions, 
  COALESCE(sales.total_sales, 0) as sales,
  (COALESCE(sales.total_sales, 0) / s.total_sessions) * 100 as conversion_rate
FROM sessions s
LEFT JOIN sales ON s.category = sales.category
ORDER BY conversion_rate DESC;

-- 3. Analyse du parcours client (Funnel)
-- Combien de sessions ont visité: Home -> Product -> Cart -> Checkout
SELECT 
  COUNT(DISTINCT c1.session_id) as home_visits,
  COUNT(DISTINCT c2.session_id) as product_visits,
  COUNT(DISTINCT c3.session_id) as cart_visits,
  COUNT(DISTINCT c4.session_id) as checkout_visits
FROM clicks c1
LEFT JOIN clicks c2 ON c1.session_id = c2.session_id AND c2.page_url = '/product'
LEFT JOIN clicks c3 ON c1.session_id = c3.session_id AND c3.page_url = '/cart'
LEFT JOIN clicks c4 ON c1.session_id = c4.session_id AND c4.page_url = '/checkout'
WHERE c1.page_url = '/home' 
  AND c1.event_date = '${hiveconf:target_date}';
