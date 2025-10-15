select title
from movies
join stars as s1 on movies.id = s1.movie_id
join people as p1 on s1.person_id = p1.id
join stars as s2 on movies.id = s2.movie_id
join people as p2 on s2.person_id = p2.id
where p1.name = 'Bradley Cooper' and p2.name ='Jennifer Lawrence';
