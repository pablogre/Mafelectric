cd\
cd C:\xampp\mysql\bin

SET hora=%date:~5,2%%date:~8,2%%date:~11,4%%time:~0,2%
%hora% 
mysqldump -uroot -pcl1v2%2605 taller > C:\taller\taller_bak%hora%.sql

mysqldump -uroot -pcl1v2%2605 taller > C:\Users\pablo\OneDrive\Desktop\PLATZI\PYTHON\TALLER\taller_bak%hora%.sql

mysqldump -uroot -pcl1v2%2605 --all-databases > C:\Users\pablo\OneDrive\Desktop\PLATZI\PYTHON\TALLER\mysql_backup%hora%.sql

