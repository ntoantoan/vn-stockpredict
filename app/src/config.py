prompt_analysis = """
Vui lòng phân tích biểu đồ dựa trên các tiêu chí sau. Trả lời ngắn gọn và dễ hiểu, đồng thời cung cấp thêm thông tin để hỗ trợ quá trình ra quyết định mua cổ phiếu. PHẢN HỒI "PHẢI Ở ĐỊNH DẠNG JSON - KHÔNG PHẢI ĐỊNH DẠNG MARKDOWN". Đơn giá là Việt Nam Đồng.

tldr: Tóm tắt và đánh giá mã cổ phiếu dựa trên các tiêu chí sau: Xu hướng hiện tại, Hành động giá, Khối lượng, Hỗ trợ & Kháng cự, Dự đoán, Chiến lược giao dịch được đề xuất với giá vào lệnh và mức dừng lỗ. Kết hợp tất cả các tiêu chí đã đánh giá thành một câu ngôn ngữ tự nhiên. Viết tối đa 300 ký tự và bao trong một chuỗi, tính từ in đậm, cụm tính từ/giá trị/số/giá.

xu_huong_hien_tai: Xu hướng tăng/Đi ngang/Xu hướng giảm. Nếu đi ngang, hãy cho biết phạm vi giao dịch (hỗ trợ & kháng cự).

hanh_dong_gia: Mô tả mô hình nến gần đây, đặc biệt là gần hỗ trợ/kháng cự, viết tối thiểu 50 từ và tối đa 100 từ, tính từ in đậm, cụm tính từ/giá trị/số/giá.

ho_tro:
- muc_gan_day: 1 mức gần đây nhất.
- muc_chinh: Giá đã được kiểm tra lại nhiều lần.

khang_cu:
- muc_gan_day: 1 mức gần đây nhất.
- muc_chinh: Giá đã được kiểm tra lại nhiều lần.

khoi_luong: Nếu nó chỉ ra động lực tăng hoặc giảm cùng với xu hướng, hãy viết tối thiểu 50 từ và tối đa 100 từ, tính từ in đậm, cụm tính từ/giá trị/số/giá.

du_doan:
- du_doan: Cổ phiếu sẽ đạt đến mức giá nào, dựa trên thông tin trước đó. Giải thích lý do. Viết tối thiểu 30 từ và tối đa 70 từ, tính từ in đậm, cụm tính từ/giá trị/số/giá.
- muc_do_tin_cay: Xác định mức độ tin cậy chính.

chien_luoc_giao_dich_de_xuat:
- de_xuat: Mua/Bán/Không giao dịch.
+ Nếu Đề xuất là Mua, hãy đề xuất kỹ thuật vào lệnh (Mua tại mức hỗ trợ, Mua đột phá) với giá vào lệnh & xác nhận & giá dừng lỗ.
+ Nếu Đề xuất là Bán, hãy đề xuất kỹ thuật vào lệnh (Bán tại mức kháng cự, Bán đột phá) với giá vào lệnh & xác nhận & giá dừng lỗ.
+ Nếu Đề xuất là Không giao dịch, gợi ý Kịch bản Mua với lệnh dừng lỗ - và Kịch bản Bán với lệnh dừng lỗ, hãy viết tối thiểu 50 từ và tối đa 100 từ, tính từ in đậm, cụm tính từ/giá trị/số/giá.

Ví dụ phản hồi JSON:
{
"tldr": "",
"xu_huong_hien_tai": "",
"hanh_dong_gia": "",
"ho_tro": {
"muc_gan_day": "",
"muc_chinh": "",
},
"khang_cu": {
"muc_gan_day": "",
"muc_chinh": "",
},
"khoi_luong": "",
"du_doan": {
"du_doan": "",
"muc_do_tin_cay": "",
},
"chien_luoc_giao_dich_de_xuat": {
"de_xuat": "",
"gia_vao_lenh": "Trả về nếu đề xuất là Mua/Bán và viết tối thiểu 50 từ và tối đa 100 từ, tính từ in đậm, cụm tính từ/giá trị/số/giá.",
"xac_nhan": "Trả về nếu đề xuất là Mua/Bán và viết tối thiểu 50 từ và tối đa 100 từ, in đậm tính từ, cụm tính từ/giá trị/số/giá.",
"gia_dung_lo": "Trả về nếu đề xuất là Mua/Bán, chỉ giá",
"kich_ban_mua": "Trả về nếu đề xuất là Không giao dịch",
"kich_ban_ban": "Trả về nếu đề xuất là Không giao dịch",
}
}
"""