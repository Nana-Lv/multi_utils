#-*-coding:utf-8-*-
from text_proc_utils.alphabets_final import alphabet


class ProcessHighFreqChar:
    """
    A class for extracting chars from text based on the frequency.
    Two result txts will be generated, one for arrange chars in descending order,
    another for the detail frequency for reference.
    """
    def __init__(self, orig_txt_path, to_del_char=None, to_keep_char=None):
        """
        The original text path is necessary.
        :param orig_txt_path:
        :param to_del_char: Chars in this string will not be considered.
        :param to_keep_char: Chars not in this string will not be considered.
        """
        self.src_path = orig_txt_path
        self.content = self.get_content()
        self.to_del = to_del_char if isinstance(to_del_char, str) else ''
        if len(self.to_del):
            print('Chars following will be filterd ...')
            print(self.to_del[:min(20, int(0.5 * len(self.to_del)))] + ' ...')
        self.to_keep = to_keep_char if isinstance(to_keep_char, str) else ''
        if len(self.to_keep):
            print('Chars not in following will be filterd ...')
            print(self.to_keep[:min(20, int(0.5 * len(self.to_keep)))] + ' ...')
        self.high_freq_char_dict, self.valid_cnt = self.get_high_freq_char_dict()
        self.res_txt = self.get_res_txt()
        self.detail_info = self.get_detail_distribute_info()
        return

    def get_content(self):
        with open(self.src_path, 'r') as f:
            contents = f.readlines()
        return contents

    def get_high_freq_char_dict(self):
        high_freq_char = {}
        valid_cnt = 0
        for line in self.content:
            line = line.strip()
            for c in line:
                if len(self.to_keep):
                    if c not in self.to_keep:
                        continue
                if len(self.to_del):
                    if c in to_del:
                        continue
                valid_cnt += 1
                if c not in high_freq_char.keys():
                    high_freq_char[c] = 1
                else:
                    high_freq_char[c] += 1
        return high_freq_char, valid_cnt

    def get_res_txt(self):
        high_freq_char_t = sorted(self.high_freq_char_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        res_txt = ''.join([x[0] for x in high_freq_char_t])
        dst_path_1 = self.src_path.split('/')[1].split('.')[0] + '_res.txt'
        with open(dst_path_1, 'w') as f:
            f.write(res_txt)
        print('Chars appeared frequently has been written to ' + dst_path_1)
        print('Please check it.')
        return res_txt

    def get_detail_distribute_info(self):
        temp_cnt = 0
        name_freq_rate = {}
        for c in self.res_txt:
            temp_cnt += self.high_freq_char_dict[c]
            name_freq_rate[c] = temp_cnt / self.valid_cnt
        dst_path_2 = self.src_path.split('/')[1].split('.')[0] + '_detail_info.txt'
        with open(dst_path_2, 'w') as f:
            for k in self.res_txt:
                v1 = '%.2f' % (name_freq_rate[k] * 100) + '%'
                v2 = str(self.high_freq_char_dict[k])
                v3 = '%.4f' % (self.high_freq_char_dict[k] / self.valid_cnt * 100) + '%'
                f.write(k + 4 * ' ' + v1 + 4 * ' ' + v2 + 4 * ' ' + v3 + '\n')
        print('Detail information has been written to ' + dst_path_2)
        print('Please check it.')
        return name_freq_rate


if __name__ == '__main__':
    path = './people_names'
    to_del = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^abcdefghijklmnopqrstuvwxyz{}®°±÷αβγδ“”‰℃←↑→↓≤≥、。《》~￥'
    to_keep = alphabet
    ProcessHighFreqChar(path, to_del, to_keep)

