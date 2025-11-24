class FuncMod:
    def str_lim(self, s: str, l: int):
        return s[:l] + '...' if len(s) > l else s