class SplitList:
    list = []
    def __init__(self, alist, wanted_parts):
        self.list = self.split_list(alist = alist, wanted_parts= wanted_parts)

    def split_list(self, alist, wanted_parts=1):
        length = len(alist)
        return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                for i in range(wanted_parts)]