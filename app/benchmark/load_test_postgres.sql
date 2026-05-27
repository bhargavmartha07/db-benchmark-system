SELECT

    u.cohort_month,

    u.user_id,

    COUNT(e.event_id) AS total_events

FROM users u

JOIN sessions s
    ON u.user_id = s.user_id

JOIN events e
    ON s.session_id = e.session_id

GROUP BY
    u.cohort_month,
    u.user_id

ORDER BY total_events DESC

LIMIT 10;