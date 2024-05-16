# https://www.immaculategrid.com/
# https://github.com/chadwickbureau/baseballdatabank.git
core_folder='D:\\Users\\sholtebeck\\Udacity\\baseballdatabank\\db'

import glob
csvfiles=glob.glob(core_folder+"\\*csv")
tables={c.split('\\')[-1][:-4]:c for c in csvfiles}


awards=[('as','All-Star'),('cya', 'Cy Young Award'), ('gg', 'Gold Glove'), ('hof', 'Hall Of Fame'), ('mvp', 'Most Valuable Player'),('roty', 'Rookie of the Year'), ('ss', 'Silver Slugger'), ('tc', 'Triple Crown'), ('wsc','World Series Champ WS Roster'),('wsmvp', 'World Series MVP')]
teams=[('ARI', 'Arizona Diamondbacks'), ('ATL', 'Atlanta Braves'), ('BAL', 'Baltimore Orioles'), ('BOS', 'Boston Red Sox'), ('CHN', 'Chicago Cubs'), ('CHA', 'Chicago White Sox'), ('CIN', 'Cincinnati Reds'), ('CLE', 'Cleveland Guardians'), ('COL', 'Colorado Rockies'), ('DET', 'Detroit Tigers'), ('HOU', 'Houston Astros'), ('KCR', 'Kansas City Royals'), ('LAA', 'Los Angeles Angels'), ('LAN', 'Los Angeles Dodgers'), ('MIA', 'Miami Marlins'), ('MIL', 'Milwaukee Brewers'), ('MIN', 'Minnesota Twins'), ('NYN', 'New York Mets'), ('NYA', 'New York Yankees'), ('OAK', 'Oakland Athletics'), ('PHI', 'Philadelphia Phillies'), ('PIT', 'Pittsburgh Pirates'), ('SDN', 'San Diego Padres'), ('SFN', 'San Francisco Giants'), ('SEA', 'Seattle Mariners'), ('SLN', 'St. Louis Cardinals'), ('TBA', 'Tampa Bay Rays'), ('TEX', 'Texas Rangers'), ('TOR', 'Toronto  Blue Jays'), ('WAS', 'Washington Nationals')]
pitchstats=[('ERAc', '≤ 3.00 ERA (Career)'), ('ERAs', '≤ 3.00 ERA (Season)'), ('SV300c', '300+ Saves (Career)'),('SV30s', '30+ Saves (Season)'),('SV40s', '40+ Saves (Season)'),('SO3000c', '3000+ Strikeouts (Career)'), ('SO200s', '200+ Strikeouts (Season)'),('W300c', '300+ Wins (Career)'),('W10s', '10+ Wins (Season)'),('W20s', '20+ Wins (Season)')]
batstats=[("AVGc",".300+ AVG (Career)"),("AVGs",".300+ AVG (Season)"),("H2000c","2000+ Hits (Career)"),("H3000c","3000+ Hits (Career)"),("H200s","200+ Hits (Season)"),("HR300c","300+ HR (Career)"),("HR400c","400+ HR (Career)"),("HR500c","500+ HR (Career)"),("HR40s","40+ HR (Season)"),("SB30s","30+ SB (Season)"), ("HS30s","30+ HR / 30+ SB (Season)"),("2B40s","40+ Doubles (Season)"),("RBI100s","100+ RBI (Season)"),("R100s","100+ Runs Scored (Season)")]
positions=[('P','Pitcher'),('C','Catcher'),('1B','First Base'),('2B','Second Base'),('3B','Third Base'),('SS','Shortstop'),('LF','Left Field'),('CF','Center Field'),('RF','Right Field'),('OF','Outfield'),('DH','Designated Hitter')]

def reload_table(table):
    if table not in tables.keys():
        return 0
    data=get_data(table)
    table_keys=" ("+','.join(data[0].keys())+")"
    import sqlite3
    dbfile="./instance/baseball.db"
    con=sqlite3.connect(dbfile)
    cur=con.cursor()
    cur.execute("drop table if exists "+table)
    create_table="create table "+table+table_keys
    cur.execute(create_table)
    rowcount=0
    for row in data:
        try:
            row_values=" values"+str(tuple([get_value(r) for r in row.values()]))
            insert_sql="insert into "+table+table_keys+row_values    
            cur.execute(insert_sql)
            rowcount+=1
        except:
            print("error on "+table+" row#"+str(rowcount)+":"+insert_sql )
            con.close()
            return rowcount
    con.commit()
    return rowcount
	
def baseball_query(sql):
#    print(sql)
    import sqlite3
    dbfile="./instance/baseball.db"
    con=sqlite3.connect(dbfile)
    cur=con.cursor() 
    res=[r for r in cur.execute(sql).fetchall()]
    cur.close()
    con.close()
    return res

def get_data(table):
    if table not in tables.keys():
        return None
    tlines=[]
    for line in open(tables[table]).readlines():
        tlines.append([get_value(t) for t in line.strip().split(',')])
    tdata=[{n:v for n,v in zip(tlines[0],tlines[t])} for t in range(1,len(tlines))]
    return tdata
    
def get_value(string):
    try:
        if ',' in string:
            return float(string)
        else:
            return int(string)
    except:
        return string

def get_name(p):
    return p['nameFirst']+" "+p["nameLast"]+" ("+p["debut"][:4]+"-"+p["finalGame"][:4]+")"

def award_key(name):
    return ''.join(n for n in name if n in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ').lower()

def only_one_team(team):
    sql="select playerName,years from players where teams='"+team+"'"
    return baseball_query(sql)

def team_overlaps(teams):
    sorteams=sorted(teams) 
    sql="select playerName,years from players where teams like '%"+sorteams[0]+"%"+sorteams[1]+"%' order by prank desc"
    return baseball_query(sql)

def team_positions(team,pos): 
    sql="select distinct p.playerName,p.years from players p join fielders f on f.playerID=p.playerID where f.teamID='"+team+"' and f.POS='"+pos+"' order by p.prank desc"
    return baseball_query(sql)

def team_awards(team,award): 
    if award=='hof':
        sql="select playerName,years from players where teams like '%"+team+"%' and hof=1"
    else:
        sql="select distinct p.playerName,p.years from players p join awards a on a.playerID=p.playerID where a.teamID='"+team+"' and a.awardID='"+award+"' order by p.prank desc"
    return baseball_query(sql)

def two_awards(award1,award2): 
    awsort=sorted([award1,award2])
    sql="select playerName,years from players where awards like '%"+awsort[0]+"%"+awsort[1]+"%' order by prank desc"
    return baseball_query(sql)

# Season Batting Stats (AVG,H,HR,SB,HS,RBI,2B)
def season_batting_stats(team,stat):
    criteria=""
    if stat=="AVG":
        criteria = " AND b.H*1000/b.AB<=300"
        stat="H*1000/b.AB"
    elif stat[:2]=="HS":
        criteria = " AND b.HR>=30 and b.SB>=30"
        stat="HR*100+b.SB"
    elif stat[:2]=="HR":
        criteria = " AND b.HR>"+stat[2:]
        stat="HR"
    elif stat[0]=="H":
        criteria = " AND b.H>="+stat[1:]
        stat="H"
    elif stat[:3]=="RBI":
        criteria = " AND b.RBI>="+stat[3:]
        stat="RBI"
    elif stat[0]=="R":
        criteria = " AND b.R>="+stat[1:]
        stat="R"
    elif stat[:2]=="SB":
        criteria = " AND b.SB>="+stat[2:]
        stat="SB"
    elif stat[:2]=="2B":
        criteria = " AND b.DB>="+stat[2:]
        stat="DB"
    sql="select distinct p.playerName,max(b."+stat+") as val from players p join batters b on b.playerID=p.playerID where b.teamID='"+team+"' "+criteria+" group by p.playerName"
    return baseball_query(sql)
    
# Career Batting Stats (AVG,H,HR)
def career_batting_stats(team,stat):
    criteria=""
    sstat=stat
    if stat=="AVG":
        criteria = " AND p.AVG>=300"
        sstat='AVG'
    elif stat[:2]=="HR":
        criteria = " AND p.HR>="+stat[2:]
        sstat='HR'
    elif stat[0]=="H":
        criteria = " AND p.H>="+stat[1:]
        sstat='H'
    sql="select p.playerName,p.years,p."+sstat+" from players p where p.bp='B' and p.teams like '%"+team+"%' "+criteria
    return baseball_query(sql)
    
def batting_stats(team,stat):
    if stat.endswith("c"):
        return career_batting_stats(team,stat[:-1])
    else:
        return season_batting_stats(team,stat[:-1])
	
def season_pitching_stats(team,stat):
    criteria=""
    if stat=="ERA":
        criteria = " AND q.ERA<='3.00'"
        sstat="ERA"
    elif stat[:2]=="SV":
        criteria = " AND q.SV>="+stat[2:]
        sstat="SV"
    elif stat[:2]=="SO":
        criteria = " AND q.SO>="+stat[2:]
        sstat="SO"
    elif stat[0]=="W":
        criteria = " AND q.W>="+stat[1:]
        sstat="W"
    sql="select distinct p.playerName,max(q."+sstat+") as val from players p join pitchers q on q.playerID=p.playerID where q.teamID='"+team+"' "+criteria+" group by p.playerName"
    return baseball_query(sql)

def career_pitching_stats(team,stat):
    pstats=['W', 'L', 'G', 'GS', 'CG', 'SHO', 'SV', 'IPouts', 'H', 'ER', 'HR', 'BB', 'SO']
    criteria=""
    sindex=-1
    if stat=="ERA":
        criteria = " AND p.AVG<=300"
    elif stat[:2]=="SV":
        sindex=pstats.index("SV")
        svalue=int(stat[2:])
    elif stat[:2]=="SO":
        sindex=pstats.index("SO")
        svalue=int(stat[2:])
    elif stat[0]=="W":
        sindex=pstats.index("W")
        svalue=int(stat[1:])
    sql="select p.playerName,p.years,p.stats from players p where p.bp='P' and teams like '%"+team+"%' "+criteria
    pitchers=baseball_query(sql)
    if sindex>=0:
        pitchers=[(p[0],int(p[2].split("-")[sindex])) for p in pitchers if p[2].count("-")==12 and int(p[2].split("-")[sindex])>=svalue]
    else:
        pitchers=[p[:2] for p in pitchers]
    return pitchers


def pitching_stats(team,stat):
    if stat.endswith("c"):
        return career_pitching_stats(team,stat[:-1])
    else:
        return season_pitching_stats(team,stat[:-1])


def get_players(filters):
    # Get all Filters
    afilters=[a for a in awards if a[0] in filters]
    tfilters=[t for t in teams if t[0] in filters]
    pfilters=[p for p in positions if p[0] in filters]
    bfilters=[b for b in batstats if b[0] in filters]
    sfilters=[s for s in pitchstats if s[0] in filters]
    #Team + Team
    if len(tfilters)==2:
        return team_overlaps(sorted([t[0] for t in tfilters]))
    #Team + Award
    elif len(afilters)==2:
        return two_awards(afilters[0][0],afilters[1][0])
    #Team + Award
    elif len(tfilters)==1 and len(afilters)==1:
        return team_awards(tfilters[0][0],afilters[0][0])
    #Team + Position
    elif len(tfilters)==1 and len(pfilters)==1:
        return team_positions(tfilters[0][0],pfilters[0][0])
    #Team + Batting Stats
    elif len(tfilters)==1 and len(bfilters)==1:
        return batting_stats(tfilters[0][0],bfilters[0][0])
    #Team + Pitching Stats
    elif len(tfilters)==1 and len(sfilters)==1:
        return pitching_stats(tfilters[0][0],sfilters[0][0])
    return []

def get_description(filters):
    afilters=[a[1] for a in awards if a[0] in filters]
    tfilters=[t[1] for t in teams if t[0] in filters]
    pfilters=[p[1] for p in positions if p[0] in filters]
    bfilters=[b[1] for b in batstats if b[0] in filters]
    sfilters=[s[1] for s in pitchstats if s[0] in filters]
    description=""
    if len(tfilters)>=2:
        description=' + '.join(tfilters)
    if len(tfilters)==1 and len(afilters)==1:
        description=tfilters[0]+' who have '+afilters[0]
    if len(tfilters)==1 and len(pfilters)==1:
        description=tfilters[0]+' who have played '+pfilters[0]
    if len(tfilters)==1 and len(bfilters)==1:
        description=tfilters[0]+' who have '+bfilters[0]
    #Team + Pitching Stats
    if len(tfilters)==1 and len(sfilters)==1:
        description=tfilters[0]+' who have '+sfilters[0]
    return description
      
   