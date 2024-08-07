
DROP VIEW IF EXISTS standard_cards_view;

CREATE VIEW standard_cards_view AS
SELECT
    cl.standard, 
    c.name, 
    c.setCode, 
    cs.releaseDate,
    c.number, 
    c.layout, 
    c.*
FROM cards AS c
JOIN cardLegalities AS cl ON cl.uuid = c.uuid
JOIN cardPurchaseUrls AS cp ON cp.uuid = c.uuid
JOIN sets AS cs ON cs.code = c.setCode
WHERE cl.standard = 'Legal' 
    AND c.isPromo IS NULL 
    AND c.borderColor = 'black' 
    AND c.isReprint IS NULL 
    AND c.promoTypes IS NULL 
ORDER BY c.name ASC, cs.releaseDate ASC, c.power DESC;


WITH ranked_cards AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY name ORDER BY releaseDate ASC, power DESC) AS rn
    FROM standard_cards_view
)
SELECT
    name, 
    setCode, 
    releaseDate,
    number, 
    layout,
    "availability",
    power, toughness,
    colorIdentity, colors,
    types, subtypes, supertypes,
    manaCost, manaValue,
    edhrecRank, edhrecSaltiness,
    "text", flavorText
FROM ranked_cards
WHERE rn = 1
ORDER BY name ASC;

