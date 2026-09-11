import botc_solver as bs

# 7 players, no outsiders: 5 Townsfolk, 1 Minion, 1 Demon
# TRUE WORLD: 0-4 real townsfolk, 5=Poisoner(minion), 6=Imp(demon)
# Everyone claims truthfully except 5 (bluffs Soldier) and 6 (bluffs Mayor)
bs.No_players = 7
bs.days = 2
bs.Type_no_list = bs.Type_no_dict[7]          # [5,0,1,1]
bs.Baron_type_no_list = bs.Baron_type_no_dict[7]
bs.Execution_Death = [None]
bs.Night_Death = [None]
bs.Virgin_activated = False
bs.Virgin_target = None
bs.Slayer_acticated = False

bs.Claimed_Role_Info = [bs.Washerwoman, bs.Chef, bs.Empath, bs.Undertaker, bs.Monk, bs.Soldier, bs.Mayor]
bs.Info_Provided = [
    [1, 3, "Chef"],   # Washerwoman: player1 is the Chef -> true
    1,                # Chef: 1 evil pair (positions 5,6 adjacent)
    [0],              # Empath: 0 evil neighbors (1=Chef,3=Undertaker both good)
    [],               # Undertaker: no execution happened
    [2],              # Monk: protected player2 (irrelevant, no deaths)
    None,             # Soldier (bluff by real Poisoner) - unused by dispatch
    None,             # Mayor (bluff by real Imp) - unused by dispatch
]

print("=== Scenario A: true minion = Poisoner ===")
results = bs.solve(verbose=True)
print(f"\nTotal solutions found: {len(results)}")
print("Expected: 1 (true world: 5=Poisoner, 6=Imp)")