import requests

class TraoDoiSub:

    def __init__(self, user, pwd):

        self.user = user
        self.pwd = pwd
        self.urls = "https://traodoisub.com/api/?fields={}&access_token={}"
    
    def Valid(self) -> bool:

        data = {
            "username": self.user,
            "password": self.pwd
        }
        headers = {
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
        }
        response = requests.post("https://traodoisub.com/scr/login.php",headers=headers, data=data)
        # print(response.text)
        if 'success":true' in response.text:
            # cookies = response.cookies["PHPSESSID"]
            stringsCookie = "PHPSESSID="+str(response.cookies["PHPSESSID"])
            headers.update({"Cookie":stringsCookie})
            getAccessToken = requests.post("https://traodoisub.com/view/setting/load.php",headers=headers).json()
            try:
                self.xuNow = getAccessToken["xu"]
                self.tokentds = getAccessToken["tokentds"]
                return True, "Đăng nhập thành công!"
            except:
                return False, "Có lỗi trong quá trình lấy token!"
        else:
            return False, "Sai tài khoản hoặc mật khẩu!"
    
    def CauHinh(self, idUser:str):
        
        Checked = requests.get(self.urls.format(f"instagram_run&id={idUser}",self.tokentds))
        # print(Checked.json())
        if "success" in Checked.json():
            self.userIG = Checked.json()['data']["uniqueID"]
            return True, "Cấu hình thành công!"
        else:
            return False, "Tài khoản chưa được cấu hình!"
    
    def GetJobInstagram(self, typeJob:str):
        
        # instagram_like, instagram_follow, instagram_comment, instagram_likecmt
        if typeJob == "LIKE":
            nameJob = "instagram_like"
        elif typeJob == "FOLLOW":
            nameJob = "instagram_follow"
        elif typeJob == "COMMENT":
            nameJob = "instagram_comment"
        elif typeJob == "LIKECMT":
            nameJob = "instagram_likecmt"
        else:
            return False, "Lựa chọn không phù hợp!"

        get = requests.get(self.urls.format(nameJob, self.tokentds))
        try:
            return True, get.json()["data"]
        except:
            return False, "Có lỗi trong quá trình lấy nhiệm vụ!"
    
    def GuiDuyet(self, idJob:str, typeJob:str):

        if typeJob == "LIKE":
            nameJob = "INS_LIKE_CACHE"
        elif typeJob == "FOLLOW":
            nameJob = "INS_FOLLOW_CACHE"
        elif typeJob == "COMMENT":
            nameJob = "INS_LIKECMT_CACHE"
        elif typeJob == "LIKECMT":
            nameJob = "INS_LIKECMT_CACHE"
        else:
            return False, "Lựa chọn không phù hợp!"
        response = requests.get(f"https://traodoisub.com/api/coin/?type={nameJob}&id={idJob}&access_token={self.tokentds}")
        if "success" in response.json():
            self.cache = response.json()['data']["cache"]
            self.coinWait = response.json()['data']["pending"]
            return True, "Gửi duyệt thành công!"
        else:
            return False, "Gửi duyệt thất bại!"
# t = TraoDoiSub("","")
# if t.Valid()[0] == True:
#     print(t.GuiDuyet("36892936852_X7UQP1XR00JXNQJMYD43","FOLLOW")[1])