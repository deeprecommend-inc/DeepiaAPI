def is_japanese(text):
    for _text in text:
        if 'ぁ' <= _text <= 'ん':
            return True
        if 'ァ' <= _text <= 'ン':
            return True
        if '一' <= _text <= '龥':
            return True
        if '０' <= _text <= '９':
            return True
        if 'Ａ' <= _text <= 'Ｚ':
            return True
        if 'ａ' <= _text <= 'ｚ':
            return True
        if '｡' <= _text <= 'ﾟ':
            return True
    return False

