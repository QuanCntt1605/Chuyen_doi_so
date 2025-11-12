<div align="center">

# AI_AGENT ĐẶT LỊCH NHA KHOA

Nền Tảng Trợ Lý Tư Vấn & Đặt Lịch Khám Răng Thông Minh

![Nha Khoa Logo](https://cdn-icons-png.flaticon.com/512/3358/3358357.png)

Sử dụng AI để tư vấn dịch vụ, kiểm tra lịch trống và tự động đặt lịch hẹn cho khách hàng.

🚀 Demo • ✨ Tính Năng • 📦 Cài Đặt • 📖 Tài Liệu • 🤝 Đóng Góp

</div>

## 📋 Mục Lục

- [Giới Thiệu](#-giới-thiệu)
- [Tính Năng](#-tính-năng)
- [Công Nghệ](#️-công-nghệ)
- [Kiến Trúc Hệ Thống](#️-kiến-trúc-hệ-thống)
- [Cài Đặt](#-cài-đặt)
- [Sử Dụng](#-sử-dụng)
- [API Documentation](#-api-documentation)
- [Tài Liệu](#-tài-liệu)
- [Screenshots](#-screenshots)
- [Đóng Góp](#️-đóng-góp)
- [License](#-license)

## 🎯 Giới Thiệu
Dental Appointment Agent là nền tảng AI Agent thông minh được thiết kế để tự động hóa quy trình tư vấn và đặt lịch hẹn cho các phòng khám nha khoa. Sử dụng sức mạnh của **Groq LLM** và **LangChain**, Agent này giúp khách hàng:

- 🤖 **Tư vấn dịch vụ** - AI giới thiệu các gói khám, dịch vụ niềng răng, tẩy trắng, v.v.
- 📅 **Kiểm tra lịch hẹn** - Kiểm tra giờ và ngày còn trống của phòng khám.
- 📝 **Đặt lịch hẹn** - Thu thập thông tin cần thiết và lưu lịch hẹn vào cơ sở dữ liệu.
- 📱 **Thu thập thông tin** - Hỏi tên, số điện thoại, dịch vụ quan tâm và thời gian mong muốn.
- 💾 **Lưu thông tin khách hàng** - Tự động lưu vào cơ sở dữ liệu MySQL khi khách xác nhận đặt lịch.
- 🗨️ **Hội thoại tự nhiên** - Giữ bộ nhớ session để trò chuyện liền mạch và hiệu quả.

🌟 **Điểm Đặc Biệt**

- ✅ **AI Thông Minh** - Sử dụng Groq LLM (Llama 3) cho phản hồi siêu tốc.
- ✅ **Tool Calling** - Sử dụng các tool (hàm) để kiểm tra lịch trống và lưu lịch hẹn.
- ✅ **Tiếng Việt** - Giao diện và hội thoại hoàn toàn bằng Tiếng Việt.
- ✅ **Session Management** - Duy trì lịch sử chat qua UUID.

## ✨ Tính Năng
🤖 **1. Tư Vấn Dịch Vụ Nha Khoa**

- Chào đón khách và giới thiệu các gói khám, dịch vụ nổi bật (VD: Tẩy trắng, Nhổ răng khôn, Niềng răng).
- Cung cấp thông tin chi tiết về quy trình và chi phí (tùy thuộc vào prompt).

📅 **2. Quản Lý & Đặt Lịch Hẹn**

- **Tool `check_availability`**: Kiểm tra các khung giờ trống cho dịch vụ và ngày cụ thể.
- **Tool `book_appointment`**: Gọi tool này sau khi thu thập đủ thông tin để lưu lịch hẹn.
- Đảm bảo khách hàng cung cấp đầy đủ: **Tên**, **Số điện thoại**, **Dịch vụ**, **Ngày/Giờ mong muốn**.

📝 **3. Thu Thập Thông Tin Khách Hàng**

- Bắt buộc hỏi: **Tên**, **Số điện thoại**, **Dịch vụ** và **Thời gian hẹn**.
- Xác nhận lại thông tin trước khi gọi tool đặt lịch.
- Lưu lịch sử chat vào DB cho mỗi session.

💾 **4. Lưu Dữ Liệu Khám Răng**

- Lưu vào bảng `appointments`: Tên, SĐT, Dịch vụ, Ngày/Giờ hẹn, Trạng thái (Pending/Confirmed).
- Tạo session mới sau khi đặt lịch thành công.

🛡️ **5. Quản Lý Lỗi Và Bảo Mật**

- Xử lý lỗi kết nối API và DB.
- CORS hỗ trợ frontend.
- Verbose logging để debug agent actions và tool calls.

## 🛠️ Công Nghệ
### Backend Stack
| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|-----------|----------|
| [Python](https://python.org) | 3.12+ | Ngôn ngữ chính |
| [FastAPI](https://fastapi.tiangolo.com) | Latest | Web framework (async) |
| [Uvicorn](https://uvicorn.org) | Latest | ASGI server |
| [Groq LLM](https://groq.com) | Llama 3 | LLM - Phân tích hội thoại, Tool Calling |
| [LangChain](https://python.langchain.com) | Latest | Agent framework (tools, memory) |
| [Pydantic](https://pydantic.dev) | V2 | Data validation và định nghĩa Tool Schema |
| [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/) | 8.x | Kết nối DB |
| [dotenv](https://pypi.org/project/python-dotenv) | Latest | Quản lý biến môi trường |

### Frontend (Tích Hợp)
- Giao diện chat đơn giản, hiển thị các bước đặt lịch.
- Sử dụng Fetch API để gọi backend.

### AI Models
- 🤖 **Groq Llama 3** (model: llama3-8b-8192)
  - Xử lý hội thoại tự nhiên, hiểu ý định của người dùng.
  - Quản lý logic đặt lịch (gọi tool khi đủ thông tin).

## 📦 Cài Đặt
### Yêu Cầu Hệ Thống
- Python 3.12 trở lên
- MySQL Server 8.0+
- [Groq API Key](https://console.groq.com/keys) (miễn phí với giới hạn)

### Bước 1: Clone Repository
### Bước 2: Tạo Virtual Environment
### Bước 3: Cài Đặt Dependencies
### Bước 4: Setup Database & .env
1. **Tạo DB**: Chạy script SQL để tạo các tables cần thiết (`sessions`, `messages`, `appointments`).
2. **File `.env`**:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_DATABASE=dental_agent
   API_KEY=your_groq_api_key
   model=llama3-8b-8192  # Hoặc model khác hỗ trợ bởi Groq
   ```

### Bước 5: Chạy Server
### Bước 6: Kết Nối Frontend
- Tích hợp API vào giao diện chat của phòng khám.
- API sẽ nhận request từ `/chat`.

## 🚀 Sử Dụng
### Test API Với Curl
### Flow Chatbot
1. **Khởi tạo**: Gửi message → AI chào và hỏi về nhu cầu (dịch vụ).
2. **Thu thập thông tin**: AI hỏi tên, SĐT, ngày/giờ mong muốn.
3. **Kiểm tra lịch**: AI gọi tool `check_availability`.
4. **Xác nhận & Đặt lịch**: User xác nhận → AI gọi tool `book_appointment` → Lưu DB và tạo session mới.

## 📖 API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **Endpoints**:
  - `POST /chat`: Xử lý tin nhắn (required: `message`; optional: `session_uuid`).
  - `OPTIONS /chat`: CORS preflight.

Chi tiết: Xem `/docs` hoặc file `main.py`.

## 📚 Tài Liệu
- [API Endpoints Guide](docs/API_ENDPOINTS_GUIDE.md) - Hướng dẫn chi tiết endpoints.
- [Database Schema](docs/DB_SCHEMA.md) - Cấu trúc tables (`appointments`).
- [LangChain Setup](docs/LANGCHAIN_SETUP.md) - Cấu hình agent và tools (ví dụ: `check_availability`, `book_appointment`).

## 📸 Screenshots
*(Bạn có thể thêm các ảnh chụp màn hình giao diện chat hoặc log đặt lịch tại đây)*

## 🤝 Đóng Góp
Contributions, issues và feature requests đều được chào đón!

1. Fork repository.
2. Tạo branch (`git checkout -b feature/AddAppointmentTool`).
3. Commit changes (`git commit -m 'Implement check_availability tool'`).
4. Push to branch (`git push origin feature/AddAppointmentTool`).
5. Mở Pull Request.

## 📄 License
MIT License - xem file `LICENSE` để biết chi tiết.

## 👨‍💻 Tác Giả
QuanNao

- GitHub: 
- Email: wwandzvcl2004@gmail.com
- Zalo: 0345377187

🙏 **Acknowledgments**

- [Groq](https://groq.com) - LLM nhanh chóng cho Tool Calling.
- [FastAPI](https://fastapi.tiangolo.com) - Framework mạnh mẽ.
- [LangChain](https://python.langchain.com) - Agent và tools.

⭐ **Cảm ơn bạn đã xem** ⭐
