select 
	t3.company,t3.company_type,t3.company_size,t3.industry,t3.valid_date,t3.position_type,t3.location,t2.positions,t3.company_site,t3.url
from 
	(select * from spider.yjs_self where id in (select min(id) from spider.yjs_self group by company)) t3 
	left join 
	(select t1.company,group_concat(t1.position_num) positions from (SELECT *,concat("  ",position_title,":",recruit_num,"人") position_num FROM spider.yjs_self) t1 group by t1.company) t2 
	on t3.company = t2.company