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
		query.execute('SELECT DATE(c."date"),MAX(json_array_length(response :: json)) as max_, MIN(json_array_length(response :: json)) as min_,AVG(json_array_length(response :: json)) as avg_ FROM public."ContestParticipants" as c INNER JOIN public."User" as u  ON c."studentId" = u.id WHERE c."studentId" NOT IN (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\') AND json_array_length(response :: json) < 10 GROUP BY DATE(c."date")'.format("ck8h06t3h00054q2bz60ukhcd","ck8h0bexe00074q2bbrsl1psj","ck99hp3ai51084m611octlxny","ck8h0b8cc00064q2bqpianua9","ck8h06n8s00044q2bujzgx7zr"))
		pat = query.fetchall()
		#print(teacher)
		return pat
	except:
		return 0
pattern()
print("pattern done")
################################################################################################################################
con6=appconnection()
def retention():
	try:
		query = con5.cursor()
		query.execute('SELECT first_week,SUM(CASE WHEN week_number = 0 THEN 1 ELSE 0 END) as week_0,SUM(CASE WHEN week_number = 1 THEN 1 ELSE 0 END) as week_1,SUM(CASE WHEN week_number = 2 THEN 1 ELSE 0 END) as week_2,SUM(CASE WHEN week_number = 3 THEN 1 ELSE 0 END) as week_3,SUM(CASE WHEN week_number = 4 THEN 1 ELSE 0 END) as week_4,SUM(CASE WHEN week_number = 5 THEN 1 ELSE 0 END) as week_5,SUM(CASE WHEN week_number = 6 THEN 1 ELSE 0 END) as week_6,SUM(CASE WHEN week_number = 7 THEN 1 ELSE 0 END) as week_7,SUM(CASE WHEN week_number = 8 THEN 1 ELSE 0 END) as week_8 FROM (SELECT a.aid,a.login_week,b.first_week as first_week,a.login_week-first_week as week_number FROM(SELECT c."studentId" as aid,EXTRACT(WEEK FROM c."date") as login_week FROM "ContestParticipants" as c GROUP BY c."studentId",EXTRACT(WEEK FROM c."date"))a,(SELECT c."studentId" as bid,MIN(EXTRACT(WEEK FROM c."date")) as first_week FROM "ContestParticipants" as c GROUP BY c."studentId")b WHERE a.aid=b.bid) as with_week_number GROUP BY first_week ORDER BY first_week')
		ret = query.fetchall()
		#print(ret)
		return ret
	except:
		return 0
retention()
print("retention done")