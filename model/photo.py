class Photo:
    """
    商品の各属性値を保持する。

    Attributes
    ----------
    photo_id : str
        社員の写真id
    photo_name : str
        社員の写真ファイルネーム
    """
    
    def __init__(self, photo_id="", photo_name=""):
        self.photo_name = photo_name
        self.photo_id = photo_id