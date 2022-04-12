from typing import List


def utk(items: List[str], keyword: str) -> List[str]:
    item_bf = []

    for i in items:
        if i == keyword:
            break
        else:
            item_bf.append(i)

    return item_bf


print(utk(['red', 'orange', 'yellow', 'green', 'blue'], 'yellow'))
