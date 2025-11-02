from collections import Counter
import copy
import itertools

# Configuration
days = 2
No_players = 5
Type_order = ["Townsfolk", "Outsider", "Minion", "Demon"]
Type_no_list = [3, 0, 1, 1]
Baron_type_no_list = [1, 2, 1, 1]

# Role lists
Townsfolks_list = ["Washerwoman", "Librarian", "Investigator", "Chef", "Empath", "Fortune_teller", "Undertaker", "Monk",
                   "Ravenkeeper", "Virgin", "Slayer", "Soldier", "Mayor", "Spy"]
Outsiders_list = ["Butler", "Drunk", "Recluse", "Saint", "Spy"]
Minions_list = ["Poisoner", "Spy", "Scarlet_woman", "Baron", "Recluse"]
Demon_list = ["Imp", "Recluse"]

Totally_Good_list = ["Washerwoman", "Librarian", "Investigator", "Chef", "Empath", "Fortune_teller", "Undertaker",
                     "Monk", "Ravenkeeper", "Virgin", "Slayer", "Soldier", "Mayor", "Butler", "Drunk", "Saint"]
Totatlly_Evil_list = ["Poisoner", "Scarlet_woman", "Baron", "Imp"]
Good_list = list(set(Townsfolks_list + Outsiders_list))
Evil_list = list(set(Minions_list + Demon_list))
Might_register_list = ["Recluse", "Spy"]
No_Info_list = ["Mayor", "Butler", "Saint", "Recluse"]

# Game state
Night_Death = []
Execution_Death = [0]
Virgin_activated = False
Virgin_target = None


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


# Define all roles
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
        raise ValueError("target1, target2, and role must not be None")
    return (role_info[target1].name == role or role_info[target1].name == "Spy") or (
            role_info[target2].name == role or role_info[target2].name == "Spy")


Investigator = Role("Investigator", "Townsfolk", 1)


@Investigator.set_ability
def ability(target1=None, target2=None, role=None, role_info=None):
    if target1 is None or target2 is None or role is None:
        raise ValueError("target1, target2, and role must not be None")
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
                        role_info[left].name not in Totatlly_Evil_list and role_info[
                    right].name not in Totally_Good_list))
        else:
            empathy_logic_list.append(
                role_info[left].name not in Totally_Good_list and role_info[right].name not in Totally_Good_list)
    return empathy_logic_list


Soldier = Role("Soldier", 'Townsfolk')


@Soldier.set_ability
def ability(current_pos):
    soldier_logic_list = []
    for day_idx in range(days - 1):
        soldier_logic_list.append(current_pos != Night_Death[day_idx])
    return soldier_logic_list


Monk = Role("Monk", 'Townsfolk')


@Monk.set_ability
def ability(target_list):
    monk_logic_list = []
    # Fixed: iterate over target_list length, not monk_logic_list
    for i in range(len(target_list)):
        monk_logic_list.append(target_list[i] != Night_Death[i])
    return monk_logic_list


Ravenkeeper = Role("Ravenkeeper", "Townsfolk")


@Ravenkeeper.set_ability
def ability(activated, target, role, role_info=None):
    if not activated:
        return True
    else:
        return role_info[target].name == role


Virgin = Role("Virgin", "Townsfolk")


@Virgin.set_ability
def ability(activated=False, target=None, role_info=None):
    if activated == True:
        return role_info[target].type == "Townsfolk"
    else:
        return role_info[target].type != "Townsfolk"


Undertaker = Role("Undertaker", 'Townsfolk')


@Undertaker.set_ability
def ability(name_list, role_info=None):
    undertaker_logic_list = [True]
    for i, pos in enumerate(Execution_Death):
        undertaker_logic_list.append(role_info[pos].name == name_list[i])
    return undertaker_logic_list


# Simple roles
Mayor = Role("Mayor", "Townsfolk")
Recluse = Role("Recluse", "Outsider")
Butler = Role("Butler", "Outsider")
Drunk = Role("Drunk", "Outsider")
Spy = Role("Spy", "Minion")
Baron = Role("Baron", "Minion")
Scarlet_woman = Role("Scarlet_woman", "Minion")
Poisoner = Role("Poisoner", "Minion")
Imp = Role("Imp", "Demon")

testing_minions = [Spy, Poisoner]


def run_solver(test_name, claimed_roles, info_provided, night_deaths, execution_deaths, virgin_active=False,
               virgin_tgt=None):
    """Run the solver with given parameters and display results"""
    global No_players, days, Night_Death, Execution_Death, Virgin_activated, Virgin_target

    No_players = len(claimed_roles)
    days = len(night_deaths) + 1
    Night_Death = night_deaths
    Execution_Death = execution_deaths
    Virgin_activated = virgin_active
    Virgin_target = virgin_tgt

    print("=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)
    print(f"Players: {No_players}, Days: {days}")
    print(f"Claimed roles: {[r.name for r in claimed_roles]}")
    print(f"Night deaths: {Night_Death}, Executions: {Execution_Death}")
    print("-" * 70)

    solutions_found = 0

    for imp_pos in range(No_players):
        temp_Role_Info = copy.deepcopy(claimed_roles)
        temp_Role_Info[imp_pos] = Imp

        if Virgin_activated:
            if claimed_roles[imp_pos].name == "Virgin" or (imp_pos == Virgin_target):
                continue

        remaining_players = [i for i in range(No_players) if i != imp_pos]

        for minion_indices in itertools.combinations(remaining_players, Type_no_list[2]):
            skip = False
            for minion_roles in itertools.permutations(testing_minions, Type_no_list[2]):
                Role_Info = copy.deepcopy(temp_Role_Info)

                for minion_pos, minion_role in zip(minion_indices, minion_roles):
                    Role_Info[minion_pos] = minion_role

                    if claimed_roles[minion_pos].name == "Virgin" or (
                            minion_pos == Virgin_target and claimed_roles[minion_pos].name == "Spy"):
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
                    if claimed_roles[player_index] == Washerwoman or claimed_roles[player_index] == Investigator:
                        Ability_info.append([claimed_roles[player_index].ability(info_provided[player_index][0],
                                                                                 info_provided[player_index][1],
                                                                                 info_provided[player_index][2],
                                                                                 Role_Info), 0])
                    elif claimed_roles[player_index] == Librarian:
                        Ability_info.append([claimed_roles[player_index].ability(info_provided[player_index][0],
                                                                                 info_provided[player_index][1],
                                                                                 info_provided[player_index][2],
                                                                                 info_provided[player_index][3],
                                                                                 Role_Info), 0])
                    elif claimed_roles[player_index] == Chef:
                        Ability_info.append(
                            [claimed_roles[player_index].ability(info_provided[player_index], Role_Info), 0])
                    elif claimed_roles[player_index] == Empath:
                        Ability_info.append(
                            [claimed_roles[player_index].ability(player_index, info_provided[player_index], Role_Info),
                             "Full"])
                    elif claimed_roles[player_index] == Undertaker:
                        Ability_info.append(
                            [claimed_roles[player_index].ability(info_provided[player_index], Role_Info),
                             "Full"])
                    elif claimed_roles[player_index] == Monk:
                        Ability_info.append(
                            [claimed_roles[player_index].ability(info_provided[player_index]),
                             "Full"])
                    elif claimed_roles[player_index] == Ravenkeeper:
                        Ability_info.append([claimed_roles[player_index].ability(info_provided[player_index][0],
                                                                                 info_provided[player_index][1],
                                                                                 info_provided[player_index][2],
                                                                                 Role_Info),
                                             info_provided[player_index][3]])
                    elif claimed_roles[player_index] == Virgin or claimed_roles[player_index] == Slayer:
                        Ability_info.append([claimed_roles[player_index].ability(info_provided[player_index][0],
                                                                                 info_provided[player_index][1],
                                                                                 Role_Info),
                                             info_provided[player_index][2]])
                    elif claimed_roles[player_index] == Soldier:
                        Ability_info.append([claimed_roles[player_index].ability(player_index), "Full"])
                    elif claimed_roles[player_index].name in No_Info_list:
                        Ability_info.append([True, "None"])

                # Fixed: Check for Poisoner object, not string
                if Poisoner in Role_Info:
                    Max_False_Info = 1
                else:
                    Max_False_Info = 0

                while day != days:
                    False_info = 0
                    for j in range(No_players):
                        # Fixed: Check name != "Drunk", not alignment
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
                    solutions_found += 1
                    role_names = [x.name for x in Role_Info]
                    print(f"Solution {solutions_found}: {role_names}")

    print(f"\n✓ Total solutions found: {solutions_found}\n")
    return solutions_found


# TEST CASE 1: Ravenkeeper dies and learns a role
print("\n" + "🔍 RAVENKEEPER TEST CASES" + "\n")

run_solver(
    "Ravenkeeper learns Chef at position 2",
    claimed_roles=[Ravenkeeper, Mayor, Chef, Mayor, Mayor],
    info_provided=[[True, 2, "Chef", 0], None, None, None, None],
    night_deaths=[0],
    execution_deaths=[1]
)

run_solver(
    "Ravenkeeper claims to see Imp (should find solutions where pos 3 is Imp)",
    claimed_roles=[Ravenkeeper, Mayor, Mayor, Mayor, Mayor],
    info_provided=[[True, 3, "Imp", 0], None, None, None, None],
    night_deaths=[0],
    execution_deaths=[1]
)

run_solver(
    "Ravenkeeper didn't activate (alive)",
    claimed_roles=[Ravenkeeper, Mayor, Chef, Mayor, Mayor],
    info_provided=[[False, 0, 0, 0], None, None, None, None],
    night_deaths=[1],
    execution_deaths=[2]
)

# TEST CASE 2: Virgin mechanics
print("\n" + "🛡️ VIRGIN TEST CASES" + "\n")

run_solver(
    "Virgin activated by Townsfolk (should confirm target is Townsfolk)",
    claimed_roles=[Virgin, Mayor, Chef, Mayor, Mayor],
    info_provided=[[True, 2, 0], None, None, None, None],
    night_deaths=[1],
    execution_deaths=[3],
    virgin_active=True,
    virgin_tgt=2
)

run_solver(
    "Virgin not activated",
    claimed_roles=[Virgin, Mayor, Mayor, Mayor, Mayor],
    info_provided=[[False, 0, 0], None, None, None, None],
    night_deaths=[1],
    execution_deaths=[2]
)

# TEST CASE 3: Monk protection
print("\n" + "🙏 MONK TEST CASES" + "\n")

run_solver(
    "Monk protected position 3 (who didn't die)",
    claimed_roles=[Monk, Mayor, Mayor, Mayor, Mayor],
    info_provided=[[3], None, None, None, None],
    night_deaths=[1],
    execution_deaths=[2]
)

run_solver(
    "Monk protected position 1 but position 1 died (contradiction!)",
    claimed_roles=[Monk, Mayor, Mayor, Mayor, Mayor],
    info_provided=[[1], None, None, None, None],
    night_deaths=[1],
    execution_deaths=[2]
)

# TEST CASE 4: Soldier survival
print("\n" + "⚔️ SOLDIER TEST CASES" + "\n")

run_solver(
    "Soldier at position 2 survived the night (should exclude pos 2 as night death)",
    claimed_roles=[Mayor, Mayor, Soldier, Mayor, Mayor],
    info_provided=[None, None, None, None, None],
    night_deaths=[1],
    execution_deaths=[3]
)

run_solver(
    "Soldier at position 1 but position 1 died at night (contradiction!)",
    claimed_roles=[Mayor, Soldier, Mayor, Mayor, Mayor],
    info_provided=[None, None, None, None, None],
    night_deaths=[1],
    execution_deaths=[2]
)

# TEST CASE 5: Undertaker sees executed roles
print("\n" + "⚰️ UNDERTAKER TEST CASES" + "\n")

run_solver(
    "Undertaker sees 'Chef' was executed at position 2",
    claimed_roles=[Undertaker, Mayor, Chef, Mayor, Mayor],
    info_provided=[["Chef"], None, None, None, None],
    night_deaths=[1],
    execution_deaths=[2]
)

run_solver(
    "Undertaker sees 'Imp' was executed (finds where Imp could be)",
    claimed_roles=[Undertaker, Mayor, Mayor, Mayor, Mayor],
    info_provided=[["Imp"], None, None, None, None],
    night_deaths=[1],
    execution_deaths=[2]
)

# TEST CASE 6: Combined abilities
print("\n" + "🎭 COMBINED TEST CASES" + "\n")

run_solver(
    "Empath + Ravenkeeper + Chef combo",
    claimed_roles=[Empath, Ravenkeeper, Chef, Mayor, Mayor],
    info_provided=[[1, 0], [True, 2, "Chef", 0], 1, None, None],
    night_deaths=[1],
    execution_deaths=[4]
)

run_solver(
    "Monk + Soldier + Undertaker combo",
    claimed_roles=[Monk, Soldier, Undertaker, Mayor, Mayor],
    info_provided=[[3], None, ["Mayor"], None, None],
    night_deaths=[3],
    execution_deaths=[4]
)

print("\n" + "=" * 70)
print("✅ ALL TESTS COMPLETE!")
print("=" * 70)