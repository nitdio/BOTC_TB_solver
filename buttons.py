import tkinter as tk

# Example BOTC Trouble Brewing roles
TB_ROLES = [
    "Washerwoman", "Librarian", "Investigator", "Chef", "Empath",
    "Fortune Teller", "Undertaker", "Monk", "Ravenkeeper",
    "Virgin", "Slayer", "Soldier", "Mayor",
    "Butler", "Recluse", "Saint", "Unknown"
]

selected_roles = []
remaining_clicks = 0

root = tk.Tk()
root.title("BOTC Role Selector")

# Display selected roles
output = tk.Label(root, text="Selected roles: []", wraplength=400)
output.pack(pady=5)

roles_frame = tk.Frame(root)
roles_frame.pack(pady=10)


# Update output text
def update_output():
    output.config(text=f"Selected roles: {selected_roles}")


# When a role button is clicked
def select_role(role_name, button):
    global remaining_clicks

    if remaining_clicks <= 0:
        return
    selected_roles.append(role_name)
    remaining_clicks -= 1
    update_output()
    if remaining_clicks == 0:
        # Remove all remaining role buttons
        for widget in roles_frame.winfo_children():
            widget.destroy()


# Show role buttons (uses a for-loop)
def show_roles(player_count):
    # Clear old buttons
    for widget in roles_frame.winfo_children():
        widget.destroy()

    for i, role in enumerate(TB_ROLES):
        btn = tk.Button(
            roles_frame,
            text=role,
            width=15,
            command=lambda r=role, b=None: select_role(r, b)
        )
        # Update the lambda to pass the button itself
        btn.config(command=lambda r=role, b=btn: select_role(r, b))
        btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)


def choose_player_count(n):
    global remaining_clicks
    count_frame.destroy()  # hide/remove number buttons
    show_roles(n)
    remaining_clicks = n


# Player count buttons (5–15)
count_frame = tk.Frame(root)
count_frame.pack(pady=10)

for n in range(5, 16):
    tk.Button(
        count_frame,
        text=str(n),
        width=4,
        command=lambda x=n: choose_player_count(x)
    ).pack(side=tk.LEFT, padx=2)

root.mainloop()