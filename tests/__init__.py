"""
Package kiểm thử tự động (Unit Test Layer).
Xác thực tính đúng đắn của các thuật toán và nghiệp vụ cốt lõi.
"""
import os
import sys

_SOURCE_CODE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source_code")
if _SOURCE_CODE_DIR not in sys.path:
    sys.path.insert(0, _SOURCE_CODE_DIR)
