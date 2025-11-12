import streamlit as st
import os
import json
import datetime # Thêm thư viện datetime
from dotenv import load_dotenv

# Thư viện LangChain
from pydantic import BaseModel, Field
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

# Tải biến môi trường
load_dotenv()

# --- 1. CẤU HÌNH HỆ THỐNG & QUẢN LÝ DỮ LIỆU ---

# Tên file lưu trữ lịch hẹn
APPOINTMENTS_FILE = "appointments.json"

# Danh sách dịch vụ nha khoa
AVAILABLE_SERVICES = {
    "Khám Răng Định Kỳ": {"duration": "30 phút", "price": "300.000 VND"},
    "Tẩy Trắng Răng": {"duration": "60 phút", "price": "1.200.000 VND"},
    "Trám Răng": {"duration": "45 phút", "price": "500.000 VND"},
    "Niềng Răng": {"duration": "120 phút", "price": "20.000.000 VND"}
}

# --- HÀM QUẢN LÝ FILE JSON ---

def load_appointments():
    """Tải lịch hẹn từ file JSON."""
    if os.path.exists(APPOINTMENTS_FILE):
        try:
            with open(APPOINTMENTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # File trống hoặc bị hỏng, trả về danh sách rỗng
            return []
    return []

def save_appointments(appointments_list):
    """Lưu lịch hẹn vào file JSON."""
    try:
        with open(APPOINTMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(appointments_list, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        st.error(f"Lỗi khi lưu dữ liệu vào file {APPOINTMENTS_FILE}: {e}")
        return False

# Khởi tạo danh sách lịch hẹn trong session state từ file
if 'SCHEDULED_APPOINTMENTS' not in st.session_state:
    st.session_state.SCHEDULED_APPOINTMENTS = load_appointments()


# --- 2. LOGIC ĐẶT LỊCH CHUNG ---

def _book_appointment_logic(customer_name: str, service_name: str, date_time: str) -> str:
    """Chứa logic đặt lịch khám răng và lưu vào file."""
    
    # 1. Chuẩn hóa tên dịch vụ
    normalized_service_name_input = service_name.strip().lower()
    found_key = None
    for key in AVAILABLE_SERVICES.keys():
        if key.strip().lower() == normalized_service_name_input:
            found_key = key
            break
    if not found_key:
        return f"Lỗi: Dịch vụ '{service_name}' không hợp lệ. Vui lòng chọn từ danh sách hiện có."
    
    service_name = found_key

    # 2. Kiểm tra trùng lịch
    for appt in st.session_state.SCHEDULED_APPOINTMENTS:
        if appt['date_time'] == date_time:
            return f"Lỗi: Lịch hẹn vào {date_time} đã có khách. Vui lòng chọn thời gian khác."
    
    # 3. Thêm lịch vào session_state
    appointment_details = {
        "customer_name": customer_name,
        "service_name": service_name,
        "date_time": date_time,
        "details": AVAILABLE_SERVICES[service_name]
    }
    st.session_state.SCHEDULED_APPOINTMENTS.append(appointment_details)
    
    # 4. Lưu dữ liệu vào file
    save_success = save_appointments(st.session_state.SCHEDULED_APPOINTMENTS)
    save_status = "Đã lưu vào file." if save_success else "LƯU VÀO FILE THẤT BẠI."
    
    return (
        f"XÁC NHẬN ĐẶT LỊCH KHÁM RĂNG THÀNH CÔNG:\n"
        f"Khách hàng: {customer_name}\n"
        f"Dịch vụ: {service_name}\n"
        f"Thời gian: {date_time}\n"
        f"Chi tiết: {AVAILABLE_SERVICES[service_name]['duration']}, {AVAILABLE_SERVICES[service_name]['price']}\n"
        f"[{save_status}]\n"
        f"Phòng khám rất hân hạnh được phục vụ quý khách!"
    )


# --- 3. CÁC TOOLS CHO AGENT ---

@tool
def list_available_services(query: str = "") -> str:
    """Liệt kê các dịch vụ nha khoa hiện có, thời gian và giá."""
    service_list = "\n".join([
        f"- {name} ({data['duration']}, {data['price']})"
        for name, data in AVAILABLE_SERVICES.items()
    ])
    return f"Các dịch vụ hiện có tại phòng khám nha khoa:\n{service_list}"

class BookAppointmentSchema(BaseModel):
    """Định nghĩa input cần thiết để đặt lịch khám răng."""
    customer_name: str = Field(description="Tên đầy đủ của khách hàng.")
    service_name: str = Field(description="Tên dịch vụ nha khoa muốn đặt (Phải khớp với danh sách).")
    date_time: str = Field(description="Ngày và giờ đặt lịch (Ví dụ: '25/12/2025 lúc 14:00').")

@tool(args_schema=BookAppointmentSchema)
def book_dental_appointment(customer_name: str, service_name: str, date_time: str) -> str:
    """Đặt lịch khám răng cho khách hàng. Cần đủ Tên, Dịch vụ, Ngày/Giờ."""
    # Gọi hàm logic đặt lịch
    return _book_appointment_logic(customer_name, service_name, date_time)

@tool
def check_all_appointments(query: str = "") -> str:
    """Liệt kê tất cả các lịch hẹn khám răng đã đặt."""
    if not st.session_state.SCHEDULED_APPOINTMENTS:
        return "Hiện tại chưa có lịch hẹn nào."
    
    return "Danh sách lịch hẹn đã đặt:\n" + "\n".join([
        f"Khách: {appt['customer_name']} | Dịch vụ: {appt['service_name']} | Lúc: {appt['date_time']}"
        for appt in st.session_state.SCHEDULED_APPOINTMENTS
    ])

# --- 4. KHỞI TẠO AGENT ---

@st.cache_resource
def initialize_dental_agent():
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")

    if GEMINI_KEY:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0,
            google_api_key=GEMINI_KEY
        )
    else:
        st.error("⚠️ Vui lòng thiết lập biến môi trường GEMINI_API_KEY trong file .env trước khi chạy ứng dụng.")
        return None

    tools = [list_available_services, book_dental_appointment, check_all_appointments]

    system_prompt = (
        "Bạn là 'Dental Booking Agent', trợ lý AI thân thiện và chuyên nghiệp. "
        "Nhiệm vụ: "
        "1. Liệt kê dịch vụ nha khoa bằng tool `list_available_services`. "
        "2. Đặt lịch khám răng bằng tool `book_dental_appointment`. "
        "3. Để đặt lịch, phải có đủ 3 thông tin: Tên khách, Dịch vụ, Ngày/Giờ. "
        "4. Giao tiếp bằng tiếng Việt."
    )

    agent_executor = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=False,
        agent_kwargs={"system_message": system_prompt},
        handle_parsing_errors=True
    )
    
    return agent_executor

# --- 5. GIAO DIỆN STREAMLIT ---

st.set_page_config(page_title="Dental AI Booking Agent", layout="wide")
st.title("🦷 Dental AI Booking Agent - Tư Vấn & Đặt Lịch Nha Khoa")

dental_agent = initialize_dental_agent()

if dental_agent:
    # --- 5.1. Giao diện Sidebar (Form Đặt Lịch Nhanh & Danh sách Lịch Hẹn) ---
    with st.sidebar:
        st.header("Đặt Lịch Nhanh 📝")

        # Form Đặt Lịch Nhanh
        with st.form("quick_booking_form"):
            st.markdown("**Điền thông tin để đặt lịch ngay!**")
            name = st.text_input("Tên Khách Hàng:", key="form_name")
            service = st.selectbox("Chọn Dịch Vụ:", list(AVAILABLE_SERVICES.keys()), key="form_service")
            
            # Thay thế text input bằng date_input và time_input
            col_date, col_time = st.columns(2)
            with col_date:
                appointment_date = st.date_input("Chọn Ngày:", min_value=datetime.date.today(), key="form_date")
            with col_time:
                # Thiết lập giờ mặc định là 9:00 sáng
                appointment_time = st.time_input("Chọn Giờ:", value=datetime.time(9, 0), step=900, key="form_time") 

            # Kết hợp ngày và giờ thành chuỗi định dạng
            # Ví dụ: "15/10/2025 09:00"
            if appointment_date and appointment_time:
                date_time_str = f"{appointment_date.strftime('%d/%m/%Y')} {appointment_time.strftime('%H:%M')}"
            else:
                date_time_str = ""

            submitted = st.form_submit_button("Xác Nhận Đặt Lịch")

            if submitted:
                if name and date_time_str:
                    # GỌI HÀM LOGIC ĐẶT LỊCH (KHÔNG PHẢI TOOL)
                    result = _book_appointment_logic(
                        customer_name=name, 
                        service_name=service, 
                        date_time=date_time_str
                    )
                    st.success(result)
                    # Sau khi đặt lịch, cần reload sidebar để cập nhật danh sách
                    st.rerun() 
                else:
                    st.error("Vui lòng điền đầy đủ Tên, Dịch Vụ, Ngày & Giờ.")
        
        st.markdown("---")
        st.header("Lịch Hẹn Đã Đặt (Được lưu trong file)")
        if st.session_state.SCHEDULED_APPOINTMENTS:
            for i, appt in enumerate(st.session_state.SCHEDULED_APPOINTMENTS):
                st.markdown(f"**Lịch #{i+1}**")
                st.markdown(f"Khách: **{appt['customer_name']}**")
                st.markdown(f"Dịch vụ: **{appt['service_name']}**")
                st.markdown(f"Thời gian: **{appt['date_time']}**")
                st.markdown("---")
        else:
            st.info("Chưa có lịch hẹn nào được đặt.")

    # --- 5.2. Giao diện Chatbot ---

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Xin chào! Tôi là Dental Booking Agent. Tôi có thể giúp bạn xem dịch vụ, đặt lịch khám hoặc kiểm tra lịch đã đặt."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hỏi tôi về dịch vụ hoặc đặt lịch..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Agent đang xử lý..."):
                try:
                    # Gọi Agent để xử lý yêu cầu (có thể gọi tool hoặc trả lời thông thường)
                    result = dental_agent.invoke({"input": prompt})
                    response = result['output']
                except Exception as e:
                    response = f"Lỗi hệ thống khi gọi AI: {e}"

            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Cần reload sidebar sau khi chat để cập nhật danh sách lịch đặt (nếu có)
        if "XÁC NHẬN ĐẶT LỊCH KHÁM RĂNG THÀNH CÔNG" in response:
             st.rerun()