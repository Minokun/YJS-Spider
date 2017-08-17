select 
	yo1.company,yo1.post_date,yo1.position_type,yo1.location,t2.positions,yo1.hr_email,yo1.source,yo1.url
from 
	(select * from yjs_other where id in (SELECT min(id) FROM spider.yjs_other group by company) ) yo1 
	left join 
	(select t1.company,group_concat(t1.position_title) positions from (select yo.company,yo.position_title from yjs_other yo group by yo.company,yo.position_title) t1 group by t1.company) t2 
	on yo1.company = t2.company
order by t2.positions desc