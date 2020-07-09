class Employee:
    """    
    商品の各属性値を保持する。

    Attributes
    ----------
    id : int
        自動生成の番号
    employee_id : str
        社員番号
    employee_name : str
        社員の名前
    employee_age : int
        社員の年齢
    gender : str
        社員の性別 
    photo_id : str
        社員の写真id
    adress : str
        社員の住所
    department_id : str
        所属している部署No.
    """
    
    def __init__(self, id="", employee_id="", employee_name="", employee_age="", gender="", photo_id="", adress="", department_id=""):
        self.id = id
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.employee_age = employee_age
        self.gender = gender
        self.photo_id = photo_id
        self.adress = adress
        self.department_id = department_id