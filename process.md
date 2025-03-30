ec2에 가상환경이랑 pip패키지 올려놨고, 
gunicorn deploy: ```gunicorn -w 8 URLShortener:create_app()```
mariadb랑 nginx만 세팅하면 됨.

back: api.linkshorty.in
 => 얘 nginx configuration setting 끝.
 => SSL 설정 done.

 
client: linkshorty.in
 => not started.


프론트는 어케 올려야될지 검색