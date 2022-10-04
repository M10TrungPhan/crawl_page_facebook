from pydantic import BaseModel
from typing import AnyStr, Optional


class AccountFacebookRequest(BaseModel):
    username: AnyStr
    password: Optional[AnyStr]
    status: Optional[AnyStr]

    def __init__(self, username: AnyStr, password: AnyStr = None, status: AnyStr = None):
        super(AccountFacebookRequest, self).__init__(username=username, password=password, status=status )
        self.username = username
        self.password = password
        self.status = status

