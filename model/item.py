
class Item:
    """    
    商品の各属性値を保持する。

    Attributes
    ----------
    employee_id : str
        社員番号
    employee_name : str
        社員の名前
    """
    def __init__(self, employee_id="", employee_name=""):
        self.employee_id = employee_id
        self.employee_name = employee_name
