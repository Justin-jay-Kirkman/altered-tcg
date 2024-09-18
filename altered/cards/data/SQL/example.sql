Select DISTINCT c.name->>'en' as en_name, c.rarity, r.rating from cards_card as c
INNER JOIN cards_cardrating as r ON r.card_id_id = c.id
where c.name->>'en' like 'Dr. Frankenstein'
and r.hero_id_id = 'ALT_CORE_B_AX_03_C'



Select name->'en',* from cards_cardrating as r
JOIN cards_card as c on c.id = r.card_id_id
where hero_id_id = 'ALT_CORE_B_OR_03_C'
AND card_id_id = 'ALT_CORE_B_OR_08_C'
limit 5

Select name->'en',* from cards_cardrating as r
JOIN cards_card as c on c.id = r.card_id_id
where hero_id_id in ('ALT_COREKS_B_OR_01_C','ALT_COREKS_B_OR_03_C','ALT_COREKS_B_OR_02_C',
  'ALT_CORE_B_OR_01_C','ALT_CORE_B_OR_03_C','ALT_CORE_B_OR_02_C')
limit 5

delete from cards_cardrating
where hero_id_id in ('ALT_COREKS_B_OR_01_C','ALT_COREKS_B_OR_03_C','ALT_COREKS_B_OR_02_C',
  'ALT_CORE_B_OR_01_C','ALT_CORE_B_OR_03_C','ALT_CORE_B_OR_02_C')