from collections import Counter
import copy
import itertools

days = 2
No_players = 5
Type_order = ["Townsfolk", "Outsider", "Minion", "Demon"]
Type_no_list = [3, 0, 1, 1]
Baron_type_no_list = [1,2,1,1]
Total_nights = 2
if sum(Type_no_list) != No_players:
    raise ValueError(f"Error: sum of Type_no_list ({sum(Type_no_list)}) does not equal No_players ({No_players})")

Townsfolks_list = ["Washerwoman", "Librarian", "Investigator", "Chef", "Empath", "Fortune_teller", "Undertaker", "Monk",
                   "Ravenkeeper", "Virgin", "Slayer", "Soldier", "Mayor", "Spy"]
True_Townsfolks_list = ["Washerwoman", "Librarian", "Investigator", "Chef", "Empath", "Fortune_teller", "Undertaker",
                        "Monk", "Ravenkeeper", "Virgin", "Slayer", "Soldier", "Mayor"]
Outsiders_list = ["Butler", "Drunk", "Recluse", "Saint", "Spy"]
True_Outsiders_list = ["Butler", "Drunk", "Recluse", "Saint"]
Totally_Good_list = ["Washerwoman", "Librarian", "Investigator", "Chef", "Empath", "Fortune_teller", "Undertaker",
                     "Monk", "Ravenkeeper", "Virgin", "Slayer", "Soldier", "Mayor", "Butler", "Drunk", "Saint"]

Minions_list = ["Poisoner", "Spy", "Scarlet_woman", "Baron", "Recluse"]
True_Minion_list = ["Poisoner", "Spy", "Scarlet_woman", "Baron"]
Demon_list = ["Imp", "Recluse"]
True_Demon_list = ["Imp"]
Totatlly_Evil_list = ["Poisoner", "Scarlet_woman", "Baron", "Imp"]

Good_list = list(set(Townsfolks_list + Outsiders_list))
Evil_list = list(set(Minions_list + Demon_list))
Might_register_list = ["Recluse", "Spy"]

No_Info_list = ["Mayor", "Butler", "Saint", "Recluse"]

Night_Death = []
Execution_Death = [0]
Poisned_list = []


class Role():
    def __init__(self, name, type, activated_day=None, ability=True):
        self.name = name
        self.type = type
        self.alignment = self.sort_alignment()
        self.ability = ability
        self.activated_day = activated_day

    def sort_alignment(self):
        if self.type in ["Outsider", "Townsfolk"]:
            return "Good"
        else:
            return "Evil"

    def set_ability(self, func):
        self.ability = func

    def set_activated_day(self, day):
        self.activated_day = day


Slayer = Role("Slayer", "Townsfolk")


@Slayer.set_ability
def ability(target, activated=False, role_info=None):
    if activated:
        return role_info[target].type == "Demon"
    else:
        return role_info[target].type != "Demon"


Librarian = Role("Librarian", "Townsfolk", 0)


@Librarian.set_ability
def ability(zero=True, target1=None, target2=None, role=None, role_info=None):
    if not isinstance(zero, bool):
        raise ValueError("zero has to be a Boolean")
    if zero == True:
        return Type_no_list[1] == 0
    if target1 is None or target2 is None or role is None:
        raise ValueError("target1, target2, and role must not be None when zero is False")
    return (role_info[target1].name == role or role_info[target1].name == "Spy") or (
            role_info[target2].name == role or role_info[target2].name == "Spy")


Washerwoman = Role("Washerwoman", "Townsfolk", 1)


@Washerwoman.set_ability
def ability(target1=None, target2=None, role=None, role_info=None):
    if target1 is None or target2 is None or role is None:
        raise ValueError("target1, target2, and role must not be None when zero is False")
    return (role_info[target1].name == role or role_info[target1].name == "Spy") or (
            role_info[target2].name == role or role_info[target2].name == "Spy")


Investigator = Role("Investigator", "Townsfolk", 1)


@Investigator.set_ability
def ability(target1=None, target2=None, role=None, role_info=None):
    if target1 is None or target2 is None or role is None:
        raise ValueError("target1, target2, and role must not be None when zero is False")
    return (role_info[target1].name == role or role_info[target1].name == "Recluse") or (
            role_info[target2].name == role or role_info[target2].name == "Recluse")


Chef = Role("Chef", "Townsfolk", 1)


@Chef.set_ability
def ability(No_pairs, role_info=None):
    min_pairs = 0
    max_pairs = 0
    for i in range(No_players - 1, -1, -1):
        if role_info[i].name in Evil_list and role_info[i - 1].name in Evil_list:
            max_pairs += 1
            if role_info[i].name not in Might_register_list or role_info[i - 1].name not in Might_register_list:
                min_pairs += 1
    return max_pairs >= No_pairs and No_pairs >= min_pairs


Virgin = Role("Virgin", "Townsfolk")
Virgin_activated = False
Virgin_target = None


@Virgin.set_ability
def ability(activated=False, night=None, target=None, role_info=None):
    global Virgin_activated, Virgin_target
    if activated == True:
        Virgin_activated = True
        Virgin_target = target
        return role_info[target].type == "Townsfolk"
    else:
        return role_info[target].type != "Townsfolk"


Empath = Role("Empath", 'Townsfolk')


@Empath.set_ability
def ability(current_pos, no_list=[], role_info=None):
    empathy_logic_list = []
    for i in range(len(no_list)):
        left = current_pos - 1
        if left == -1:
            left = No_players - 1
        while left in Execution_Death[:i] or left in Night_Death[:i]:
            left -= 1
            if left == -1:
                left = No_players - 1

        right = current_pos + 1
        if right == No_players:
            right = 0
        while right in Execution_Death[:i] or right in Night_Death[:i]:
            right += 1
            if right == No_players:
                right = 0

        if no_list[i] == 0:
            empathy_logic_list.append(
                role_info[left].name not in Totatlly_Evil_list and role_info[right].name not in Totatlly_Evil_list)
        elif no_list[i] == 1:
            empathy_logic_list.append(
                (role_info[left].name not in Totally_Good_list and role_info[right].name not in Totatlly_Evil_list) or (
                        role_info[left].name not in Totatlly_Evil_list and role_info[right].name not in Totally_Good_list))
        else:
            empathy_logic_list.append(
                role_info[left].name not in Totally_Good_list and role_info[right].name not in Totally_Good_list)
    return empathy_logic_list


Soldier = Role("Soldier", 'Townsfolk')


@Soldier.set_ability
def ability(current_pos):
    soldier_logic_list = []
    for day in range(days - 1):
        soldier_logic_list.append(current_pos != Night_Death[day])
    return soldier_logic_list

Monk = Role("Monk", 'Townsfolk')
@Monk.set_ability
def ability(target_list):
    monk_logic_list=[]
    for i in range(len(monk_logic_list)):
        monk_logic_list.append(target_list[i]!=Night_Death[i])
    return monk_logic_list


Ravenkeeper= Role("Ravenkeeper","Townsfolk")
@Ravenkeeper.set_ability
def ability(activated,target, role, role_info=None):
    if not activated:
        return True
    else:
        return role_info[target].name==role


Undertaker = Role("Undertaker", 'Townsfolk')


@Undertaker.set_ability
def ability(name_list, role_info=None):

    undertaker_logic_list = []
    for i, pos in enumerate(Execution_Death):
        undertaker_logic_list.append(role_info[pos].name == name_list[i])
    return undertaker_logic_list


Mayor = Role("Mayor", "Townsfolk")
Recluse = Role("Recluse", "Outsider")
Butler = Role("Butler", "Outsider")
Drunk = Role("Drunk", "Outsider")
Spy = Role("Spy", "Minion")
Baron = Role("Baron", "Minion")
Scarlet_woman = Role("Scarlet_woman", "Minion")
Poisoner = Role("Poisoner", "Minion")
Imp = Role("Imp", "Demon")

Status_type = ["Alive", "Executed", "Night_Death"]
Status = []

# No_players=int(input("How many players (not including travellers) are there? "))
# days=int(input("How many days has it been?"))
# Night_Death=[]
# Execution_Death=[]
# Claimed_Role_Info=[]

# for day in range(days-1):
#     target=input(f"Who got executed on day {day+1}?")
#     if target!="None":
#         Execution_Death.append(int(target))
#     target = input(f"Who got killed on night {day + 2}?")
#     if target != "None":
#         Night_Death.append(int(target))

No_players = 5
days = 2
Night_death = [4]
Execution_Death = [2]
Info_Provided = []

# for position in range(No_players):
#
#     Claimed_Role=input(f"What is position {position+1}'s claimed role?")
#     if Claimed_Role=="Washerwoman":
#         target1,target2= map(int, input("Who are the targets? ").split())
#         Known_role=input("Which particular townsfolk do you know?")
#         Claimed_Role_Info.append(Washerwoman)
#         Info_Provided.append([target1,target2,Known_role])
#     elif Claimed_Role=="Librarian":
#         zero = input("Do you get zero? T/F")
#         if zero=="T":
#             Info_Provided.append([True,0,0,0])
#         elif zero=="F":
#             target1,target2= map(int, input("Who are the targets? ").split())
#             Known_role=input("Which particular outsider do you know?")
#             Claimed_Role_Info.append(Librarian)
#             Info_Provided.append([False,target1,target2,Known_role])
#     elif Claimed_Role=="Investigator":
#         target1, target2 = map(int, input("Who are the targets? ").split())
#         Known_role = input("Which particular minions do you know?")
#         Claimed_Role_Info.append(Investigator)
#         Info_Provided.append([target1, target2, Known_role])
#     elif Claimed_Role=="Chef":
#         Num = int(input("What is the number of pairs of evil?"))
#         Claimed_Role_Info.append(Chef)
#         Info_Provided.append(Num)
#     elif Claimed_Role=="Empath":
#         Empath_num_list=[]
#         for night in range(days):
#             if night!=0:
#                 if position == Execution_Death[night-1] or position == Night_Death[night-1] :
#                     break
#             Empath_num_list.append(int(input(f"What number do you get on night {night+1}?")))
#         Claimed_Role_Info.append(Empath)
#         Info_Provided.append(Empath_num_list)
#     elif Claimed_Role=="Recluse":
#         Claimed_Role_Info.append(Recluse)
#         Info_Provided.append(None)

Claimed_Role_Info = [Empath, Recluse, Chef, Librarian, Washerwoman]
Info_Provided = [[1, 0], True, 1, [True, 0, 0, 0], [2, 3, "Chef"]]

Virgin_activated = True
Virgin_target = None
testing_minions = [Spy]
num_minions = 1

for imp_pos in range(No_players):
    temp_Role_Info = copy.deepcopy(Claimed_Role_Info)
    temp_Role_Info[imp_pos] = Imp
    if Virgin_activated:
        if Claimed_Role_Info[imp_pos].name == "Virgin" or (imp_pos == Virgin_target):
            continue

    remaining_players = [i for i in range(No_players) if i != imp_pos]

    for minion_indices in itertools.combinations(remaining_players, Type_no_list[3]):
        skip = False
        for minion_roles in itertools.permutations(testing_minions, Type_no_list[3]):
            Role_Info = copy.deepcopy(temp_Role_Info)

            for minion_pos, minion_role in zip(minion_indices, minion_roles):
                Role_Info[minion_pos] = minion_role

                if Claimed_Role_Info[minion_pos].name == "Virgin" or (
                        minion_pos == Virgin_target and Claimed_Role_Info[minion_pos].name == "Spy"):
                    skip = True
                    break
            if skip == True:
                skip = False
                break

            if len(Role_Info) != len(set(Role_Info)):
                break


            Type_counts = Counter(role.type for role in Role_Info)
            if Baron in Role_Info:
                valid = all(Type_counts.get(t, 0) == n for t, n in zip(Type_order, Baron_type_no_list))
            else:
                valid = all(Type_counts.get(t, 0) == n for t, n in zip(Type_order, Type_no_list))

            if not valid:
                break

            day = 0
            Info = True
            Ability_info = []

            for player_index in range(No_players):
                if Claimed_Role_Info[player_index] == Washerwoman or Claimed_Role_Info[player_index] == Investigator:
                    Ability_info.append([Claimed_Role_Info[player_index].ability(Info_Provided[player_index][0],
                                                                                 Info_Provided[player_index][1],
                                                                                 Info_Provided[player_index][2],
                                                                                 Role_Info), 0])
                elif Claimed_Role_Info[player_index] == Librarian:
                    Ability_info.append([Claimed_Role_Info[player_index].ability(Info_Provided[player_index][0],
                                                                                 Info_Provided[player_index][1],
                                                                                 Info_Provided[player_index][2],
                                                                                 Info_Provided[player_index][3],
                                                                                 Role_Info), 0])
                elif Claimed_Role_Info[player_index] == Chef:
                    Ability_info.append(
                        [Claimed_Role_Info[player_index].ability(Info_Provided[player_index], Role_Info), 0])
                elif Claimed_Role_Info[player_index] == Empath:
                    Ability_info.append(
                        [Claimed_Role_Info[player_index].ability(player_index, Info_Provided[player_index], Role_Info),
                         "Full"])
                elif Claimed_Role_Info[player_index].name in No_Info_list:
                    Ability_info.append([True, "None"])

            if "Poisoner" in Role_Info:
                Max_False_Info = 1
            else:
                Max_False_Info = 0

            Make_sense = True
            while day != days:
                False_info = 0
                for j in range(No_players):
                    if Role_Info[j].alignment == "Good" and Role_Info[j].alignment != "Drunk" and (
                            Ability_info[j][1] == day or Ability_info[j][1] == "Full"):
                        if Ability_info[j][1] == "Full":
                            if day + 1 <= len(Ability_info[j][0]):
                                if Ability_info[j][0][day] == False:
                                    False_info += 1
                                    if False_info > Max_False_Info:
                                        Info = False
                                        break
                        else:
                            if Ability_info[j][0] == False:
                                False_info += 1
                                if False_info > Max_False_Info:
                                    Info = False
                                    break
                day += 1
                if Info == False:
                    break

            if Info == True:
                list = [x.name for x in Role_Info]
                print(list)
                print("----")