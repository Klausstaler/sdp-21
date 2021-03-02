import re
lines = []
i = 1
with open("SuctionBox.proto", "r") as f:
    for line in f.readlines():
        if "connector" in line:
            line = re.sub(r"connector\([0-9]+[0-9]?\)", f"connector({i})", line)
            i += 1
        lines.append(line)
with open("SuctionBox.proto", "w") as f:
    f.writelines(lines)
