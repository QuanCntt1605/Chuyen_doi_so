<div align="center">

# Mixue Chat Assistant

Nền Tảng Trợ Lý Đặt Hàng Thông Minh Cho Mixue

![Mixue Logo](https://z-cdn-media.chatglm.cn/files/02125486-3cea-4a7e-a46a-c625a4738ea0_pasted_image_1760946317368.png?auth_key=1792482330-9103a701e84d4413b5b1d2c56f9883e6-0-ac321e285660450ea2c4a14880a45cae)

Sử dụng AI để giới thiệu menu, xử lý đơn hàng và lưu thông tin khách hàng một cách tự động  

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
Mixue Chat Assistant là nền tảng chatbot thông minh được xây dựng cho Mixue - thương hiệu trà sữa và đồ uống nổi tiếng. Sử dụng sức mạnh của **Groq LLM** và **LangChain**, Mixue Chat Assistant giúp khách hàng:

- 🤖 **Giới thiệu menu tự động** - AI chào đón và gợi ý món dựa trên menu nổi bật.
- 🍦 **Xử lý đơn hàng** - Chọn món, thêm vào giỏ và tính tổng tiền.
- 📱 **Thu thập thông tin** - Hỏi tên, số điện thoại và loại đơn hàng (Ăn tại quán/Mang về).
- 💾 **Lưu đơn hàng** - Tự động lưu vào cơ sở dữ liệu MySQL khi khách xác nhận.
- 🗨️ **Hội thoại tự nhiên** - Giữ bộ nhớ session để trò chuyện liền mạch.

🌟 **Điểm Đặc Biệt**

- ✅ **AI Thông Minh** - Sử dụng Groq LLM (Llama 3) cho phản hồi nhanh chóng.
- ✅ **Session Management** - Duy trì lịch sử chat qua UUID.
- ✅ **Tiếng Việt** - Giao diện và hội thoại hoàn toàn tiếng Việt.
- ✅ **Menu Đa Dạng** - 9 món nổi bật từ Mixue với giá và tag (Must Try, Best Seller...).

## ✨ Tính Năng
🤖 **1. Giới Thiệu Menu Tự Động**

- Chào đón khách và giới thiệu menu ngay từ tin nhắn đầu tiên.
- Gợi ý món theo tag: Must Try, Best Seller, Hot Trend.
- Hiển thị chi tiết: Tên món, giá, hình ảnh (từ frontend).

📋 **2. Xử Lý Đơn Hàng**

- Chọn món từ menu (click hoặc chat).
- Tính tổng tiền và hiển thị đơn hàng.

📝 **3. Thu Thập Thông Tin Khách Hàng**

- Bắt buộc hỏi: **Tên**, **Số điện thoại**, **Loại đơn hàng** (Ăn tại quán/Mang về).
- Xác nhận thông tin trước khi lưu.
- Lưu lịch sử chat vào DB cho mỗi session.

💾 **4. Lưu Và Quản Lý Đơn Hàng**

- Gọi tool `save_order_tool` khi xác nhận.
- Lưu vào bảng `orders`: Tên, SĐT, loại đơn, items (JSON), tổng tiền.
- Tạo session mới sau khi lưu đơn.

🛡️ **5. Quản Lý Lỗi Và Bảo Mật**

- Xử lý lỗi kết nối API và DB.
- CORS hỗ trợ frontend (localhost hoặc bất kỳ domain).
- Verbose logging để debug agent actions.

## 🛠️ Công Nghệ
### Backend Stack
| Công Nghệ | Phiên Bản | Mục Đích |
|-----------|-----------|----------|
| [Python](https://python.org) | 3.12+ | Ngôn ngữ chính |
| [FastAPI](https://fastapi.tiangolo.com) | Latest | Web framework (async) |
| [Uvicorn](https://uvicorn.org) | Latest | ASGI server |
| [Groq LLM](https://groq.com) | Llama 3 | LLM - Phân tích hội thoại |
| [LangChain](https://python.langchain.com) | Latest | Agent framework (tools, memory) |
| [Pydantic](https://pydantic.dev) | V2 | Data validation |
| [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/) | 8.x | Kết nối DB |
| [dotenv](https://pypi.org/project/python-dotenv) | Latest | Quản lý biến môi trường |

### Frontend (Tích Hợp)
- HTML/CSS/JS thuần (không framework).
- Fetch API để gọi backend.
- Hiển thị menu với hình ảnh base64.

### AI Models
- 🤖 **Groq Llama 3** (model: llama3-8b-8192)
  - Xử lý hội thoại tự nhiên.
  - Quản lý logic order (hỏi thông tin, xác nhận).
  - Gợi ý menu dựa trên prompt.

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  index   │  │  menu    │  │  chat    │  │ session  │   │
│  │  .html   │  │ sidebar  │  │ window   │  │ info     │   │
│  └────┬─────┘  └────┬──────┘  └────┬─────┘  └────┬─────┘   │
│       │              │              │             │         │
│       └──────────────┴──────────────┴─────────────┘         │
│                          │                                  │
│                    Fetch API (HTTP)                         │
└──────────────────────────┼──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │  main.py - Agent Executor & API Routes             │     │
│  │  • POST /chat                                       │     │
│  │  • OPTIONS /chat (CORS)                             │     │
│  │  • Session & Message Management                     │     │
│  └────┬───────────────────────────┬────────────────┬──┘     │
│       │                           │                │        │
│  ┌────▼─────┐  ┌─────────────────▼──┐  ┌─────────▼──────┐ │
│  │ LangChain│  │ Tools             │  │ Database       │ │
│  │ Agent    │  │ (save_order)     │  │ Utils          │ │
│  │          │  │                   │  │                │ │
│  └────┬─────┘  └─────────┬─────────┘  └────┬───────────┘ │
└───────┼──────────────────┼─────────────────┼──────────────┘
        │                  │                 │
┌───────▼──────┐  ┌────────▼────────┐  ┌────▼──────────────┐
│ Groq LLM     │  │ MySQL           │  │ MySQL             │
│ (Llama 3)    │  │ (Sessions)      │  │ (Orders/Messages) │
│              │  │                 │  │                   │
│ • Conversation│  │ • session_uuid  │  │ • customer_name   │
│ • Prompt      │  │ • created_at   │  │ • phone           │
│ • Tool Calling│  │                 │  │ • order_type      │
│              │  │                 │  │ • items (JSON)    │
└──────────────┘  └─────────────────┘  └───────────────────┘
```

## 📦 Cài Đặt
### Yêu Cầu Hệ Thống
- Python 3.12 trở lên
- MySQL Server 8.0+
- [Groq API Key](https://console.groq.com/keys) (miễn phí với giới hạn)

### Bước 1: Clone Repository
```
git clone https://github.com/PhamThang-209-204/mixue-chat-backend.git
cd mixue-chat-backend
```

### Bước 2: Tạo Virtual Environment
```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies
```
pip install fastapi uvicorn langchain-groq langchain pydantic mysql-connector-python python-dotenv
```

### Bước 4: Setup Database & .env
1. **Tạo DB**: Chạy script SQL trong README để tạo tables (`sessions`, `messages`, `orders`).
2. **File `.env`**:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_DATABASE=chatbot
   API_KEY=your_groq_api_key
   model=llama3-8b-8192  # Hoặc model khác hỗ trợ bởi Groq
   ```

### Bước 5: Chạy Server
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Output:
```
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12347]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Bước 6: Kết Nối Frontend
- Mở file `index.html` (từ frontend) trong browser.
- API sẽ nhận request từ `/chat`.

## 🚀 Sử Dụng
### Test API Với Curl
```
# Tin nhắn đầu tiên (tạo session)
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Giới thiệu menu"}'

# Tiếp tục session
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tôi muốn kem ốc quế", "session_uuid": "uuid-from-response"}'
```

### Flow Chatbot
1. **Khởi tạo**: Gửi message → AI chào và giới thiệu menu.
2. **Chọn món**: User chọn món → AI thêm vào giỏ.
3. **Thông tin**: AI hỏi tên, SĐT, loại đơn nếu thiếu.
4. **Xác nhận**: Hiển thị đơn → User xác nhận → Lưu DB và tạo session mới.

## 📖 API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **Endpoints**:
  - `POST /chat`: Xử lý tin nhắn (required: `message`; optional: `session_uuid`).
  - `OPTIONS /chat`: CORS preflight.

Chi tiết: Xem `/docs` hoặc file `main.py`.

## 📚 Tài Liệu
- [API Endpoints Guide](docs/API_ENDPOINTS_GUIDE.md) - Hướng dẫn chi tiết endpoints.
- [Database Schema](docs/DB_SCHEMA.md) - Cấu trúc tables.
- [LangChain Setup](docs/LANGCHAIN_SETUP.md) - Cấu hình agent và tools.

## 📸 Screenshots
## 🤝 Đóng Góp
Contributions, issues và feature requests đều được chào đón!

1. Fork repository.
2. Tạo branch (`git checkout -b feature/AmazingFeature`).
3. Commit changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to branch (`git push origin feature/AmazingFeature`).
5. Mở Pull Request.

## 📄 License
MIT License - xem file `LICENSE` để biết chi tiết.

## 👨‍💻 Tác Giả
Phạm Thắng

- GitHub: [@PhamThang-209-204](https://github.com/PhamThang-209-204)
- Email: thang20092004@gmail.com

🙏 **Acknowledgments**

- [Groq](https://groq.com) - LLM nhanh chóng.
- [FastAPI](https://fastapi.tiangolo.com) - Framework mạnh mẽ.
- [LangChain](https://python.langchain.com) - Agent và tools.
- [Mixue](https://mixue.com) - Nguồn cảm hứng menu.

⭐ **Nếu project này hữu ích, hãy cho một star nhé!** ⭐

Made with ❤️ by Phạm Thắng
