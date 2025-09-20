kiss = []
shotgun_limit = {}
f = open(r'Bot_Data/Images_Media/Kiss.txt', 'r')
for line in f:
    kiss.append(line.strip("\n"))

for line in open(r'Bot_Data/Images_Media/Bot_Avatar.txt', 'r'):
    bot_avatar = line.strip("\n")

bounty = {}
bounty_play = {}

die = 0
