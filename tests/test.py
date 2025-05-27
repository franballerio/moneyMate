
def get_spent(spent: list[str]) -> list | int:
    '''Creates an expense object and checks if the expense format is correct'''
    # if ("," in "".join(spent)):
    #     item = []
    #     for i in spent:
    #         if ("," not in i):
    #             item.append(i)
    #         else:
    #             item.append(i.replace(",", ""))
    #             item.append(i.replace(" ", ""))
    #             spent = spent[spent.index(i)+1:]
    #             break
    #     spent.insert(0, " ".join(item))
    
    if len(spent) != 3:
        return 0

    try:
        int(spent[1])
    except ValueError:  # Check if amount is a number
        return 1

    return tuple([spent[0],spent[1],spent[2]])


def format_spent(spent: str):
    if ("," in spent):
        spent = spent.split(",")
        spent[1] = spent[1].replace(" ","")
        spent[2] = spent[2].replace(" ","")
        
    else:
        spent = spent.split(" ")
    return spent

print(get_spent(format_spent("jean zara, 100, ropa")))