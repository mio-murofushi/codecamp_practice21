class Department:
    """
    商品の各属性値を保持する。

    Attributes
    ----------
    department_id : str
        部署id
    department_name : str
        部署名
    """
    
    def __init__(self, department_id="", department_name=""):
        self.department_id = department_id
        self.department_name = department_name


