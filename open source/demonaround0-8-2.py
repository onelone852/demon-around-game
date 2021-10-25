import random
from time import sleep
from copy import deepcopy
import requests
import json
 
response = requests.get("https://raw.githubusercontent.com/onelone852/demon-around-game/main/storge/demonaround.json")
sk = response.json()
 
running = True
gameround = 1
playerlist = []
gameing = False
choicing = False
 
class char():
 
    def __init__(self,name,orhp,oratk,orattribute,skills,orsp):
        self.name = name
        self.orhp = orhp
        self.oratk = oratk
        self.atk = deepcopy(oratk)
        self.hp = deepcopy(orhp)
        self.skills = skills
 
        self.attribute = deepcopy(orattribute)
        self.orattribute = orattribute
        self.orsp = orsp
        self.sp = deepcopy(orsp)
 
        self.effect = {}
 
        self.skillslist = []
        for ski in skills:
            self.skillslist.append(sk[name][ski]['name'])
           
 
    def attack(self,obj,atk=None,nomsg=False):
        if self.hp > 0:
            atk = atk or self.atk
            obj.hp -= atk
            if self.name == obj.name:
                checkname = "自身"
            else:
                checkname = self.name
            if nomsg == False:
                print(F"{obj.name}被{checkname}攻擊！受到了{atk}點傷害。")
            try:
                self.when_attack()
            except:
                pass
            try:
                obj.when_attacken()
            except:
                pass
 
        else:
            return "fail"
 
    def health(self,obj,hp=None,limit=True,nomsg=False):
        if self.hp > 0:
           
            hp = hp or self.atk
            obj.hp += hp
            if limit == True:
                if obj.hp > obj.orhp:
                    obj.hp = obj.orhp
            if self.name == obj.name:
                checkname = "自身"
            else:
                checkname = obj.name
            if nomsg == False:
                print(F"{self.name}為{checkname}回復生命值！回復了{hp}點生命值。")
            try:
                self.when_health()
            except:
                pass
            try:
                obj.when_healthen()
            except:
                pass
        else:
            return "fail"
 
 
    def effecting(self,obj,effect,effecting,round=1,forever=False):
        if forever == True:
                round = 99999999999999999999999999999
 
        if effect == "atkadd":
            effectnow = obj.effect.get(effect,None)
            if effectnow == None:
                obj.effect[effect] = [effect,0,round]
            obj.effect[effect][1] += effecting
            obj.atk += effecting
 
        if effect == "poisoning":
            obj.effect[effect] = [effect,effecting,round]

 
    def noeffect(self,effect):
        effecting = self.effect[effect]
        try:
            if effect == "atkadd":
                self.atk -= effecting[1]
            self.effect[effect] = None
           
 
        except:
            pass
 
 
 
   
# 技能組
 
class deadman(char):
 
    def skill(self,skill,otherplaychar,if_end=True,round=1):
        playchar = self
 
        if skill == "死之禮":
            playchar.attack(otherplaychar)
        elif skill == "死吻":
            playchar.attack(otherplaychar,(playchar.atk)/2)
            playchar.health(playchar,(playchar.atk)/2)
        elif skill == "復生":
            print("此爲被動技能")
            if_end = False
        return if_end
 
    def when_attacken(self):
        self.health(self,hp=5)
 
    def relive(self):
        if self.hp <= 0:
            self.hp = self.orhp
            print(F"{self.name}復活了！")
 
class hellwife(char):
 
    def skill(self,skill,otherplaychar,if_end=True,round=1):
        playchar = self
 
        if skill == "地擊":
            playchar.attack(otherplaychar)
        elif skill == "地獄之王":
            playchar.hell(otherplaychar)
        return if_end
 
    def when_skip(self):
        print(F"{self.name}覺醒地獄之力！")
        self.atkadd(self,5,forever=True)
 
 
    def hell(self,obj):    
        if "live in hell" in obj.attribute:
            self.health(obj,hp=20,nomsg=True)
            print(F"{obj.name}被壓入地獄！但{obj.name}在地獄恢復生命值後回來了！！")
        else:
            r = self.attack(obj,50,True)
            if r != "fail":
                print(F"{obj.name}被壓入地獄！！")
 
class boneman(char):
 
    def skill(self,skill,otherplaychar,if_end=True,round=1):
        playchar = self
 
        if skill == "骨擊":
            playchar.attack(otherplaychar)
        elif skill == "骨毀":
            playchar.health(playchar,hp=(playchar.atk))
            playchar.health(otherplaychar,hp=(playchar.atk)/2)
        elif skill == "吸魂":
            playchar.getsoul()
        elif skill == "連環骨擊":
            playchar.allbone(playcharlist)
        return if_end
 
    def getsoul(self):
        try:
            health = (random.randint((round(self.hp))/4,round(self.hp)))/2
            r = self.health(self,health,False,True)
            if r != "fail":
                print(F"{self.name}吸取衆人的靈魂！")
        except:
            pass
 
    def allbone(self,other: list):
        for char in other:
            if char != self:
                r = self.attack(char,10,nomsg=True)
        if r != "fail":
            print(F"{self.name}使出連環骨擊！")
 
class believer(char):
    def skill(self,skill,otherplaychar,if_end=True,round=1):
        playchar = self
        if skill == "魔之鐮":
            playchar.attack(otherplaychar)
            playchar.health(playchar,5+(gameround/4),nomsg=True)
        elif skill == "撕裂":
            playchar.attack(playchar,atk=(playchar.atk/4))
            playchar.attack(otherplaychar,atk=(playchar.atk*0.75))
            playchar.attack(otherplaychar,atk=(playchar.atk*0.75))
        elif skill == "祈禱":
            self.tray(round)
        return if_end
 
    def when_roundthen(self,round):
        self.health(self,round/2,nomsg=True,limit=False)
        self.effecting(self,"atkadd",round/4,round=0,forever=True)
 
    def tray(self,round=1):
        self.health(self,round*0.8,limit=False)
 
    def suragain(self,round=1):
        if self.hp <= 0:
            self.hp = round*3
 
class brokewheel(char):
    def skill(self,skill,otherplaychar,if_end=True,round=1):
        playchar = self
        if skill == "穿透":
            playchar.attack(otherplaychar)
            playchar.attack(otherplaychar)
        elif skill == "重碾":
            playchar.wheel(otherplaychar)
        elif skill == "輪之地獄":
            attacking = random.randint(20,50)
            for i in range(attacking):
                if i == attacking:
                    break
                else:
                    playchar.attack(otherplaychar,playchar.atk*0.1)
        return if_end
 
    def wheel(self,otherplaychar):
        playchar = self
 
        playchar.attack(otherplaychar,(playchar.atk)*3)
        playchar.effecting(otherplaychar,"poisoning",5,round=3)

class blooddemon(char):
    def skill(self,skill,otherplaychar,if_end=True,round=1):
        playchar = self
        if skill == "魔爪":
            playchar.attack(otherplaychar)
            playchar.health(playchar,self.atk/2,limit=False)
        elif skill == "血魔之力":
            playchar.health(playchar,self.atk,nomsg=True,limit=False)
            print(F"{self.name}覺醒血魔之力！")
            if_end = False
        elif skill == "狂化":
            playchar.effecting(playchar,"atkadd",self.atk,round=1)
            print(F"{self.name}狂化了！")
            if_end = False
        return if_end
 
 
chardeadman = deadman("死亡之身",220,15,["daed","man","relive"],sk["死亡之身"],12)
charhellwife = hellwife("地獄女僕",110,35,["live in hell"],sk["地獄女僕"],10)
charboneman = boneman("零骨",150,20,["bone"],sk["零骨"],12)
charbeliever = believer("\"使徒\"",140,10,["group","relive"],sk["\"使徒\""],6)
charbrokewheel = brokewheel("破輪",170,5,["wheel"],sk["破輪"],9)
charblooddemon = blooddemon("嗜血狂魔",66,26,["blood"],sk["嗜血狂魔"],6)
 
 
 
 
playerlist = [chardeadman,charhellwife,charboneman,charbeliever,charbrokewheel,charblooddemon]
foreverlist = deepcopy(playerlist)
 
def makeinput(list:list,returnobj: bool=True,beforetext: str="",aftertext: str="",nameing=False):
    number = 1
    str = ""
    for l in list:
        if nameing == False:
            str = F"{str}{number}. {l}\n"
        else:
            str = F"{str}{number}. {l.name}\n"
        number += 1
    choice = input(F"{beforetext}{str}{aftertext}你的選擇:")
    if returnobj == True:
        try:
            choice = int(choice)
            return list[choice-1]
        except:
            pass
 
def skillinput(dict:dict,returnobj=True,beforetext: str="",aftertext: str=""):
    number = 1
    str = ""
    for el in dict:
        l = dict[el]
        name = l["name"]
        str = F"{str}{number}. {name} SP:{l['sp']} 冷卻:{l['cooldown']}\n"
        number += 1
    choice = input(F"{beforetext}{str}{aftertext}你的選擇:")
    if returnobj:
        try:
            return dict[choice-1]["name"]
        except:
            return choice
 
def then():
    print("--------------------------------------------------------")
 
def reset(playchar,otherplaychar):
    global gameround
    global playerlist
    gameround = 1
    playerlist = deepcopy(foreverlist)
    player = [playchar,otherplaychar]
    for char in player:
        char.atk = deepcopy(char.oratk)
        char.hp = deepcopy(char.orhp)
 
        char.attribute = deepcopy(char.orattribute)
        char.sp = deepcopy(char.orsp)
        char.effect = {}
 
def endcho():
    global choicing
    choicing = False
 
def roundthen(playerlist: list=None):
    global gameround
    global playchar
    global playchar1
    global playchar2
    gameround += 1
    if playchar1 == playchar:
        playchar1.sp += 1
        skills = playchar2.skills
    else:
        playchar2.sp += 1
        skills = playchar1.skills
    for skilling in skills:
            skill = skills[skilling]
            if skill["cooldown"] != 0:
                skill["cooldown"] = skill["cooldown"] - 1
    for player in playerlist:

            try:
                player.when_roundthen(gameround)
            except:
                pass
            try:
                for effection in player.effect:
                    effect = player.effect.get(effection,None)
                    if effect is not None:
                        effecttime = effect[2]
                        effecting = effect[1]
                        effectname = effect[0]

                    
                        if effecttime > 0:
                            if effectname == "poisoning":
                                player.attack(player,effecting,nomsg=True)
                                print(F"{player.name}受到{effecting}傷害。")
                                then()
                            effect[2] = effecttime - 1
                        else:
                            player.noeffect(effectname)
            except RuntimeError:
                pass
while running == True:
 
    print("《邪神領域》\n作者：湯深菜熱\n版本:0.8.2")
 
    sleep(0.25)
 
    then()
 
    gameing = None
 
    startmenu = ["開始游戲","離開游戲","協助區"]
    choice = makeinput(list=startmenu)
    if choice == "開始游戲":
            playnum = 2
            gameing = True
            playcharlist = []
            then()
            try:
                playchar1 = makeinput(playerlist,beforetext="第一玩家選擇:\n",nameing=True)
                playerlist.remove(playchar1)
                playcharlist.append(playchar1)
                then()
                playchar2 = makeinput(playerlist,beforetext="第二玩家選擇:\n",nameing=True)
                playerlist.remove(playchar2)
                playcharlist.append(playchar2)
 
            except:
                gameing = False
                running = False
 
            then()
 
            playchar = None

            while gameing == True:
                if playchar == None or playchar == playchar2:
                    playchar = playchar1
                    otherplaychar = playchar2
                   
                else:
                    playchar = playchar2
                    otherplaychar = playchar1
           
               
                print(F"第{gameround}回合\n{playchar.name}：{playchar.hp}/{playchar.sp}\n{otherplaychar.name}：{otherplaychar.hp}/{otherplaychar.sp}")
                then()
                sleep(0.1)
                choicing = True
                while choicing:
                    if_end = True
 
                    skill = skillinput(playchar.skills,beforetext=F"{playchar.name}的行動:\n",aftertext="skip(s)=跳過\nleave(l)=投降\n")
                    then()
 
                    if skill == "leave" or skill == "l":
                        print(F"回合:{gameround}\n{otherplaychar.name}勝利！")
                        reset(playchar,otherplaychar)
 
                        then()
 
                        gameing = False
 
                    elif skill == "skip" or skill == "s":
                        print(F"{playchar.name}跳過！")
 
                        try:
                            playchar.when_skip()
                        except:
                            pass
 
                    else:
                        list = playchar.skillslist
                        skills = playchar.skills
                            
                        try:
                            skill = int(skill)
                            skill = skill - 1
                            skill = list[skill]

                            if playchar.sp >= skills[skill]["sp"] and skills[skill]["cooldown"] == 0:
                                if_end = playchar.skill(skill,otherplaychar,round=gameround)
                                playchar.sp = deepcopy(playchar.sp - playchar.skills[skill]["sp"])
                                skills[skill]["cooldown"] = deepcopy(skills[skill]["orcooldown"])

                            elif playchar.sp < skills[skill]["sp"]:
                                print("SP不足")
                                if_end = False

                            elif skills[skill]["cooldown"] > 0:
                                print("該技能正處冷卻中")
                                if_end = False
                        except:
                            print("無效")
                            if_end = False
                        
                            
 
 
                           
                    then()
 
                    if playchar.hp <= 0:
                        if not "relive" in playchar.attribute:
                            print(F"回合:{gameround}\n{otherplaychar.name}勝利！")
                            reset(playchar,otherplaychar) # 重置
 
                            gameing = False # 停止游戲
 
                            then()
                        elif  "relive" in playchar.attribute: # 判定是否需要復活
                            if playchar == chardeadman:
                                playchar.relive()
                                (playchar.attribute).remove("relive")
                            elif playchar == charbeliever:
                                playchar.suragain(gameround)
                                (playchar.attribute).remove("relive")
 
                    if if_end == True: # 判定是否結束回合
                        endcho()
                        roundthen(playcharlist)
               
    elif choice == "離開游戲":
        gameing = False
        running = False

    elif choice == "協助區":
        print("https://github.com/onelone852/demon-around-game/wiki/%E3%80%8A%E9%82%AA%E7%A5%9E%E9%A0%98%E5%9F%9F%E3%80%8B%E5%AE%98%E6%96%B9%E7%B6%AD%E5%9F%BA")
        then()

    else:
        print("???")
        then()
 
 
then()
print("《邪神領域》\n作者：湯深菜熱")
then()
 
sleep(1.5)
 
exit()

# CC-BY-SA 3.0
 
 
   
