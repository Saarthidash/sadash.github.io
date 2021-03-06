import psycopg2

def appconnection():
	try:
		con = psycopg2.connect(user="postgres",
		                       password="selfCompassion",
		                       host="34.93.183.58",
		                       port="5432",
		                       database="postgres")
		con.autocommit = True
#		print(con.get_dsn_parameters(), "n")
		print("App Database Connected =  True")
		return con
	except (Exception, psycopg2.Error) as error:
		print("App Database Connected =  False")
		print("Error while connecting to PostgreSQL", error)

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################


con1=appconnection()
def new_user():
	try:
		query = con1.cursor()
		query.execute('SELECT DATE(u."createdAt"),COUNT(*) FROM public."User" AS u GROUP BY DATE(u."createdAt") ORDER BY DATE(u."createdAt") ASC')
		new_user_count = query.fetchall()
		#print(new_user_count)
		return new_user_count
	except:
		return 0
        
print("new_user done")
#############################################################################################################################
con2=appconnection()
def submit():
	try:
		query = con2.cursor()
		query.execute('SELECT date1_,new_user_submit,all_user_submit FROM(SELECT DATE(c."date") as date1_,COUNT(*) as all_user_submit  FROM public."ContestParticipants" as c WHERE c."isSubmitted"=\'{}\'  GROUP BY DATE(c."date")ORDER BY DATE(c."date")) as t1 INNER JOIN(SELECT DATE(c."date") as date2_,COUNT(*) AS new_user_submit FROM public."ContestParticipants" as c INNER JOIN public."User" as u ON u.id = c."studentId" WHERE c."isSubmitted" = \'{}\'  AND DATE(u."createdAt")=DATE(c."date") GROUP BY DATE(c."date") ORDER BY DATE(c."date")) as t2  on t1.date1_ = t2.date2_ '.format("true","true"))
		submitted = query.fetchall()
		#print(submitted)
		return submitted
	except:
		return 0
submit()
print("Completed done")
#############################################################################################################################
con3=appconnection()
def nosubmit():
	try:
		query = con3.cursor()
		query.execute('SELECT date1_,new_user_submit,all_user_submit FROM(SELECT DATE(c."date") as date1_,COUNT(*) as all_user_submit  FROM public."ContestParticipants" as c WHERE c."isSubmitted"=\'{}\'  GROUP BY DATE(c."date")ORDER BY DATE(c."date")) as t1 INNER JOIN(SELECT DATE(c."date") as date2_,COUNT(*) AS new_user_submit FROM public."ContestParticipants" as c INNER JOIN public."User" as u ON u.id = c."studentId" WHERE c."isSubmitted" = \'{}\'  AND DATE(u."createdAt")=DATE(c."date") GROUP BY DATE(c."date") ORDER BY DATE(c."date")) as t2  on t1.date1_ = t2.date2_ '.format("false","false"))
		incomplete = query.fetchall()
		#print(teacher)
		return incomplete
	except:
		return 0
nosubmit()
print("Incompleted done")
##############################################################################################################################
con4=appconnection()
def hist():
	try:
		query = con4.cursor()
		query.execute('SELECT id1_,nosubmit,submit,date_ FROM(SELECT c."studentId" as id1_,COUNT(*) as nosubmit FROM "ContestParticipants" as c WHERE c."isSubmitted" = \'{}\' GROUP BY c."studentId") as a INNER JOIN (SELECT DISTINCT(c."studentId") as id2_,COUNT(*) as submit,u."createdAt" as date_ FROM public."ContestParticipants" as c INNER JOIN public."User" as u ON u.id = c."studentId" WHERE c."isSubmitted" = \'{}\' GROUP BY c."studentId",u."createdAt") as b on a.id1_ =  b.id2_'.format("false","true"))
		histogram = query.fetchall()
		#print(teacher)
		return histogram
	except:
		return 0
hist()
print("Histogram done")
###############################################################################################################################
con5=appconnection()
def pattern():
	try:
		query = con5.cursor()
		query.execute('SELECT b.return_date,a.max_n,b.max_r,a.min_n,b.min_r,a.avg_n,b.avg_r FROM (SELECT DATE(c."date") as new_date,MAX(json_array_length(response :: json)) as max_n, MIN(json_array_length(response :: json)) as min_n,AVG(json_array_length(response :: json)) as avg_n FROM "ContestParticipants" as c INNER JOIN "User" as u ON c."studentId" = u.id AND json_array_length(response :: json) < 10 AND DATE(c."date") = DATE(u."createdAt") GROUP BY DATE(c."date"))a FULL JOIN (SELECT DATE(c."date") as return_date, MAX(json_array_length(response :: json)) as max_r, MIN(json_array_length(response :: json)) as min_r, AVG(json_array_length(response :: json)) as avg_r  FROM "ContestParticipants" as c INNER JOIN "User" as u  ON c."studentId" = u.id  AND json_array_length(response :: json) < 10 AND DATE(c."date") != DATE(u."createdAt") GROUP BY DATE(c."date"))b on a.new_date = b.return_date')
		pat = query.fetchall()
		#print(pat)
		return pat
	except:
		return 0
pattern()
print("pattern done")
################################################################################################################################
con6=appconnection()
def week_retention():
	try:
		query = con6.cursor()
		query.execute('SELECT first_week,SUM(CASE WHEN week_number = 0 THEN 1 ELSE 0 END) as week_0,SUM(CASE WHEN week_number = 1 THEN 1 ELSE 0 END) as week_1,SUM(CASE WHEN week_number = 2 THEN 1 ELSE 0 END) as week_2,SUM(CASE WHEN week_number = 3 THEN 1 ELSE 0 END) as week_3,SUM(CASE WHEN week_number = 4 THEN 1 ELSE 0 END) as week_4,SUM(CASE WHEN week_number = 6 THEN 1 ELSE 0 END) as week_6,SUM(CASE WHEN week_number = 9 THEN 1 ELSE 0 END) as week_9,SUM(CASE WHEN week_number = 13 THEN 1 ELSE 0 END) as week_13,SUM(CASE WHEN week_number = 18 THEN 1 ELSE 0 END) as week_18 FROM (SELECT a.aid,a.login_week,b.first_week as first_week,a.login_week-first_week as week_number FROM (SELECT c."studentId" as aid,EXTRACT(WEEK FROM c."date") as login_week FROM "ContestParticipants" as c GROUP BY c."studentId",EXTRACT(WEEK FROM c."date")) a,(SELECT c."studentId" as bid,MIN(EXTRACT(WEEK FROM c."date")) as first_week FROM "ContestParticipants" as c GROUP BY c."studentId")b WHERE a.aid=b.bid) as with_week_number GROUP BY first_week ORDER BY first_week')
		ret = query.fetchall()
		#print(ret)
		return ret
	except:
		return 0
week_retention()
print("week retention done")
################################################################################################################################
con7=appconnection()
def day_retention():
	try:
		query = con7.cursor()
		query.execute('SELECT first_day,SUM(CASE WHEN day_number = 0 THEN 1 ELSE 0 END) as day_0,SUM(CASE WHEN day_number = 1 THEN 1 ELSE 0 END) as day_1,SUM(CASE WHEN day_number = 7 THEN 1 ELSE 0 END) as day_7,SUM(CASE WHEN day_number = 14 THEN 1 ELSE 0 END) as day_14,SUM(CASE WHEN day_number = 21 THEN 1 ELSE 0 END) as day_21,SUM(CASE WHEN day_number = 30 THEN 1 ELSE 0 END) as day_30,SUM(CASE WHEN day_number = 45 THEN 1 ELSE 0 END) as day_45,SUM(CASE WHEN day_number = 60 THEN 1 ELSE 0 END) as day_60,SUM(CASE WHEN day_number = 90 THEN 1 ELSE 0 END) as day_90,SUM(CASE WHEN day_number = 120 THEN 1 ELSE 0 END) as day_120 FROM (SELECT a.aid,a.login_day,b.first_day as first_day,a.login_day-first_day as day_number FROM (SELECT c."studentId" as aid,EXTRACT(DOY FROM c."date") as login_day FROM "ContestParticipants" as c GROUP BY c."studentId",EXTRACT(DOY FROM c."date")) a,(SELECT c."studentId" as bid,MIN(EXTRACT(DOY FROM c."date")) as first_day FROM "ContestParticipants" as c GROUP BY c."studentId")b WHERE a.aid=b.bid) as with_day_number GROUP BY first_day ORDER BY first_day')
		ret = query.fetchall()
		#print(ret)
		return ret
	except:
		return 0
day_retention()
print("day retention done")