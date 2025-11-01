#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

VENV_ACTIVATE="$SCRIPT_DIR/venv/bin/activate"
PYTHON_EXEC="$SCRIPT_DIR/venv/bin/python"
INDEX_SCRIPT="$SCRIPT_DIR/main_index.py"
ASK_SCRIPT="$SCRIPT_DIR/main_ask.py"
LIST_SCRIPT="$SCRIPT_DIR/main_list_files.py"
TREE_SCRIPT="$SCRIPT_DIR/main_list_tree.py"
CHAT_SCRIPT="$SCRIPT_DIR/main_chat.py"

if [ ! -f "$VENV_ACTIVATE" ]; then
  echo "Error: Virtual environment 'venv/bin/activate' tidak ditemukan di $SCRIPT_DIR"
  exit 1
fi
if [ ! -f "$PYTHON_EXEC" ]; then
  echo "Error: Python executable 'venv/bin/python' tidak ditemukan."
  exit 1
fi

source "$VENV_ACTIVATE"

COMMAND="$1"
shift

case "$COMMAND" in
  --index)
    PROJECT_PATH="$1" 
    if [ -z "$PROJECT_PATH" ]; then
      PROJECT_PATH=$(pwd)
      echo "[Info] Tidak ada path diberikan. Menggunakan direktori saat ini: $PROJECT_PATH"
    else
      echo "[Info] Mengindeks path spesifik: $PROJECT_PATH"
    fi
    "$PYTHON_EXEC" "$INDEX_SCRIPT" "$PROJECT_PATH"
    ;;

  --ask)
    if [ -z "$@" ]; then
      echo "Error: Perintah '--ask' membutuhkan pertanyaan."
      echo "Contoh: purwa --ask \"Bagaimana cara kerja auth?\""
      exit 1
    fi
    "$PYTHON_EXEC" "$ASK_SCRIPT" "$@"
    ;;

  --chat)
    echo "[Info] Memulai sesi chat interaktif..."
    "$PYTHON_EXEC" "$CHAT_SCRIPT"
    ;;

  --list)
    echo "[Info] Mengambil daftar file yang terindeks dari database..."
    "$PYTHON_EXEC" "$LIST_SCRIPT"
    ;;

  --tree)
    echo "[Info] Mengambil daftar file dan membangun tree..."
    "$PYTHON_EXEC" "$TREE_SCRIPT"
    ;;

  --help|-h)
    echo ""
    echo "Bantuan Penggunaan Purwa-Assistant: "
    echo ""
    echo "  run-purwa.sh --index [PATH]"
    echo "    - Mengindeks proyek di [PATH]. Jika path kosong,"
    echo "    - akan mengindeks direktori tempat Anda berada saat ini."
    echo ""
    echo "  run-purwa.sh --ask \"[PERTANYAAN]\""
    echo "    - Mengajukan satu pertanyaan langsung ke AI."
    echo ""
    echo "  run-purwa.sh --chat"
    echo "    - Memulai sesi chat interaktif (dengan ingatan)."
    echo ""
    echo "  run-purwa.sh --list"
    echo "    - Menampilkan semua file yang sudah terindeks (dari database)."
    echo ""
    echo "  run-purwa.sh --tree"
    echo "    - Menampilkan semua file yang sudah terindeks (tree)."
    echo ""
    echo "  run-purwa.sh --help"
    echo "    - Menampilkan pesan bantuan ini."
    ;;
      
  "")
    echo "[Error] Perintah tidak diberikan."
    "$0" --help
    exit 1
    ;;
      
  *)
    echo "[Error] Perintah tidak dikenal: '$COMMAND'"
    "$0" --help
    exit 1
    ;;
esac