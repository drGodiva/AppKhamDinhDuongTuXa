import streamlit as st
import requests
import json
import urllib.parse

# 1. LINK WEBHOOK GOOGLE APPS SCRIPT
URL_WEBHOOK_GOOGLE_SHEET = "https://script.google.com/macros/s/AKfycbwdriqO51UiAKejdJOvZsQU6To-YAqQEPzkKTloOPhmkOeYQ6ow4H9Jsj3k85hMPHKODQ/exec"

# 2. Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="Học Viện MBA - Kiểm Soát Sinh Học & Tầm Soát Sức Khỏe",
    page_icon="🧬",
    layout="wide"
)

# Giao diện nhận diện MBA: Xanh ngọc lục bảo và chữ vàng kim
css_style = """
<style>
.stApp { background-color: #004d40; color: #F0F4F8; }
h1 { color: #D4AF37 !important; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6); text-align: center; font-weight: bold; }
h2, h3 { color: #F7D070 !important; }
.box-lead { background: rgba(255, 255, 255, 0.08); border: 2px solid #D4AF37; border-radius: 12px; padding: 20px; margin-bottom: 25px; }
.metric-card { background-color: rgba(0, 0, 0, 0.25); border: 1px solid rgba(212, 175, 55, 0.4); padding: 16px; border-radius: 10px; margin-top: 15px; }
.metric-val { font-size: 26px; font-weight: bold; color: #FFE082; }
.report-card { background-color: #064037; border: 2px solid #D4AF37; border-radius: 12px; padding: 24px; margin-top: 25px; }
label, p, span { color: #F0F4F8 !important; }
.stButton>button { background-color: #D4AF37; color: #00332C; font-weight: bold; border-radius: 8px; padding: 12px 24px; width: 100%; border: none; }
.stButton>button:hover { background-color: #F7D070; color: #00221D; }
.btn-zalo { display: inline-block; background-color: #0068FF; color: #FFFFFF !important; font-weight: bold; text-align: center; padding: 14px 24px; border-radius: 8px; text-decoration: none; font-size: 16px; width: 100%; margin-top: 15px; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

st.markdown("<h1>HỌC VIỆN MBA - CÔNG CỤ TÍNH CHỈ SỐ SINH HỌC & CHUYỂN HÓA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 15px; color: #CBD5E1;'>Hệ thống sàng lọc, túm bắt vấn đề chuyển hóa và tư vấn phục hồi sinh học tế bào</p>", unsafe_allow_html=True)
st.markdown("---")

# ==================== BƯỚC 1: THÔNG TIN HỒ SƠ ====================
st.markdown("<div class='box-lead'>", unsafe_allow_html=True)
st.subheader("📋 BƯỚC 1: THÔNG TIN HỒ SƠ SINH HỌC CÁ NHÂN")
st.caption("Điền thông tin để hệ thống xuất Báo cáo phân tích chuyên sâu gửi về Email và hỗ trợ tư vấn trực tiếp.")

col_lead1, col_lead2, col_lead3, col_lead4 = st.columns([1.2, 1.0, 1.2, 1.4])
with col_lead1:
    HoTen = st.text_input("Họ và Tên (*):", placeholder="Ví dụ: Nguyễn Văn A", key="lead_name")
with col_lead2:
    SoDienThoai = st.text_input("Số điện thoại / Zalo (*):", placeholder="0909xxxxxx", key="lead_phone")
with col_lead3:
    EmailKhach = st.text_input("Email (nếu có để nhận Ebook):", placeholder="vidu@gmail.com", key="lead_email")
with col_lead4:
    VanDeQuanTam = st.selectbox(
        "Vấn đề quan tâm hàng đầu:",
        [
            "Bụng to, mỡ nội tạng khó giảm",
            "Đường huyết cao / Lo sợ tiểu đường",
            "Mệt mỏi mạn tính, thiếu hụt năng lượng",
            "Mất ngủ, khó ngủ sâu giấc",
            "Yếu cơ, teo cơ, đau nhức xương khớp",
            "Tăng huyết áp / Mỡ máu / Nguy cơ tim mạch"
        ],
        key="lead_problem"
    )
st.markdown("</div>", unsafe_allow_html=True)

# Bộ nhớ tạm phiên làm việc
if "data_metrics" not in st.session_state:
    st.session_state.data_metrics = {
        "WHtR": None,
        "WHR": None,
        "RFM": None,
        "BMR": None,
        "MatNuoc": None,
        "CanhBao": []
    }

# ==================== BƯỚC 2: 5 TAB CÔNG THỨC ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. WHtR (Eo / Chiều cao)",
    "2. WHR (Eo / Mông)",
    "3. RFM (% Mỡ cơ thể)",
    "4. BMR (Chuyển hóa cơ bản)",
    "5. Tỷ Lệ Mất Nước"
])

# 1. WHtR
with tab1:
    st.subheader("Tỷ lệ Vòng eo / Chiều cao (WHtR)")
    col1, col2 = st.columns(2)
    with col1:
        VongBung_WHtR = st.number_input("Vòng bụng ngang rốn (cm):", min_value=30.0, max_value=200.0, value=78.0, step=0.5, key="whtr_vb")
    with col2:
        ChieuCao_WHtR = st.number_input("Chiều cao (cm):", min_value=80.0, max_value=250.0, value=165.0, step=0.5, key="whtr_cc")

    if st.button("Lưu & Đánh Giá Chỉ Số WHtR", key="btn_whtr"):
        if ChieuCao_WHtR > 0:
            val = round(VongBung_WHtR / ChieuCao_WHtR, 2)
            st.session_state.data_metrics["WHtR"] = val
            st.markdown("<div class='metric-card'>Chỉ số WHtR: <span class='metric-val'>" + str(val) + "</span></div>", unsafe_allow_html=True)
            if val >= 0.5:
                warn = "WHtR = " + str(val) + " (≥ 0.5): Mỡ nội tạng bao quanh tạng phủ cao, nguy cơ xơ vữa mạch máu và rối loạn chuyển hóa."
                if warn not in st.session_state.data_metrics["CanhBao"]:
                    st.session_state.data_metrics["CanhBao"].append(warn)
                st.warning("⚠️ " + warn)
            else:
                st.success("✅ Chỉ số an toàn: Mức tích tụ mỡ trung tâm trong giới hạn kiểm soát tốt.")

# 2. WHR
with tab2:
    st.subheader("Tỷ lệ Vòng eo / Vòng mông (WHR)")
    col1, col2, col3 = st.columns(3)
    with col1:
        GioiTinh_WHR = st.radio("Giới tính:", ["Nam", "Nữ"], horizontal=True, key="whr_sex")
    with col2:
        VongBung_WHR = st.number_input("Vòng bụng (cm):", min_value=30.0, max_value=200.0, value=82.0, step=0.5, key="whr_vb")
    with col3:
        VongMong_WHR = st.number_input("Vòng mông (cm):", min_value=30.0, max_value=220.0, value=92.0, step=0.5, key="whr_vm")

    if st.button("Lưu & Đánh Giá Chỉ Số WHR", key="btn_whr"):
        if VongMong_WHR > 0:
            val = round(VongBung_WHR / VongMong_WHR, 2)
            st.session_state.data_metrics["WHR"] = val
            is_danger = (GioiTinh_WHR == "Nam" and val > 0.90) or (GioiTinh_WHR == "Nữ" and val > 0.85)
            st.markdown("<div class='metric-card'>Chỉ số WHR: <span class='metric-val'>" + str(val) + "</span></div>", unsafe_allow_html=True)
            if is_danger:
                warn = "WHR = " + str(val) + ": Dáng quả táo, mỡ chèn ép tuần hoàn nội tạng, nguy cơ gan nhiễm mỡ."
                if warn not in st.session_state.data_metrics["CanhBao"]:
                    st.session_state.data_metrics["CanhBao"].append(warn)
                st.warning("⚠️ " + warn)
            else:
                st.success("✅ Phân bố mỡ cơ thể cân đối.")

# 3. RFM
with tab3:
    st.subheader("Relative Fat Mass (RFM - Ước tính % Mỡ cơ thể)")
    col1, col2, col3 = st.columns(3)
    with col1:
        GioiTinh_RFM = st.radio("Giới tính:", ["Nam", "Nữ"], horizontal=True, key="rfm_sex")
    with col2:
        ChieuCao_RFM = st.number_input("Chiều cao (cm):", value=165.0, step=0.5, key="rfm_cc")
    with col3:
        VongEo_RFM = st.number_input("Vòng eo (cm):", value=78.0, step=0.5, key="rfm_ve")

    if st.button("Lưu & Đánh Giá % Mỡ RFM", key="btn_rfm"):
        if VongEo_RFM > 0:
            rfm = round((64.0 - (20.0 * (ChieuCao_RFM / VongEo_RFM))) if GioiTinh_RFM == "Nam" else (76.0 - (20.0 * (ChieuCao_RFM / VongEo_RFM))), 1)
            st.session_state.data_metrics["RFM"] = rfm
            st.markdown("<div class='metric-card'>Tỷ lệ mỡ cơ thể (RFM): <span class='metric-val'>" + str(rfm) + "%</span></div>", unsafe_allow_html=True)
            if (GioiTinh_RFM == "Nam" and rfm > 25) or (GioiTinh_RFM == "Nữ" and rfm > 32):
                warn = "RFM = " + str(rfm) + "%: Lượng mỡ dư thừa vượt ngưỡng an toàn, cảnh báo nguy cơ gan nhiễm mỡ và đề kháng insulin."
                if warn not in st.session_state.data_metrics["CanhBao"]:
                    st.session_state.data_metrics["CanhBao"].append(warn)
                st.warning("⚠️ " + warn)
            else:
                st.success("✅ Tỷ lệ mỡ cơ thể trong ngưỡng bình thường.")

# 4. BMR
with tab4:
    st.subheader("Tiêu Hao Năng Lượng Cơ Bản (BMR)")
    col1, col2 = st.columns(2)
    with col1:
        GioiTinh_BMR = st.radio("Giới tính:", ["Nam", "Nữ"], horizontal=True, key="bmr_sex")
        Tuoi_BMR = st.number_input("Tuổi:", min_value=10, max_value=120, value=40, step=1, key="bmr_age")
    with col2:
        CanNang_BMR = st.number_input("Cân nặng (kg):", value=62.0, step=0.5, key="bmr_w")
        ChieuCao_BMR = st.number_input("Chiều cao (cm):", value=165.0, step=0.5, key="bmr_h")

    if st.button("Lưu & Đánh Giá BMR", key="btn_bmr"):
        bmr = int((10.0 * CanNang_BMR) + (6.25 * ChieuCao_BMR) - (5.0 * Tuoi_BMR) + (5.0 if GioiTinh_BMR == "Nam" else -161.0))
        st.session_state.data_metrics["BMR"] = bmr
        st.markdown("<div class='metric-card'>Tiêu hao BMR: <span class='metric-val'>" + str(bmr) + " kcal/ngày</span></div>", unsafe_allow_html=True)

# 5. Mất Nước
with tab5:
    st.subheader("Tỷ Lệ Mất Nước Ước Tính")
    col1, col2 = st.columns(2)
    with col1:
        Truoc = st.number_input("Cân nặng trước (kg):", value=62.0, step=0.1, key="dehyd_b")
    with col2:
        Sau = st.number_input("Cân nặng sau (kg):", value=61.2, step=0.1, key="dehyd_a")

    if st.button("Lưu & Đánh Giá Mất Nước", key="btn_dehyd"):
        if Truoc > 0:
            loss = round(((Truoc - Sau) / Truoc) * 100.0, 2)
            st.session_state.data_metrics["MatNuoc"] = loss
            st.markdown("<div class='metric-card'>Tỷ lệ mất nước: <span class='metric-val'>" + str(loss) + "%</span></div>", unsafe_allow_html=True)
            if loss > 2.0:
                warn = "Mất nước " + str(loss) + "% (> 2%): Giảm dịch thể lưu thông, máu quánh đặc, ảnh hưởng huyết động."
                if warn not in st.session_state.data_metrics["CanhBao"]:
                    st.session_state.data_metrics["CanhBao"].append(warn)
                st.warning("⚠️ " + warn)
            else:
                st.success("✅ Mức dịch thể ổn định.")

# ==================== BƯỚC 3: GỬI WEBHOOK & XUẤT BÁO CÁO ====================
st.markdown("---")
st.subheader("🎯 BƯỚC 3: TỔNG HỢP BÁO CÁO & LƯU HỒ SƠ VỀ GOOGLE SHEET")

if st.button("📥 BẤM ĐỂ LƯU VÀO GOOGLE SHEET & XUẤT BÁO CÁO TƯ VẤN"):
    if not HoTen or not SoDienThoai:
        st.error("⚠️ Thầy/Khách hàng vui lòng điền đầy đủ Họ Tên và Số Điện Thoại ở BƯỚC 1 trước khi lưu!")
    else:
        m = st.session_state.data_metrics
        whtr_txt = str(m['WHtR']) if m['WHtR'] else "Chưa nhập"
        whr_txt = str(m['WHR']) if m['WHR'] else "Chưa nhập"
        rfm_txt = str(m['RFM']) + "%" if m['RFM'] else "Chưa nhập"
        bmr_txt = str(m['BMR']) + " kcal" if m['BMR'] else "Chưa nhập"
        loss_txt = str(m['MatNuoc']) + "%" if m['MatNuoc'] else "Chưa nhập"

        payload = {
            "HoTen": HoTen,
            "SoDienThoai": SoDienThoai,
            "Email": EmailKhach,
            "VanDeQuanTam": VanDeQuanTam,
            "WHtR": whtr_txt,
            "WHR": whr_txt,
            "RFM": rfm_txt,
            "BMR": bmr_txt,
            "MatNuoc": loss_txt
        }

        with st.spinner("Đang lưu trữ dữ liệu và kích hoạt hệ thống tư vấn..."):
            try:
                res = requests.post(URL_WEBHOOK_GOOGLE_SHEET, data=json.dumps(payload), timeout=10)
                ket_qua = res.json()

                if ket_qua.get("status") == "success":
                    st.success("🎉 DỮ LIỆU ĐÃ ĐƯỢC LƯU VÀO GOOGLE SHEET VÀ TỰ ĐỘNG GỬI EMAIL THÀNH CÔNG!")

                    # GIAO DIỆN THỨ 2: TƯ VẤN TRỰC TIẾP TẠI BÀN
                    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
                    st.markdown("<h2 style='color:#D4AF37; text-align:center; margin-top:0;'>PHIẾU TƯ VẤN SỨC KHỎE TẠI BÀN</h2>", unsafe_allow_html=True)
                    st.write(f"**Họ và tên:** {ket_qua.get('HoTen')} | **SĐT:** {ket_qua.get('SoDienThoai')}")
                    st.write(f"**Mức độ nguy cơ:** {ket_qua.get('MucDoNguyCo')}")
                    st.markdown("---")
                    st.markdown("#### 1. TỔNG HỢP NGUY CƠ LÂM SÀNG:")
                    st.info(ket_qua.get('KetLuanTongHop'))
                    st.markdown("#### 2. LỜI KHUYÊN & GIẢI PHÁP DINH DƯỠNG TẾ BÀO:")
                    st.success(ket_qua.get('PhacDoDinhDuong'))
                    st.caption(f"Trạng thái thư: {ket_qua.get('EmailStatus')}")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(f"Lỗi phản hồi từ Google Sheet: {ket_qua.get('message')}")
            except Exception as e:
                st.warning(f"Lưu ý: Không thể kết nối với Webhook (Lỗi: {e}). Dữ liệu vẫn sẵn sàng để gửi qua Zalo.")

        # NÚT GỬI HỒ SƠ QUA ZALO THS JONATHAN PHỤNG
        msg_text = (
            "KÍNH GỬI THS JONATHAN PHỤNG - MBA\n"
            "Hồ sơ sàng lọc sinh học thực địa Trà Vinh:\n"
            f"• Họ và Tên: {HoTen}\n"
            f"• Số điện thoại: {SoDienThoai}\n"
            f"• Email: {EmailKhach if EmailKhach else 'Không có'}\n"
            f"• Nỗi lo quan tâm: {VanDeQuanTam}\n"
            "--------------------------\n"
            f"KẾT QUẢ: WHtR: {whtr_txt} | WHR: {whr_txt} | %Mỡ RFM: {rfm_txt} | BMR: {bmr_txt} | Mất nước: {loss_txt}"
        )
        zalo_link = "https://zalo.me/0909380181?text=" + urllib.parse.quote(msg_text)

        st.markdown(f'<a href="{zalo_link}" target="_blank" class="btn-zalo">📲 BẤM VÀO ĐÂY ĐỂ GỬI HỒ SƠ QUA ZALO BÁC SĨ (0909 380 181)</a>', unsafe_allow_html=True)
