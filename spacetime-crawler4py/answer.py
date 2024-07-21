from tool import subdomains_tracker

lst = dict()
with open('crawled_urls2.txt', 'r', encoding="utf-8") as file:
    lines = file.readlines()
    update_lines = set(lines)
    for i in lines:
        if len(subdomains_tracker(i)) != 0:
            if subdomains_tracker(i) in lst:
                lst[subdomains_tracker(i)] += 1
            else:
                lst[subdomains_tracker(i)] = 1
for item in sorted(lst.items()):
    print(*item, sep=", ")
print(len(lst))
print(len(update_lines))
