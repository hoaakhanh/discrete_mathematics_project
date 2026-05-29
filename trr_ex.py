# Thiết kế các class sau: 
  
# 1. TaiLieu (Abstract Base Class) 
#    - Thuộc tính: ma_tai_lieu, tieu_de, nam_xuat_ban 
#    - Abstract method: hien_thi_chi_tiet() 
#    - Concrete method: __str__() 
  
# 2. Sach(TaiLieu) 
#    - Thêm: tac_gia, so_trang, __so_ban_co_san (private) 
#    - Property: so_ban_co_san (getter + setter có validation) 
#    - Override: hien_thi_chi_tiet() 
  
# 3. TapChi(TaiLieu) 
#    - Thêm: so_phat_hanh, nha_xuat_ban 
#    - Override: hien_thi_chi_tiet() 
  
# 4. ThuVien 
#    - Quản lý danh sách TaiLieu 
#    - them_tai_lieu(tai_lieu) 
#    - tim_kiem(tu_khoa) -> list 
#    - hien_thi_tat_ca() 
#    - thong_ke() -> dict {'Sach': n, 'TapChi': m} 
from abc import ABC, abstractmethod
class TaiLieu(ABC):
    def __init__(self, ma_tai_lieu, tieu_de, nam_xuat_ban):
        self.ma_tai_lieu = ma_tai_lieu
        self.tieu_de = tieu_de
        self.nam_xuat_ban = nam_xuat_ban
    @abstractmethod
    def hien_thi_chi_tiet(self):
        pass
    # Concret method
    def __str__(self):
        return f"Document ID: {self.ma_tai_lieu}, Title: {self.tieu_de}, Year: {self.nam_xuat_ban}"


class Sach(TaiLieu):
    def __init__(self, ma_tai_lieu, tieu_de, nam_xuat_ban, tac_gia, so_trang, __so_ban_co_san):
        super().__init__(ma_tai_lieu, tieu_de, nam_xuat_ban)
        self.tac_gia = tac_gia
        self.so_trang = so_trang
        self.__so_ban_co_san = __so_ban_co_san

    #Getter -> lay ttin co san
    @property # Bien method thanh attribute
    def so_ban_co_san(self):
        return self.__so_ban_co_san

    #Setter -> thay doi ttin co san
    so_ban_co_san.setter
    def so_ban_co_san(self, value):
        if value < 0:
            raise ValueError("So ban co san khong the am")
        self.__so_ban_co_san = value

    def hien_thi_chi_tiet(self):
        return f"Ma tai lieu: {self.ma_tai_lieu}, Sach: {self.tieu_de}, Tac gia: {self.tac_gia}, So trang: {self.so_trang}, Nam xuat_ban: {self.nam_xuat_ban}"

class TapChi(TaiLieu):
    def __init__(self, ma_tai_lieu, tieu_de, nam_xuat_ban, so_phat_hanh, nha_xuat_ban):
        super().__init__(ma_tai_lieu, tieu_de, nam_xuat_ban)
        self.so_phat_hanh = so_phat_hanh
        self.nha_xuat_ban = nha_xuat_ban

    def hien_thi_chi_tiet(self):
        return f"Ma tai lieu: {self.ma_tai_lieu}, Sach: {self.tieu_de}, Nam: {self.nam_xuat_ban}, So luong phat hanh: {self.so_phat_hanh}, Nha xuat ban: {self.nha_xuat_ban}"

class ThuVien:
    def __init__(self):
        self.danh_sach_tai_lieu = []

    def them_tai_lieu(self, tai_lieu: TaiLieu):
        self.danh_sach_tai_lieu.append(tai_lieu)

    def xoa_tai_lieu(self, tai_lieu: TaiLieu):
        self.danh_sach_tai_lieu.remove(tai_lieu)

    def tim_kiem(self, keyword):
        return [tai_lieu for tai_lieu in self.danh_sach_tai_lieu if keyword.lower() in tai_lieu.tieu_de.lower()] #???
        #return list

    def hien_thi_tat_ca(self):
        for tai_lieu in self.danh_sach_tai_lieu:
            print(tai_lieu.hien_thi_chi_tiet())

    def thong_ke(self): #???
        return {
            "sach": sum(isinstance(tai_lieu, Sach) for tai_lieu in self.danh_sach_tai_lieu),
            "tap_chi": sum(isinstance(tai_lieu, TaiLieu) for tai_lieu in self.danh_sach_tai_lieu)
        }



lib = ThuVien()

sach_1 = Sach("S001", "Python Programming", 2020, "Jonh Doe", 350, 5)
tap_chi_1 = TapChi("T001", "Tech Monthly", 2021, 12, "Tech Publisher")

lib.them_tai_lieu(sach_1)
lib.them_tai_lieu(tap_chi_1)
lib.hien_thi_tat_ca()
print(lib.thong_ke(), "\n")

has_p_in_title = lib.tim_kiem("t")
for tai_lieu in has_p_in_title:
    print(tai_lieu.hien_thi_chi_tiet())
print()
 
lib.xoa_tai_lieu(sach_1)
lib.hien_thi_tat_ca()