class ConnectionError(Exception):
    """Exception raised for errors in the connection to the backend server."""
    
    def __init__(self, backend_host: str, backend_port: str):
        """
            Backend host or port is not reachable.
        """
        self.message = f"Không thể kết nối tới máy chủ backend tại {backend_host}:{backend_port}. Vui lòng kiểm tra lại kết nối mạng hoặc thông tin cấu hình."
        super().__init__(self.message)