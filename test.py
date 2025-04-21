from quackbox import leaderboard, save_data

# leaderboard.add_leaderboard_entry("score", 100)

entries = leaderboard.get_global_lb_entries("score")
print(entries)

entries = leaderboard.get_user_lb_entries("score", 1, 1)
print(entries)

save_data.add_save_data("123-456-7890", "This save has infinite money")
# save_data.add_save_data("save2", "This save doesn't have infinite money")

save = save_data.get_save_data_file("save1")
print(save)

save = save_data.get_save_data(r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$")
print(save)

names = save_data.get_save_file_names()
print(names)