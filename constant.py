class ResMessage():
    OK = "Ok"
    DUP_TEAM_NAME = "ชื่อทีมซ้ำ"
    EMPTY_FIELD = "กรุณากรอกข้อมูล" # Field cannot be empty
    DUP_USER = "ชื่อนักวิ่งซ้ำ" # Duplicate name found
    USER_NOT_FOUND = "ไม่พบชื่อนักวิ่งในระยะ 10K" # User not found
    USER_REGISTERED = "นักวิ่งลงทะเบียนไปแล้ว"  # Already registered
    NOT_FIRST_10K = "เคยวิ่ง 10K แล้ว" # This user ran 10k before