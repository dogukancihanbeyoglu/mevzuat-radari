#!/usr/bin/env python3
"""
Web Server Launcher for Mevzuat Radarı.
Starts the FastAPI web server on http://localhost:8000.
Usage:
    python run_web.py [--port 8000] [--host 0.0.0.0]
"""
import os
import sys
import argparse
import uvicorn

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


def main():
    parser = argparse.ArgumentParser(description="Mevzuat Radarı Web Paneli")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Sunucu host IP adresi (varsayılan: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Sunucu portu (varsayılan: 8000)")
    parser.add_argument("--reload", action="store_true", help="Geliştirici modu: otomatik yeniden yükleme")

    args = parser.parse_args()

    print("================================================================")
    print("🌐 Mevzuat Radarı Web Paneli Başlatılıyor...")
    print(f"🔗 Erişim Adresi: http://{args.host}:{args.port}")
    print("================================================================")

    uvicorn.run(
        "src.web_app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
