import botc_solver as bs

# 8 players: 5 TF, 1 Outsider, 1 Minion, 1 Demon
# TRUE WORLD: 0=Washerwoman,1=Chef,2=Investigator,3=Empath,4=Undertaker (TF)
#             5=Saint (Outsider), 6=Poisoner (Minion, bluffs Butler), 7=Imp (Demon, bluffs Recluse)
bs.No_players = 8
bs.days = 2
bs.Type_no_list = bs.Type_no_dict[8]           # [5,1,1,1]
bs.Baron_type_no_list = bs.Baron_type_no_dict[8]
bs.Execution_Death = [3]     # player3 (Empath) executed day1
bs.Night_Death = [None]
bs.Virgin_activated = False
bs.Virgin_target = None
bs.Slayer_acticated = False

bs.Claimed_Role_Info = [bs.Washerwoman, bs.Chef, bs.Investigator, bs.Empath, bs.Undertaker,
                         bs.Saint, bs.Butler, bs.Recluse]
bs.Info_Provided = [
    [1, 4, "Chef"],      # Washerwoman: player1 is Chef
    1,                   # Chef: 1 evil pair (6,7 adjacent)
    [6, 7, "Poisoner"],  # Investigator: one of 6/7 is Poisoner
    [0],                 # Empath: 0 evil neighbors (2,4 both good) on night1
    ["Empath"],          # Undertaker: player executed day1 was Empath
    None,                # Saint - no info
    None,                # Butler (bluff, real Poisoner) - no info
    None,                # Recluse (bluff, real Imp) - no info
]

print("=== Scenario A2: true minion = Poisoner (tighter clues) ===")
results = bs.solve(verbose=True)
distinct = set(tuple(r[1]) for r in results)
print(f"\nRaw solution count: {len(results)}")
print(f"Distinct worlds (dedup): {len(distinct)}")
for d in distinct:
    print(d)