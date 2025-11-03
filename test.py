from collections import Counter
import copy
import itertools

## Note: Day 0 in python means things that things happened in night 1 and day 1, But days would be equal to 1 if night 1 passed and it's day 1
No_players = 8

# === ROLE TYPE DISTRIBUTION TABLES ===
# Each list represents how many of each type appear depending on player count:
Type_order = ["Townsfolk", "Outsider", "Minion", "Demon"]

# Default setup (no Baron)
Type_no_dict = {
    5:  [3, 0, 1, 1],
    6:  [3, 1, 1, 1],
    7:  [5, 0, 1, 1],
    8:  [5, 1, 1, 1],
    9:  [5, 2, 1, 1],
    10: [7, 0, 2, 1],
    11: [7, 1, 2, 1],
    12: [7, 2, 2, 1],
    13: [9, 0, 3, 1],
    14: [9, 1, 3, 1],
    15: [9, 2, 3, 1]
}

for key, values in Type_no_dict.items():
        total = sum(values)
        if total != key:
            print(f"Error in Type_no_dict: key {key} ≠ sum({values}) = {total}")

# Default setup (with Baron)
Baron_type_no_dict = {
    5:  [1, 2, 1, 1],
    6:  [1, 3, 1, 1],
    7:  [3, 2, 1, 1],
    8:  [3, 3, 1, 1],
    9:  [3, 4, 1, 1],
    10: [5, 2, 2, 1],
    11: [5, 3, 2, 1],
    12: [5, 4, 2, 1],
    13: [7, 2, 3, 1],
    14: [7, 3, 3, 1],
    15: [7, 4, 3, 1]
}

for key, values in Baron_type_no_dict.items():
        total = sum(values)
        if total != key:
            print(f"Error in Baron_type_no_dict: key {key} ≠ sum({values}) = {total}")


# === ROLE LISTS ===
# List of roles that can be registered as townsfolks
Townsfolks_list = ["Washerwoman", "Librarian", "Investigator", "Chef", "Empath", "Fortune_Teller", "Undertaker", "Monk",
                   "Ravenkeeper", "Virgin", "Slayer", "Soldier", "Mayor", "Spy"]

# List of townsfolks
True_Townsfolks_list = ["Washerwoman", "Librarian", "Investigator", "Chef", "Empath", "Fortune_Teller", "Undertaker",
                        "Monk", "Ravenkeeper", "Virgin", "Slayer", "Soldier", "Mayor"]

# List of roles that can be registered as outsiders
Outsiders_list = ["Butler", "Drunk", "Recluse", "Saint", "Spy"]

# List of outsiders
True_Outsiders_list = ["Butler", "Drunk", "Recluse", "Saint"]

# List of good roles that cannot be registered as evil
Totally_Good_list = ["Washerwoman", "Librarian", "Investigator", "Chef", "Empath", "Fortune_Teller", "Undertaker",
                     "Monk", "Ravenkeeper", "Virgin", "Slayer", "Soldier", "Mayor", "Butler", "Drunk", "Saint"]

# List of roles that can be registered as minions
Minions_list = ["Poisoner", "Spy", "Scarlet_woman", "Baron", "Recluse"]

# List of minions
True_Minion_list = ["Poisoner", "Spy", "Scarlet_woman", "Baron"]

#List of roles that can be registered as demons
Demon_list = ["Imp", "Recluse"]

#List of demons
True_Demon_list = ["Imp"]

# List of evil roles that cannot be registered as good
Totatlly_Evil_list = ["Poisoner", "Scarlet_woman", "Baron", "Imp"]

# List of roles that can be registered as good
Good_list = list(set(Townsfolks_list + Outsiders_list))

# List of roles that can be registered as evil
Evil_list = list(set(Minions_list + Demon_list))

# List of evil roles
True_Evil_list=list(set(True_Minion_list + True_Demon_list))

# List of roles that can be registered as good or evil
Might_register_list = ["Recluse", "Spy"]

# List of good roles that does not provide any info at allF
No_Info_list = ["Mayor", "Butler", "Saint", "Recluse"]



# === ROLE CLASS DEFINITION ===
class Role():
    """Represents a single role in the game, with its type, alignment, and ability."""

    def __init__(self, name, type, activated_day=None, ability=True):
        self.name = name  #String name for easier logic
        self.type = type #(Townsfolk, Minion, etc.)
        self.alignment = self.sort_alignment() #Good or evil
        self.ability = ability  # Will be replaced by a function later
        self.activated_day = activated_day  # Tracks when ability activates, 0 as Day and night 1 etc
        self.true_activated = None

    def sort_alignment(self):
        """Determine alignment based on role type."""
        if self.type in ["Outsider", "Townsfolk"]:
            return "Good"
        elif self.type in ["Minion", "Demon"]:
            return "Evil"

    def set_ability(self, func):
        self.ability = func

    def set_input_logic(self, func):
        self.input_logic = func

# == TOWNSFOLK ROLE ==
# --- Washerwoman ---
# Learns that one of two players is a specific Townsfolk.
Washerwoman = Role("Washerwoman", "Townsfolk", 0)
@Washerwoman.set_ability
def ability(target1=None, target2=None, role=None, role_info=None):
    # validations:
    if not all(isinstance(x, int) for x in [target1, target2]):
        raise TypeError("Washerwoman error: target1 and target2 must be integers")
    if target1 >= No_players or target2 >= No_players or target1 < 0 or target2 < 0:
        raise ValueError("Washerwoman error: target1 and target2 must be valid player indices (0 to No_players - 1)")
    if target1 == target2:
        raise ValueError("Washerwoman error: target1 and target2 must not be the same player")
    if not isinstance(role, str):
        raise TypeError("Washerwoman error: role must be a string")
    if role not in True_Townsfolks_list:
        raise ValueError("Washerwoman error: role must be in True_Townsfolks_list")
    if not isinstance(role_info, list) or not all(isinstance(r, Role) for r in role_info):
        raise TypeError("Washerwoman error: role_info must be a list of Role instances")
    # logic:
    return (role_info[target1].name == role or role_info[target1].name == "Spy") or (
            role_info[target2].name == role or role_info[target2].name == "Spy")

# --- Librarian ---
# Learns that one of two players is a specific Outsider.
Librarian = Role("Librarian", "Townsfolk", 0)
@Librarian.set_ability
def ability(zero=True, target1=None, target2=None, role=None, role_info=None):
    # validations no.1:
    if not isinstance(zero, bool):
        raise TypeError("Librarian error: Parameter 'zero' must be a boolean.")
    if not isinstance(role_info, list) or not all(isinstance(r, Role) for r in role_info):
        raise TypeError("Librarian error: role_info must be a list of Role instances")

    # logic no.1: if Librarian got a 0
    if zero:
        return (Type_no_list[1] == 0 and all(r.name != "Baron" for r in role_info))

    # validations no.2:
    if target1 is None or target2 is None or role is None:
        raise ValueError("Librarian error: target1, target2, and role must not be None when zero is False")
    if target1 >= No_players or target2 >= No_players or target1 < 0 or target2 < 0:
        raise ValueError("Librarian error: target1 and target2 must be valid player indices (0 to No_players - 1)")
    if target1 == target2:
        raise ValueError("Librarian error: target1 and target2 must not be the same player")
    if role not in True_Outsiders_list:
        raise ValueError("Librarian error: role must be in True_Outsiders_list")

    #logic no.2: if Librarian got 2 targets and an outside role
    return (role_info[target1].name == role or role_info[target1].name == "Spy") or (
            role_info[target2].name == role or role_info[target2].name == "Spy")

# --- Investigator ---
# Learns that one of two players is a specific Minion.
Investigator = Role("Investigator", "Townsfolk", 0)
@Investigator.set_ability
def ability(target1=None, target2=None, role=None, role_info=None):
    # validations:
    if not all(isinstance(x, int) for x in [target1, target2]):
        raise TypeError("Investigator error: target1 and target2 must be integers")
    if target1 >= No_players or target2 >= No_players or target1 < 0 or target2 < 0:
        raise ValueError("Investigator error: target1 and target2 must be valid player indices (0 to No_players - 1)")
    if target1 == target2:
        raise ValueError("Investigator error: target1 and target2 must not be the same player")
    if not isinstance(role, str):
        raise TypeError("Investigator error: role must be a string")
    if role not in True_Minion_list:
        raise ValueError("Investigator error: role must be in True_Minion_list")
    if not isinstance(role_info, list) or not all(isinstance(r, Role) for r in role_info):
        raise TypeError("Investigator error: role_info must be a list of Role instances")

    # logic:
    return (role_info[target1].name == role or role_info[target1].name == "Recluse") or (
            role_info[target2].name == role or role_info[target2].name == "Recluse")


# --- Chef ---
# Learns how many pairs of evil players are sitting next to each other.
Chef = Role("Chef", "Townsfolk", 0)
@Chef.set_ability
def ability(No_pairs, role_info=None):
    # validation:
    if not isinstance(No_pairs, int) :
        raise TypeError("Chef error: No_pairs must be an integer")
    if No_pairs >= No_players or No_pairs < 0 :
        raise ValueError("Chef error: No_pairs must be valid player indices (0 to No_players - 1)")
    if not isinstance(role_info, list) or not all(isinstance(r, Role) for r in role_info):
        raise TypeError("Chef error: role_info must be a list of Role instances")

    #logic:
    min_pairs = 0
    max_pairs = 0
    for i in range(No_players - 1, -1, -1):
        if role_info[i].name in Evil_list and role_info[i - 1].name in Evil_list:
            max_pairs += 1
            if role_info[i].name not in Might_register_list and role_info[i - 1].name not in Might_register_list:
                min_pairs += 1
    return max_pairs >= No_pairs >= min_pairs

# --- Empath ---
# Each night, learns how many of their living neighbors are evil.
Empath = Role("Empath", 'Townsfolk')
@Empath.set_ability
def ability(current_pos, no_list=[], role_info=None):
    # validation:
    # note will add len of list correspond to execution and night death soon
    if not isinstance(current_pos, int) :
        raise TypeError("Empath error: current_pos must be an integer")
    if current_pos >= No_players or current_pos < 0 :
        raise ValueError("Empath error: current_pos must be valid player indices (0 to No_players - 1)")
    if not isinstance(no_list, list) or not all(isinstance(x, int) for x in no_list):
        raise TypeError("Empath error: no_list must be a list of integers")
    if len(no_list) == 0:
        raise ValueError("Empath error: no_list cannot be empty")
    if len(no_list) > days:
        raise ValueError("Empath error: no_list length cannot be greater than days")
    if not all(0 <= x <= 2 for x in no_list):
        raise ValueError("all elements in no_list must be between 0 and 2")
    if not isinstance(role_info, list) or not all(isinstance(r, Role) for r in role_info):
        raise TypeError("Empath error: role_info must be a list of Role instances")

    # logic
    empathy_logic_list = []
    #Each day
    for i in range(len(no_list)):
        #Check left alive player
        left = current_pos - 1
        if left == -1:
            left = No_players - 1
        while left in Execution_Death[:i] or left in Night_Death[:i]:
            left -= 1
            if left == -1:
                left = No_players - 1

        #Check right alive player
        right = current_pos + 1
        if right == No_players:
            right = 0
        while right in Execution_Death[:i] or right in Night_Death[:i]:
            right += 1
            if right == No_players:
                right = 0
        # return bool
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

# --- Fortune Teller ---
# Each night, chooses two players and learns if one is a Demon. One good player (red herring) will be registered as the Demon.
Fortune_Teller=Role("Fortune_Teller","Townsfolk")
@Fortune_Teller.set_ability
def ability(target_list,red_herring,role_info=None):
    # validation:
    # note will add len of list correspond to execution and night death soon
    if not isinstance(target_list, list):
        raise TypeError("FT error: target_list must be a list of lists")
    if not all(isinstance(sublist, list) and len(sublist) == 3 for sublist in target_list):
        raise ValueError("FT error: Each element in target_list must be a list of exactly 3 values: [int, int, bool]")
    for i, (t1, t2, flag) in enumerate(target_list):
        # Check types
        if not isinstance(t1, int) or not isinstance(t2, int):
            raise TypeError(f"FT error: target_list[{i}]: first two elements must be integers")
        if not isinstance(flag, bool):
            raise TypeError(f"FT error: target_list[{i}]: third element must be a boolean")
        if t1 < 0 or t1 >= No_players or t2 < 0 or t2 >= No_players:
            raise ValueError(f"FT error: target_list[{i}]: target indices must be between 0 and No_players - 1")
        if t1 == t2:
            raise ValueError(f"FT error: target_list[{i}]: target1 and target2 must not be the same player")
        if not isinstance(red_herring, int):
            raise TypeError("FT error: red_herring must be an integer")
        if red_herring < 0 or red_herring >= No_players:
            raise ValueError("FT error: red_herring must be a valid player index (0 to No_players - 1)")
        if not isinstance(role_info, list) or not all(isinstance(r, Role) for r in role_info):
            raise TypeError("FT error: role_info must be a list of Role instances")

    #logic
    FT_logic_list=[]
    for target_list_i in target_list:
        if target_list_i[2]==True:
            FT_logic_list.append(( role_info[target_list_i[0]].name in Demon_list) or (role_info[target_list_i[1]].name in Demon_list)or(target_list_i[0] ==red_herring or target_list_i[1] ==red_herring ))
        else:
            FT_logic_list.append((role_info[target_list_i[0]].name not in True_Demon_list) and (
                        role_info[target_list_i[1]].name not in True_Demon_list) and (
                                             target_list_i[0] != red_herring and target_list_i[1] != red_herring))
    return FT_logic_list

# --- Undertaker ---
# Learns the role of the player executed the previous day.
Undertaker = Role("Undertaker", 'Townsfolk')
@Undertaker.set_ability
def ability(name_list, role_info=None):
    #validation:
    if not isinstance(name_list, list) or not all(isinstance(n, str) for n in name_list):
        raise TypeError("Undertaker error: name_list must be a list of strings")
    if len(name_list) >= days:
        raise ValueError("Undertaker error: len(name_list) must be less than days")
    if not isinstance(role_info, list) or not all(isinstance(r, Role) for r in role_info):
        raise TypeError("Undertaker error: role_info must be a list of Role instances")

    #logic
    undertaker_logic_list = [True]
    for i, pos in enumerate(Execution_Death):
        if pos!=None:
            undertaker_logic_list.append(role_info[pos].name == name_list[i])
        else:
            undertaker_logic_list.append(True)
    return undertaker_logic_list


Slayer = Role("Slayer", "Townsfolk")
@Slayer.set_ability
def ability(target, activated=False, role_info=None):
    if activated:
        return role_info[target].type == "Demon" or role_info[target].type == "Recluse"
    else:
        return role_info[target].type != "Demon"

Virgin = Role("Virgin", "Townsfolk")
Virgin_activated = False
Virgin_target = None


@Virgin.set_ability
def ability(activated=False, target=None, role_info=None):
    global Virgin_activated, Virgin_target
    if activated == True:
        Virgin_activated = True
        Virgin_target = target
        return role_info[target].type == "Townsfolk"
    else:
        return role_info[target].type != "Townsfolk"






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
    monk_logic_list=[True]
    for i in range(len(target_list)):
        monk_logic_list.append(target_list[i]!=Night_Death[i])
    return monk_logic_list


Ravenkeeper= Role("Ravenkeeper","Townsfolk")
@Ravenkeeper.set_ability
def ability(activated,target, role, role_info=None):
    if not activated:
        return True
    else:
        return role_info[target].name==role




Mayor = Role("Mayor", "Townsfolk")
Recluse = Role("Recluse", "Outsider")
Butler = Role("Butler", "Outsider")
Saint = Role("Saint", "Outsider")
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
#
# for day in range(days-1):
#     target=input(f"Who got executed on day {day+1}?")
#     if target!="None":
#         Execution_Death.append(int(target))
#     else:
#           Execution_Death.append(None)
#     target = input(f"Who got killed on night {day + 2}?")
#     if target != "None":
#         Night_Death.append(int(target))
#     else:
#          Night_Death.append(None)


Virgin_activated = False
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
#      elif Claimed_Role == "Fortune_Teller":
#             FT_target_list=[]
#             for night in range(days):
#                 if night!=0:
#                     if position == Execution_Death[night-1] or position == Night_Death[night-1] :
#                         break
#                 target1,target2= map(int, input("Who are the targets? ").split())
#                 FT_Bool= input("Do you get yes? T/F")
#                 if FT_Bool=="T":
#                     FT_target_list.append([target1, target2,True])
#                 elif FT_Bool == "T":
#                     FT_target_list.append([target1, target2, False])
#             Claimed_Role_Info.append(Fortune_Teller)
#             Info_Provided.append(FT_target_list)


#     elif Claimed_Role=="Undertaker":
#         Undertaker_role_list = []
#         if days==1:
#             Claimed_Role_Info.append(Undertaker)
#             Info_Provided.append(Undertaker_role_list)
#         for night in range(1,days):
#             if position == Execution_Death[night - 1] or position == Night_Death[night - 1]:
#                 break
#             Undertaker_role_list.append(input(f"What role did you see for the executed player on night {night+1}?"))
#         Claimed_Role_Info.append(Undertaker)
#         Info_Provided.append(Undertaker_role_list)
#     elif Claimed_Role=="Monk":
#         Monk_pos_list=[]
#         if days==1:
#             Claimed_Role_Info.append(Monk)
#             Info_Provided.append(Monk_pos_list)
#         for night in range(1,days):
#             if position == Execution_Death[night - 1] or position == Night_Death[night - 1]:
#                 break
#             Monk_pos_list.append(int(input(f"Which person did you protect on night {night+1}?")))
#         Claimed_Role_Info.append(Monk)
#         Info_Provided.append(Monk_pos_list)
#     elif Claimed_Role=="Ravenkeeper":
#         activated_bool=input("Did you ability get activated? T/F")
#         if activated_bool=="T":
#             target=int(input("Who's the target?"))
#             role=input("What's their role?")
#             night_activated=int(input("At which night was it activated"))
#             Claimed_Role_Info.append(Ravenkeeper)
#             Info_Provided.append([True,target,role,night_activated])
#         elif activated_bool=="F":
#             Claimed_Role_Info.append(Ravenkeeper)
#             Info_Provided.append([False,0,0,0])
#
#     elif Claimed_Role=="Virgin":
#         activated_bool=input("Did you ability get activated? T/F")
#         if activated_bool=="T":
#             Virgin_activated=True
#             target=int(input("Who's the target?"))
#             night_activated = int(input("At which night was it activated"))
#             Claimed_Role_Info.append(Virgin)
#             Info_Provided.append([True, target, night_activated])
#
#         elif activated_bool=="F":
#             Claimed_Role_Info.append(Virgin)
#             Info_Provided.append([False, 0, 0])
#     elif Claimed_Role=="Slayer":
#         night_used = input("When did you use your ability?")
#         activated_bool = input("Did you ability get activated? T/F")
#         target = int(input("Who's the target?"))
#
#         if activated_bool == "T":
#             activated=True
#         elif activated_bool == "F":
#             activated = False
#         Claimed_Role_Info.append(Slayer)
#         Info_Provided.append([target, activated, night_used])
#     elif Claimed_Role =="Soldier":
#         Claimed_Role_Info.append(Soldier)
#         Info_Provided.append(None)
#     elif Claimed_Role =="Mayor":
#         Claimed_Role_Info.append(Mayor)
#         Info_Provided.append(None)
#     elif Claimed_Role=="Butler":
#         Claimed_Role_Info.append(Butler)
#         Info_Provided.append(None)
#     elif Claimed_Role=="Recluse":
#         Claimed_Role_Info.append(Recluse)
#         Info_Provided.append(None)

days = 3
Type_no_list =  Type_no_dict[No_players]
Baron_type_no_list = Baron_type_no_dict[No_players]
Execution_Death = [0,7]
Night_Death = [3, 5]
Info_Provided = []
Claimed_Role_Info = [Empath, Saint, Slayer, Ravenkeeper, Investigator,
 Fortune_Teller, Recluse, Slayer]
Info_Provided = [
    [1],
    True,
    [4,False,2],
    [True,2,"Scarlet_woman",1],
    [1,3,"Spy"],
    [[3,7,False],[2,7,False]],
    True,
    [1,False,1]

]
Correct_info=["Empath","Saint","Slayer","Ravenkeeper","Investigator","Fortune_Teller","Imp","Poisoner"]
Virgin_activated = True
Virgin_target = 3

testing_minions = [ Poisoner]
num_minions = 1
solution=0
for imp_pos in range(No_players):

    temp_Role_Info = copy.deepcopy(Claimed_Role_Info)
    temp_Role_Info[imp_pos] = Imp

    if Virgin_activated:

        if Claimed_Role_Info[imp_pos].name == "Virgin" or (imp_pos == Virgin_target):
            continue

    remaining_players = [i for i in range(No_players) if i != imp_pos]

    for minion_indices in itertools.combinations(remaining_players, Type_no_list[2]):
        skip = False
        for minion_roles in itertools.permutations(testing_minions, Type_no_list[2]):


            temp_Role_Info2 = copy.deepcopy(temp_Role_Info)


            for minion_pos, minion_role in zip(minion_indices, minion_roles):
                temp_Role_Info2[minion_pos] = minion_role
                if Virgin_activated:
                    if Claimed_Role_Info[minion_pos].name == "Virgin" or (
                            minion_pos == Virgin_target and Claimed_Role_Info[minion_pos].name != "Spy"):
                        break
            if len(temp_Role_Info2) != len(set(temp_Role_Info2)):
                continue
            remaining_players = [i for i in range(No_players) if (temp_Role_Info2[i].name not in True_Evil_list and temp_Role_Info2[i].name not in True_Outsiders_list)] + ["No_Drunk"]
            potential_red_herring = [i for i in range(No_players) if (temp_Role_Info2[i].name not in True_Evil_list and temp_Role_Info2[i].name not in True_Outsiders_list)]

            for drunk_pos in remaining_players:
                Role_Info=copy.deepcopy(temp_Role_Info2)

                # print(remaining_players)
                # print(drunk_pos)

                if drunk_pos=="No_Drunk":
                    pass
                elif isinstance(drunk_pos, int):

                    if Virgin_activated:
                        if Claimed_Role_Info[drunk_pos].name == "Virgin" or (drunk_pos == Virgin_target):

                            continue

                    Role_Info[drunk_pos] = Drunk



                start_list = [x.name for x in Role_Info]




                if imp_pos in Execution_Death and Scarlet_woman not in Role_Info:
                    continue
                if len(Role_Info) != len(set(Role_Info)):
                    continue




                Type_counts = Counter(role.type for role in Role_Info)

                ending_list = [x.name for x in Role_Info]

                # print(ending_list)
                if "Baron" in ending_list:
                    valid = all(Type_counts.get(t, 0) == n for t, n in zip(Type_order, Baron_type_no_list))
                else:


                    valid = all(Type_counts.get(t, 0) == n for t, n in zip(Type_order, Type_no_list))

                if not valid:
                    continue

                # ending_list = [x.name for x in Role_Info]
                # print(ending_list)
                if "Fortune_Teller" in ending_list:
                    FT_loop=potential_red_herring
                else:
                    FT_loop=range(1)

                for red_herring in FT_loop:


                    Ability_info = []


                    for player_index in range(No_players):

                        if Claimed_Role_Info[player_index] == Washerwoman or Claimed_Role_Info[player_index] == Investigator:
                            Ability_info.append([Claimed_Role_Info[player_index].ability(Info_Provided[player_index][0],
                                                                                         Info_Provided[player_index][1],
                                                                                         Info_Provided[player_index][2],
                                                                                         Role_Info), 0])
                        elif Claimed_Role_Info[player_index] == Librarian :
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
                        elif Claimed_Role_Info[player_index] == Fortune_Teller:
                            Ability_info.append(
                                [Claimed_Role_Info[player_index].ability(Info_Provided[player_index],red_herring,
                                                                         Role_Info),
                                 "Full"])

                        elif Claimed_Role_Info[player_index]== Undertaker:
                            Ability_info.append(
                                [Claimed_Role_Info[player_index].ability(Info_Provided[player_index], Role_Info),
                                 "Full"])
                        elif Claimed_Role_Info[player_index]== Monk:
                            Ability_info.append(
                                [Claimed_Role_Info[player_index].ability(Info_Provided[player_index]),
                                 "Full"])
                        elif Claimed_Role_Info[player_index] == Ravenkeeper:
                            Ability_info.append([Claimed_Role_Info[player_index].ability(Info_Provided[player_index][0],
                                                                                        Info_Provided[player_index][1],
                                                                                        Info_Provided[player_index][2],
                                                                                        Role_Info), Info_Provided[player_index][3]])
                        elif Claimed_Role_Info[player_index] == Virgin or Claimed_Role_Info[player_index] == Slayer :
                            Ability_info.append([Claimed_Role_Info[player_index].ability(Info_Provided[player_index][0],
                                                                                         Info_Provided[player_index][1],Role_Info),Info_Provided[player_index][2]])
                        elif Claimed_Role_Info[player_index] == Soldier:
                            Ability_info.append([Claimed_Role_Info[player_index].ability(player_index),"Full"])


                        elif Claimed_Role_Info[player_index].name in No_Info_list:
                            Ability_info.append([True, "None"])

                    ending_list = [x.name for x in Role_Info]



                    existing_minion_positions = [
                        i for i, role in enumerate(Role_Info)
                        if role.name in True_Minion_list and role.name != "Scarlet_woman"
                    ]
                    starting_list = [x.name for x in Role_Info]
                    temp_Role_Info3=copy.deepcopy(Role_Info)
                    for perm in itertools.permutations(existing_minion_positions):
                        Role_Info=copy.deepcopy(temp_Role_Info3)
                        day = 0
                        star_pass_no=0
                        Info = True
                        if Scarlet_woman in Role_Info:
                            sw_pos = Role_Info.index(Scarlet_woman)
                        while day != days:

                            if Scarlet_woman in Role_Info:

                                if (
                                        day != 0
                                        and (
                                        (Execution_Death[day - 1] is not None and Role_Info[
                                            Execution_Death[day - 1]].name == "Imp")
                                        or (Night_Death[day - 1] is not None and Role_Info[
                                    Night_Death[day - 1]].name == "Imp")
                                )
                                ):
                                    if sw_pos not in Execution_Death[:day] and sw_pos not in Night_Death[:day]:
                                        Role_Info[sw_pos] = Imp
                                    elif (
                                                day != 0
                                                and Night_Death[day - 1] is not None
                                                and Role_Info[Night_Death[day - 1]].name == "Imp"
                                        ):
                                        while True:
                                            star_pass_no += 1
                                            if star_pass_no == len(perm):
                                                Info = False
                                                break
                                            if perm[star_pass_no] not in Execution_Death[
                                                                         :day] and perm[star_pass_no] not in Night_Death[
                                                                                                             :day]:
                                                Role_Info[perm[star_pass_no]] = Imp
                                                break



                            elif (

                                    day != 0

                                    and Night_Death[day - 1] is not None

                                    and Role_Info[Night_Death[day - 1]].name == "Imp"

                            ):
                                while True:

                                    if star_pass_no == len(perm):
                                        Info=False
                                        break
                                    if perm[star_pass_no] not in Execution_Death[
                                                                    :day] and perm[star_pass_no] not in Night_Death[:day]:
                                        Role_Info[perm[star_pass_no]] = Imp
                                        star_pass_no += 1
                                        break
                                    star_pass_no += 1
                            elif (
                                            day != 0
                                            and Execution_Death[day - 1] is not None
                                            and Role_Info[Execution_Death[day - 1]].name == "Imp"
                                    ):
                                Info=False
                                break


                            ending_list = [x.name for x in Role_Info]


                            if "Poisoner" in ending_list and ending_list.index("Poisoner") not in Execution_Death[:day]  and ending_list.index("Poisoner") not in Night_Death[:day]:

                                Max_False_Info = 1

                            else:

                                Max_False_Info = 0

                            False_info = 0

                            for j in range(No_players):

                                if Role_Info[j].alignment == "Good" and Role_Info[j].name != "Drunk" and (
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
                            print(f"solution {solution}")
                            solution+=1
                            ending_list = [x.name for x in Role_Info]

                            print(starting_list)
                            print(ending_list)
                            if "Fortune_Teller" in starting_list:
                                print(f"red_herring is {red_herring}")
                            print("----")
