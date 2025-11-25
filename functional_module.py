class FuncMod:
    def str_lim(self, s: str, l: int):
        single_line = s.replace('\r\n', ' ') \
            .replace('\n', ' ') \
            .replace('\r', ' ')
        return single_line[:l] + '...' if len(single_line) > l else single_line