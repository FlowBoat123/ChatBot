# Mở file input.txt và đọc nội dung

def tim_dong_lap_lai_2_lan(danh_sach_dong):
    # Tạo từ điển để đếm số lần xuất hiện của mỗi dòng
    dem_dong = {}
    
    # Lặp qua từng dòng và đếm số lần xuất hiện
    for dong in danh_sach_dong:
        if dong in dem_dong:
            dem_dong[dong] += 1
        else:
            dem_dong[dong] = 1

    # Tìm các dòng xuất hiện chính xác 2 lần
    ket_qua = [dong for dong, so_lan in dem_dong.items() if so_lan == 2]

    return ket_qua

with open('input.txt', 'r', encoding='utf-8') as file:
    # Đọc từng dòng trong file
    # for line in file:
    #     # In từng dòng ra màn hình với dấu gạch đầu dòng
    print(tim_dong_lap_lai_2_lan(file))  # Sử dụng strip() để loại bỏ ký tự xuống dòng
