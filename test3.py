import botc_solver as bs

# 7 players with Baron: 3 Townsfolk, 2 Outsiders, 1 Minion(Baron), 1 Demon
# TRUE WORLD: 0=Washerwoman,1=Chef,2=Empath (TF), 3=Saint,4=Butler (Outsider),
#             5=Baron(minion), 6=Imp(demon)
bs.No_players = 7
bs.days = 2
bs.Type_no_list = bs.Type_no_dict[7]
bs.Baron_type_no_list = bs.Baron_type_no_dict[7]   # [3,2,1,1]
bs.Execution_Death = [None]
bs.Night_Death = [None]
bs.Virgin_activated = False
bs.Virgin_target = None
bs.Slayer_acticated = False

bs.Claimed_Role_Info = [bs.Washerwoman, bs.Chef, bs.Empath, bs.Saint, bs.Butler, bs.Mayor, bs.Recluse]
bs.Info_Provided = [
    [1, 3, "Chef"],   # Washerwoman: player1 is the Chef -> true
    1,                # Chef: 1 evil pair (positions 5,6 adjacent)
    [0],              # Empath: 0 evil neighbors (1=Chef,3=Saint both good)
    None,             # Saint (real) - no info
    None,             # Butler (real) - no info
    None,             # Mayor (bluff by real Baron) - no info
    None,             # Recluse (bluff by real Imp) - no info
]

print("=== Scenario B: true minion = Baron (control) ===")
results = bs.solve(verbose=True)
print(f"\nTotal solutions found: {len(results)}")
print("Expected: 1 (true world: 5=Baron, 6=Imp)")