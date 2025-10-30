from collections import Counter
days=2
No_players=5
Type_order = ["Townsfolk", "Outsider", "Minion", "Demon"]
Type_no_list=[3,0,1,1]
Total_nights=2
if sum(Type_no_list) != No_players:
    raise ValueError(f"Error: sum of Type_no_list ({sum(Type_no_list)}) does not equal No_players ({No_players})")

Townsfolks_list=["Washerwoman","Libarian","Investigator","Chef","Empath","Fortune_teller","Undertaker","Monk","Ravenkeeper","Virgin","Slayer","Soldier","Mayor","Spy"]
True_Townsfolks_list=["Washerwoman","Libarian","Investigator","Chef","Empath","Fortune_teller","Undertaker","Monk","Ravenkeeper","Virgin","Slayer","Soldier","Mayor"]
Outsiders_list=["Butler","Drunk","Recluse","Saint","Spy"]
True_Outsiders_list=["Butler","Drunk","Recluse","Saint"]
Totally_Good_list=["Washerwoman","Libarian","Investigator","Chef","Empath","Fortune_teller","Undertaker","Monk","Ravenkeeper","Virgin","Slayer","Soldier","Mayor","Butler","Drunk","Saint"]

Minions_list=["Poisoner","Spy","Scarlet_woman","Baron","Recluse"]
True_Minion_list=["Poisoner","Spy","Scarlet_woman","Baron"]
Demon_list=["Imp","Recluse"]
True_Demon_list=["Imp"]
Totatlly_Evil_list=["Poisoner","Scarlet_woman","Baron","Imp"]

Good_list=list(set(Townsfolks_list + Outsiders_list))
Evil_list=list(set(Minions_list + Demon_list))
Might_register_list=["Recluse","Spy"]

Night_Death=[] #num
Execution_Death=[0]
Poisned_list=[]

class Role():
    def __init__(self, name, type, ability=None):
        self.name = name
        self.type = type
        self.alignment=self.sort_alignment()
        self.ability=ability
        self.activated_day=None


    def sort_alignment(self):
        if self.type in ["Outsider", "Townsfolk"]:
            return  "Good"
        else:
            return "Evil"

    def set_ability(self, func):
        self.ability = func

    def set_activated_day(self, day):
        self.activated_day=day

Slayer=Role("Slayer","Townsfolk","")
@Slayer.set_ability
def ability(target, activated=False):
    if activated:
        return Role_Info[target].type == "Demon"
    else:
        return  Role_Info[target].type == "Demon"



Libarian=(Role("Libarian", "Townsfolk"))
@Libarian.set_ability
def ability(zero=True,target1=None,target2=None,role=None):
    if not isinstance(zero, bool):
        raise ValueError("zero has to be a Boolean")
    if zero==True:
        return Type_no_list[1] == 0
    if target1 is None or target2 is None or role is None:
        raise ValueError("target1, target2, and role must not be None when zero is False")
    return (Role_Info[target1].name == role or "Spy") or (Role_Info[target2].name == role or "Spy")

Washerwoman=Role("Washerwoman","Townsfolk")
@Washerwoman.set_ability
def ability(target1=None,target2=None,role=None):
    if target1 is None or target2 is None or role is None:
        raise ValueError("target1, target2, and role must not be None when zero is False")
    return (Role_Info[target1].name == role or "Spy") or (Role_Info[target2].name == role or "Spy")

Investigator=Role("Investigator","Townsfolk")
@Investigator.set_ability
def ability(target1=None,target2=None,role=None):
    if target1 is None or target2 is None or role is None:
        raise ValueError("target1, target2, and role must not be None when zero is False")
    return (Role_Info[target1].name == role or "Recluse") or (Role_Info[target2].name == role or "Recluse")

Chef=Role("Chef","Townsfolk")
@Chef.set_ability
def ability(No_pairs):
    min_pairs=0
    max_pairs=0
    for i in range(No_players-1,-1,-1):
        if Role_Info[i].name in Evil_list and Role_Info[i-1].name in Evil_list:
            max_pairs+=1
            if Role_Info[i].name not in Might_register_list or Role_Info[i-1].name not in Might_register_list:
                min_pairs+=1
    return max_pairs>=No_pairs and No_pairs>=min_pairs

Virgin=Role("Virgin","Townsfolk")

Virgin_activated=False
Virgin_target=None
@Virgin.set_ability
def ability(activated=False,night=None,target=None):
    global Virgin_activated, Virgin_target
    if activated==True:
        Virgin_activated = True
        Virgin_target=target
        return Role_Info[target].type == "Townsfolk"
    else:
        return True

Empath=Role("Empath",'Townsfolk')
@Empath.set_ability
def ability(current_pos,no_list=[],poisoner_exist=False):
    if poisoner_exist==False:
        empathy_logic_list=[]
        for i in range(len(no_list)):
            while True:
                left=current_pos-1
                if left==-1:
                    left=No_players-1
                if left not in Execution_Death[:i] and left not in Night_Death[:i]:
                    break
            while True:
                right = current_pos + 1
                if right == No_players:
                    right = 0
                if right not in Execution_Death[:i] and right not in Night_Death[:i]:
                    break

            if no_list[i]==0:
                empathy_logic_list.append(Role_Info[left].name not in Totatlly_Evil_list and Role_Info[right].name not in Totatlly_Evil_list)
            elif no_list[i]==1:
                empathy_logic_list.append(
                    (Role_Info[left].name not in Totally_Good_list  and Role_Info[right].name not in Totatlly_Evil_list) or (Role_Info[left].name not in Totatlly_Evil_list and Role_Info[right].name not in Totally_Good_list) )
            else:
                empathy_logic_list.append(
                    Role_Info[left].name not in Totally_Good_list and Role_Info[right].name not in Totally_Good_list)
        #         print(Role_Info[left].name,Role_Info[right].name,no_list[i])
        # print(empathy_logic_list)
        return all(empathy_logic_list)

Soldier=Role("Soldier",'Townsfolk')
@Soldier.set_ability
def ability(poisoner_exist=False):
    if poisoner_exist==False:
        return "Soldier" not in Night_Death
    else:
        Poisned_list[Night_Death.index("Soldier")]

Undertaker=Role("Undertaker",'Townsfolk')
@Undertaker.set_ability
def ability(name_list,poisoner_exist=False):
    if poisoner_exist==False:
        undertaker_logic_list=[]
        for i, pos in enumerate(Execution_Death):
            undertaker_logic_list.append(Role_Info[pos].name==name_list[i])
        return all(undertaker_logic_list)


Mayor=Role("Mayor","Townsfolk",True)


Recluse=Role("Recluse","Outsider",True)
Butler=Role("Butler","Outsider",True)
Drunk=Role("Drunk","Outsider",True)

Spy=Role("Spy","Minion",True)
Baron=Role("Baron","Minion",True)

Imp=Role("Imp","Demon")


Claimed_Role_Info=[Empath,Soldier,Slayer,Washerwoman,Libarian]
Status_type=["Alive","Executed","Night_Death"]
Status=[]
Role_Info=Claimed_Role_Info.copy()

for a in range(No_players):
    for b in range(No_players):

        Current_imp = []


        if Virgin_activated:
            if Role_Info[b].name=="Virgin" :
                continue
        Role_Info[b] = Spy

        if Virgin_activated:
            if Role_Info[a].name=="Virgin" or (a==Virgin_target):
                continue
        Role_Info[a]=Imp

        Current_imp.append("Imp")
        if a in Execution_Death: #haven't add logic for scarlet woman yet
            Role_Info = Claimed_Role_Info.copy()
            continue
        Info=True
        Ability_info = [Claimed_Role_Info[0].ability(0, [2, 2]), Claimed_Role_Info[1].ability(),
                        Role_Info[3].type != "Demon", Claimed_Role_Info[3].ability(2, 4, "Slayer"),
                        Claimed_Role_Info[4].ability(True)]




        if len(Role_Info) != len(set(Role_Info)):
            Role_Info = Claimed_Role_Info.copy()
            continue


        # Count types in current assignment
        Type_counts = Counter(role.type for role in Role_Info)

        valid = all(Type_counts.get(t, 0) == n for t, n in zip(Type_order, Type_no_list))

        if not valid:
            Role_Info = Claimed_Role_Info.copy()
            continue
        # print(Ability_info)
        for j in range(No_players):
            # print(Info)
            # print(Role_Info[j].name, Role_Info[j].alignment, Ability_info[j])
            if Role_Info[j].alignment=="Good":

                if Ability_info[j]==False:
                    Info=False
                    break
        # print(Info)
        if Info==True:
            list=[x.name for x in Role_Info]
            print(list),

        Role_Info = Claimed_Role_Info.copy()



