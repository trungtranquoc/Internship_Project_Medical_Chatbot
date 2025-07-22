
class CustomHTTPError:
    """Base class for HTTP errors."""
    @staticmethod
    def error_raising(code, message):
        if code == 403:
            raise CustomHTTPForbidden()
        elif code == 401:
            raise CustomHTTPUnauthorized()
        else:
            raise CustomDefaultHTTPError(code, message)

class CustomHTTPForbidden(Exception):
    def __init__(self):
        self.messsage = "Bạn không có quyền sử dụng dịch vụ này. Vui lòng kiểm tra lại thông tin cá nhân."
        super().__init__(self.messsage)

class CustomHTTPUnauthorized(Exception):
    def __init__(self):
        self.message = "Tài khoản hoặc mật khẩu không đúng. Vui lòng kiểm tra lại thông tin đăng nhập hoặc thông báo với quản trị viên."
        super().__init__(self.message)

class CustomDefaultHTTPError(Exception):
    def __init__(self, code: int, message: str):
        self.message = f"Đã có lỗi không xác định xảy ra ! Mã lỗi: {code}. Nội dung: {message}"
        super().__init__(self.message)