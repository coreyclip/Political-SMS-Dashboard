DROP TABLE IF EXISTS PoliticalTexts; -- table to export

CREATE Table PoliticalTexts AS 
select m.ROWID,
h.id AS SenderPhonNumber, 
m.text, 
m.subject, 
m.country,
m.attributedBody,
m.type,
m.[date], 
m.date_delivered
from handle h
INNER JOIN chat_handle_join chj
ON h.ROWID = chj.handle_id
INNER JOIN chat_message_join cmj 
ON chj.chat_id = cmj.chat_id
INNER JOIN message m 
ON cmj.message_id = m.ROWID
where h.id IN (88022, 52005, 43367) -- sender phone number 
;
