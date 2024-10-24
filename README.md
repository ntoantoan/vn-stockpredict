# Stock Analysis Project

## Overview
This project is a stock analysis application that provides chart analysis and data management for stock market information. It uses FastAPI for the backend, PostgreSQL for data storage, and integrates with VNDirect for chart data.

## Features
- User authentication
- Chart analysis for stocks
- Data management for company information
- Admin functionalities

## Tech Stack
- Backend: FastAPI
- Database: PostgreSQL
- Containerization: Docker
- Web Scraping: Selenium
- Chart Data: VNDirect

## Setup and Installation
1. Clone the repository
2. Install Docker and Docker Compose
3. Run `docker compose up --build` to start the application

## Project Structure
- `app/`: Main application directory
  - `src/`: Source code
    - `chart/`: Chart analysis functionality
    - `dataset/`: Data insertion and management
    - `internal/`: Internal admin routes
    - `routers/`: API routes
  - `main.py`: Application entry point
- `run.sh`: Script to run the Docker containers

## API Endpoints
- `/api/auth`: Authentication routes
- `/api/chart-analysis`: Chart analysis routes
- `/api/admin`: Admin routes

## Database
The project uses a PostgreSQL database with a `companies` table to store stock information.

## Chart Example
![Chart Example](app/src/chart/screenshot.jpg)


{
  "tldr": "Xu hướng **đi ngang** với **phạm vi giao dịch** từ **25.50** đến **29.00**. Nến gần đây có **biến động mạnh**, ghi nhận một số **biến động giá** gần **26.75**. Động lượng khối lượng **giảm** có thể thiếu động lực cho một biến động lớn hơn.",
  "xu_huong_hien_tai": "Đi ngang, **25.50** - **29.00**",
  "hanh_dong_gia": "Nến gần đây cho thấy **sự dao động** mạnh trong **phạm vi hẹp**, đặc biệt quanh mức **26.75**, điều này thể hiện xu hướng thiếu **khả quan** để phá vỡ mức **kháng cự** hoặc mức **hỗ trợ**. Biến động giá bất ngờ có thể xảy ra dựa trên một số **tin tức cơ bản**.",
  "ho_tro": {
    "muc_gan_day": "26.50",
    "muc_chinh": "25.50"
  },
  "khang_cu": {
    "muc_gan_day": "27.50",
    "muc_chinh": "29.00"
  },
  "khoi_luong": "Khối lượng giao dịch gần đây **giảm**, đây là tín hiệu không **mạnh mẽ** cho một xu hướng **bứt phá**. Điều này có thể chỉ ra thị trường đang **chờ đợi** một chất xúc tác để phá vỡ **trạng thái tích lũy** hiện tại.",
  "du_doan": {
    "du_doan": "Cổ phiếu có thể **giảm** về mức **hỗ trợ** **25.50** nếu không có **bứt phá** mạnh, do khối lượng đang **yếu**. Sự thiếu vắng các **tin tức lớn** có thể làm chậm **biến động** đáng kể.",
    "muc_do_tin_cay": "Trung bình"
  },
  "chien_luoc_giao_dich_de_xuat": {
    "de_xuat": "Không giao dịch",
    "kich_ban_mua": "Nếu giá giảm về **25.50**, cân nhắc **mua** với **dừng lỗ** tại **24.50**. Điều này sẽ đảm bảo rủi ro được quản lý trong trường hợp có sự quay đầu thị trường.",
    "kich_ban_ban": "Nếu giá tăng tới gần **29.00**, xem xét **bán** nếu khối lượng tăng với **dừng lỗ** đặt tại **30.00** để tận dụng mức **kháng cự mạnh**."
  }
}

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
