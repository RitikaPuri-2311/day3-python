# flatten nested list

nested_list = [[ "apple","grapes","banana" ], [["kiwi","orange","mango"], "pineapple", "papaya"], ["watermelon", "melon"]]


flatlist = []


def flat(lis):
    for i in lis:
        if isinstance(i, list):
            flat(i)
        else:
            flatlist.append(i)


flat(nested_list)
print(flatlist)