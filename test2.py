import itertools

from test import *

testing_minions=[Baron,Spy]
num_minions=1
for imp_index in range(No_players):
    temp_Role_Info = Claimed_Role_Info.copy()
    temp_Role_Info[imp_index] = Imp
    remaining_players = [i for i in range(No_players) if i != imp_index]

    # Choose minion positions among remaining players
    for minion_indices in itertools.combinations(remaining_players, num_minions):

        # Assign minions in all possible orders (permutations)
        for minion_roles in itertools.permutations(testing_minions, num_minions):
            Role_Info = temp_Role_Info.copy()
            print("Minion positions:", minion_indices)

            # Assign minion roles to positions
            for minion_pos, minion_role in zip(minion_indices, minion_roles):
                Role_Info[minion_pos] = minion_role
                print(minion_pos, minion_role.name)

            # Optional: print full Role_Info for debugging
            print([role.name for role in Role_Info])
            print("---")

        day=0
        Ability_info=[]
        if Virgin_activated:
            if Role_Info[a].name=="Virgin" or (a==Virgin_target):
                continue
        Role_Info[a]=Imp
        while day!=days:



            day+=1


