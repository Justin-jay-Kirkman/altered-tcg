Select DISTINCT c.name->>'en' as en_name, c.rarity, r.rating from cards_card as c
INNER JOIN cards_cardrating as r ON r.card_id_id = c.id
where c.name->>'en' like 'Dr. Frankenstein'
and r.hero_id_id = 'ALT_CORE_B_AX_03_C'